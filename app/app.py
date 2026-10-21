import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from recommendation_engine import RecommendationEngine
import ocr_services

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

engine = RecommendationEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    doc_type = data.get('doc_type', [])
    language = data.get('language', [])
    overlap = data.get('overlap', False)
    preference = data.get('preference', 'Accuracy')
    model_type = data.get('model_type', 'Both')
    
    print(f"DEBUG - Received data:")
    print(f"  doc_type: {doc_type}")
    print(f"  language: {language}")
    print(f"  overlap: {overlap}")
    print(f"  preference: {preference}")
    print(f"  model_type: {model_type}")
    
    result = engine.recommend(doc_type, language, overlap, preference, model_type)
    
    print(f"DEBUG - Result: {result}")
    
    return jsonify(result)

@app.route('/test_model', methods=['POST'])
def test_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
        
    model_name = request.form.get('model_name')
    language = request.form.get('language', 'en')
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = {}
        
        if model_name == 'Google Vision':
            result = ocr_services.predict_google_vision(filepath, lang=language)
        elif model_name == 'Gemini 2.5':
            result = ocr_services.predict_gemini(filepath)
        elif model_name == 'GPT-4o' or model_name == 'gpt-4o-mini':
            result = ocr_services.predict_gpt4o(filepath)
        elif model_name == 'Claude 4':
            result = ocr_services.predict_claude(filepath)
        elif model_name == 'EasyOCR':
            result = ocr_services.predict_easyocr(filepath, lang=language)
        elif model_name == 'Tesseract':
            result = ocr_services.predict_tesseract(filepath, lang=language)
        elif model_name == 'TrOCR':
            model_type = request.form.get('model_type_variant', 'printed') 
            result = ocr_services.predict_trocr(filepath, model_type=model_type)
        elif model_name == 'DocTR':
            result = ocr_services.predict_doctr(filepath)
        else:
            result = {"error": "Model testing not implemented for this model yet."}
            
        
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
