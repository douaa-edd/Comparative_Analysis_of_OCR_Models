
class RecommendationEngine:
    def __init__(self):
        self.models = {
            "Handwritten": {
                "Open": [
                    {"name": "TrOCR", "accuracy": 70.75, "speed": 0.276},
                    {"name": "DocTR", "accuracy": 41.36, "speed": 1.171},
                    {"name": "Tesseract", "accuracy": 38.44, "speed": 0.718},
                    {"name": "EasyOCR", "accuracy": 31.03, "speed": 1.154}
                ],
                "Closed": [
                    {"name": "Gemini 2.5", "accuracy": 94.63, "speed": 2.568},
                    {"name": "Claude 4", "accuracy": 92.56, "speed": 3.633},
                    {"name": "GPT-4o", "accuracy": 92.48, "speed": 3.335},
                    {"name": "Google Vision", "accuracy": 79.17, "speed": 0.301}
                ]
            },
            "English": {
                "Open": [
                    {"name": "DocTR", "accuracy": 96.01, "speed": 2.900},
                    {"name": "EasyOCR", "accuracy": 89.82, "speed": 2.990},
                    {"name": "Tesseract", "accuracy": 88.42, "speed": 0.895},
                    {"name": "TrOCR", "accuracy": 0.90, "speed": 0.270} # Poor accuracy
                ],
                "Closed": [
                    {"name": "Google Vision", "accuracy": 95.13, "speed": 0.342},
                    {"name": "Claude 4", "accuracy": 93.05, "speed": 14.496},
                    {"name": "Gemini 2.5", "accuracy": 92.57, "speed": 3.879},
                    {"name": "GPT-4o", "accuracy": 91.13, "speed": 8.708}
                ]
            },
            "French": {
                "Open": [
                    {"name": "DocTR", "accuracy": 58.93, "speed": 3.177},
                    {"name": "EasyOCR", "accuracy": 57.12, "speed": 2.797},
                    {"name": "Tesseract", "accuracy": 55.54, "speed": 1.359},
                    {"name": "TrOCR", "accuracy": 0.43, "speed": 0.246}
                ],
                "Closed": [
                    {"name": "GPT-4o", "accuracy": 57.78, "speed": 7.303},
                    {"name": "Gemini 2.5", "accuracy": 57.18, "speed": 3.567},
                    {"name": "Google Vision", "accuracy": 56.90, "speed": 0.349},
                    {"name": "Claude 4", "accuracy": 54.66, "speed": 15.602}
                ]
            },
            "Arabic": {
                "Open": [
                    {"name": "EasyOCR", "accuracy": 38.58, "speed": 2.844},
                    {"name": "Tesseract", "accuracy": 21.38, "speed": 0.824},
                    {"name": "DocTR", "accuracy": 15.24, "speed": 1.530},
                    {"name": "TrOCR", "accuracy": 0.30, "speed": 0.170}
                ],
                "Closed": [
                    {"name": "Gemini 2.5", "accuracy": 52.32, "speed": 4.288},
                    {"name": "Google Vision", "accuracy": 52.09, "speed": 0.304},
                    {"name": "Claude 4", "accuracy": 46.26, "speed": 10.485},
                    {"name": "GPT-4o", "accuracy": 43.25, "speed": 4.448}
                ]
            },
            "Japanese": {
                "Open": [
                    {"name": "EasyOCR", "accuracy": 37.68, "speed": 3.912},
                    {"name": "DocTR", "accuracy": 26.39, "speed": 1.295},
                    {"name": "Tesseract", "accuracy": 15.37, "speed": 1.077},
                    {"name": "TrOCR", "accuracy": 1.60, "speed": 0.261}
                ],
                "Closed": [
                    {"name": "Gemini 2.5", "accuracy": 55.82, "speed": 3.881},
                    {"name": "Claude 4", "accuracy": 50.66, "speed": 4.215},
                    {"name": "Google Vision", "accuracy": 50.19, "speed": 0.376},
                    {"name": "GPT-4o", "accuracy": 49.04, "speed": 3.190}
                ]
            },
            "German": {
                "Open": [
                    {"name": "DocTR", "accuracy": 53.25, "speed": 1.671},
                    {"name": "EasyOCR", "accuracy": 52.02, "speed": 3.093},
                    {"name": "Tesseract", "accuracy": 20.42, "speed": 1.232},
                    {"name": "TrOCR", "accuracy": 4.04, "speed": 0.296}
                ],
                "Closed": [
                    {"name": "Gemini 2.5", "accuracy": 69.14, "speed": 3.834},
                    {"name": "Google Vision", "accuracy": 69.02, "speed": 0.396},
                    {"name": "Claude 4", "accuracy": 62.72, "speed": 6.517},
                    {"name": "GPT-4o", "accuracy": 59.86, "speed": 3.767}
                ]
            },
            "Spanish": {
                "Open": [
                    {"name": "EasyOCR", "accuracy": 58.72, "speed": 0.341},
                    {"name": "DocTR", "accuracy": 53.60, "speed": 1.080},
                    {"name": "Tesseract", "accuracy": 17.45, "speed": 0.314},
                    {"name": "TrOCR", "accuracy": 6.98, "speed": 0.143}
                ],
                "Closed": [
                    {"name": "Claude 4", "accuracy": 69.29, "speed": 3.550},
                    {"name": "GPT-4o", "accuracy": 67.96, "speed": 2.221},
                    {"name": "Gemini 2.5", "accuracy": 66.56, "speed": 2.202},
                    {"name": "Google Vision", "accuracy": 65.07, "speed": 0.210}
                ]
            },
            "Combined": {
                "Open": [
                     {"name": "DocTR", "accuracy": 25.06, "speed": 2.54},
                     {"name": "EasyOCR", "accuracy": 24.08, "speed": 9.50},
                     {"name": "Tesseract", "accuracy": 18.61, "speed": 1.68},
                     {"name": "TrOCR", "accuracy": 0.0, "speed": 0.0}
                ],
                "Closed": [
                    {"name": "Gemini 2.5", "accuracy": 37.45, "speed": 8.81},
                    {"name": "Google Vision", "accuracy": 34.77, "speed": 0.28},
                    {"name": "Claude 4", "accuracy": 25.89, "speed": 14.48},
                    {"name": "GPT-4o", "accuracy": 20.62, "speed": 5.92}
                ]
            }
        }

    def recommend(self, doc_type, language, overlap, preference, model_type):
        
        if not isinstance(doc_type, list): 
            doc_type = [doc_type] if doc_type else []
        if not isinstance(language, list): 
            language = [language] if language else []
        
        doc_type = [dt for dt in doc_type if dt]
        language = [lang for lang in language if lang]
        
        if not doc_type:
            doc_type = ['Typed']
        
        if not language and 'Typed' in doc_type:
            language = ['English']

      
        if len(language) > 1 or len(doc_type) > 1 or "Combined" in language:
             category = "Combined"
        elif "Handwritten" in doc_type:
             category = "Handwritten"
        else:
             category = language[0] if language else "English"
        
        if category not in self.models:
            return {"error": "Language/Category not supported"}

        candidates = []
        if model_type == "Open Source":
            candidates = self.models[category]["Open"]
        elif model_type == "Closed Source":
            candidates = self.models[category]["Closed"]
        else:
            candidates = self.models[category]["Open"] + self.models[category]["Closed"]

        
        
        filtered_candidates = []
        for model in candidates:
            if model["name"] == "TrOCR":
                if overlap:
                    continue
                if category != "Handwritten": 
                     continue
            filtered_candidates.append(model)
            
        candidates = filtered_candidates

        if not candidates:
            return {"error": "No suitable models found"}

        if preference == "Speed":
            recommended = sorted(candidates, key=lambda x: (x["speed"], -x["accuracy"]))
        else:
            recommended = sorted(candidates, key=lambda x: (-x["accuracy"], x["speed"]))

        best_model = recommended[0]
        
        return {
            "recommended_model": best_model,
            "all_candidates": recommended,
            "category": category
        }
