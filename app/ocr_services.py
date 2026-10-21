import os
import io
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from google.cloud import vision
import google.generativeai as genai
from openai import OpenAI
import anthropic


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CREDS_FILE = os.path.join(BASE_DIR, 'Credentials_Google_Cloud.json')
GEMINI_API_KEY = 'YourGeminiAPIKeyHere'
GPT_API_KEY = 'YourGPTAPIKeyHere'
CLAUDE_API_KEY = 'YourClaudeAPIKeyHere'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDS_FILE
vision_client = vision.ImageAnnotatorClient()

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash') 

openai_client = OpenAI(api_key=GPT_API_KEY) 

claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def predict_google_vision(image_path, lang="en"):
    start_time = time.time()
    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = vision_client.text_detection(image=image, image_context={"language_hints": [lang]})
        
        if response.error.message:
            return {"text": f"Error: {response.error.message}", "time": 0}

        texts = response.text_annotations
        if texts:
            result = texts[0].description
        else:
            result = ""
            
        elapsed = time.time() - start_time
        return {"text": result, "time": round(elapsed, 3)}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_gemini(image_path):
    start_time = time.time()
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        response = gemini_model.generate_content([
            "Extract all text from this image exactly as it appears.",
            {"mime_type": "image/jpeg", "data": image_data}
        ])
        
        elapsed = time.time() - start_time
        return {"text": response.text, "time": round(elapsed, 3)}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_gpt4o(image_path):
    start_time = time.time()
    try:
        import base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image exactly as it appears."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
            timeout=30.0
        )
        
        result = response.choices[0].message.content
        elapsed = time.time() - start_time
        return {"text": result, "time": round(elapsed, 3)}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_claude(image_path):
    start_time = time.time()
    try:
        import base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from this image exactly as it appears."
                        }
                    ]
                }
            ]
        )
        
        result = message.content[0].text
        elapsed = time.time() - start_time
        return {"text": result, "time": round(elapsed, 3)}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "time": 0}

# --- Open Source Models Integration ---

easyocr_reader_en = None
easyocr_reader_latin = None
easyocr_reader_arabic = None
easyocr_reader_japanese = None

trocr_processor_hw = None
trocr_model_hw = None
trocr_processor_pr = None
trocr_model_pr = None

doctr_model = None

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

lang_map_tess = {
    'eng': 'eng',
    'fra': 'fra',
    'deu': 'deu',
    'spa': 'spa',
    'ara': 'ara',
    'jpn': 'jpn'
}
ALL_TESS_LANGS = "eng+fra+deu+spa+ara+jpn"

def load_easyocr_models():
    global easyocr_reader_en, easyocr_reader_latin, easyocr_reader_arabic, easyocr_reader_japanese
    import easyocr
    if easyocr_reader_en is None:
        print("Loading EasyOCR models...")
        easyocr_reader_en = easyocr.Reader(['en'], gpu=False)
        easyocr_reader_latin = easyocr.Reader(['en', 'fr', 'de', 'es'], gpu=False)
        easyocr_reader_arabic = easyocr.Reader(['ar', 'en'], gpu=False)
        easyocr_reader_japanese = easyocr.Reader(['ja', 'en'], gpu=False)
        print("EasyOCR models loaded.")

def load_trocr_models():
    global trocr_processor_hw, trocr_model_hw, trocr_processor_pr, trocr_model_pr
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if trocr_model_hw is None:
        print("Loading TrOCR models...")
        trocr_processor_hw = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        trocr_model_hw = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to(device)
        
        trocr_processor_pr = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
        trocr_model_pr = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed').to(device)
        print("TrOCR models loaded.")
    return device

def load_doctr_model():
    global doctr_model
    from doctr.models import ocr_predictor
    if doctr_model is None:
        print("Loading DocTR model...")
        doctr_model = ocr_predictor(pretrained=True)
        print("DocTR model loaded.")

def predict_easyocr(image_path, lang='en'):
    start_time = time.time()
    logger.info(f"Starting EasyOCR prediction for {lang}")
    try:
        load_easyocr_models()
        if lang == 'Arabic':
            reader = easyocr_reader_arabic
        elif lang == 'Japanese':
            reader = easyocr_reader_japanese
        elif lang in ['French', 'German', 'Spanish']:
            reader = easyocr_reader_latin
        else:
            reader = easyocr_reader_en
            
        result = reader.readtext(image_path, detail=0)
        text = ' '.join(result)
        elapsed = time.time() - start_time
        logger.info(f"EasyOCR prediction completed in {elapsed:.2f}s")
        return {"text": text, "time": round(elapsed, 3)}
    except Exception as e:
        import traceback
        logger.error(f"EasyOCR failed: {e}")
        logger.error(traceback.format_exc())
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_tesseract(image_path, lang='English'):
    start_time = time.time()
    try:
        from PIL import Image
        img = Image.open(image_path)
        
        lang_code_map = {
            'English': 'eng', 'French': 'fra', 'Arabic': 'ara',
            'Japanese': 'jpn', 'German': 'deu', 'Spanish': 'spa'
        }
        
        tess_lang = lang_code_map.get(lang, 'eng')

        
        text = pytesseract.image_to_string(img, lang=tess_lang)
        elapsed = time.time() - start_time
        return {"text": text.strip(), "time": round(elapsed, 3)}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_trocr(image_path, model_type='printed'):
    start_time = time.time()
    logger.info(f"Starting TrOCR prediction for {model_type}")
    try:
        import torch
        from PIL import Image
        device = load_trocr_models()
        image = Image.open(image_path).convert("RGB")
        
        if model_type == 'handwritten':
            processor = trocr_processor_hw
            model = trocr_model_hw
        else:
            processor = trocr_processor_pr
            model = trocr_model_pr
            
        pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        elapsed = time.time() - start_time
        logger.info(f"TrOCR prediction completed in {elapsed:.2f}s")
        return {"text": text.strip(), "time": round(elapsed, 3)}
    except Exception as e:
        logger.error(f"TrOCR failed: {e}")
        return {"text": f"Error: {str(e)}", "time": 0}

def predict_doctr(image_path):
    start_time = time.time()
    logger.info("Starting DocTR prediction")
    try:
        try:
            from doctr.io import DocumentFile
        except ImportError:
            return {"text": "Error: DocTR is not installed. Install with: pip install python-doctr[torch]", "time": 0}
        
        load_doctr_model()
        doc = DocumentFile.from_images(image_path)
        result = doctr_model(doc)
        
        text_lines = []
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    line_text = ' '.join([word.value for word in line.words])
                    text_lines.append(line_text)
                    
        elapsed = time.time() - start_time
        logger.info(f"DocTR prediction completed in {elapsed:.2f}s")
        return {"text": ' '.join(text_lines), "time": round(elapsed, 3)}
    except Exception as e:
        import traceback
        logger.error(f"DocTR failed: {e}")
        logger.error(traceback.format_exc())
        return {"text": f"Error: {str(e)}", "time": 0}

