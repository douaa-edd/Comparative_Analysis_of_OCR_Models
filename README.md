# Comparative Analysis and Recommendation of OCR Models

A comprehensive web application for comparing and recommending OCR (Optical Character Recognition) models based on document type, language, and user preferences. This project includes benchmarking of both open-source and closed-source OCR models across multiple languages and document types.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Datasets](#datasets)
- [Supported OCR Models](#supported-ocr-models)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Benchmarking Results](#benchmarking-results)
- [Project Structure](#project-structure)

## Overview
This project provides a comprehensive solution for OCR model evaluation and recommendation. It includes:

-   **Web Application**: A Flask-based web interface for OCR model recommendation and testing
-   **Benchmarking Notebooks**: Jupyter notebooks for evaluating OCR models on various datasets
-   **Recommendation Engine**: An intelligent system that suggests the best OCR model based on specific requirements
-   **Research Article**: A formal study detailing the methodology, results, and analysis of the comparison.

## Features
-   **Model Comparison**: Compare 8 different OCR models (4 open-source, 4 closed-source)
-   **Multi-language Support**: Test and compare models across 6 languages (English, French, Arabic, Japanese, German, Spanish)
-   **Document Type Recognition**: Specialized handling for handwritten and typed documents
-   **Overlap Detection**: Identify and handle overlapping text in documents
-   **Performance Metrics**: Evaluate models using Accuracy, Character Error Rate (CER), and Word Error Rate (WER)
-   **Real-time Testing**: Upload images and test OCR models directly through the web interface
-   **Smart Recommendations**: Get model suggestions based on document type, language, and performance preference (speed vs. accuracy)

## Architecture
The system consists of three main components:

1.  **Web Application** (`app/`): Flask-based web interface
2.  **Benchmarking Suite** (`*.ipynb`): Jupyter notebooks for model evaluation
3.  **Dataset Management** (`Data/`): Organized datasets for testing

### Technology Stack
-   **Backend**: Flask (Python web framework)
-   **Frontend**: HTML, CSS, JavaScript
-   **OCR Models**:
    -   *Closed-source*: Google Vision, Gemini 2.5, GPT-4o, Claude 4
    -   *Open-source*: Tesseract, EasyOCR, TrOCR, DocTR

## Datasets
The project includes four primary dataset categories used for comprehensive testing:

1.  **Handwritten Dataset**
    -   Contains handwritten text images
    -   Used for evaluating handwriting recognition capabilities

2.  **Multilingual Dataset**
    -   Includes typed text in 6 languages:
        -   English (`dataset_eng/`)
        -   French (`dataset_french/`)
        -   Arabic (`dataset_arabic/`)
        -   Japanese (`dataset_japanese/`)
        -   German (`dataset_german/`)
        -   Spanish (`dataset_spanish/`)

3.  **Overlap Dataset**
    -   Contains images with overlapping text
    -   Tests model robustness in complex scenarios

4.  **Combined Dataset**
    -   A diverse mix of handwritten, printed, and overlapping text.
    -   Used to evaluate versatile, general-purpose performance of models.

Each dataset includes:
-   `images/`: Collection of test images
-   `labels.csv` or `label.csv`: Ground truth text for evaluation

## Supported OCR Models

### Closed-Source Models
-   **Google Vision OCR**: Cloud-based OCR service. Excellent for multi-language support.
-   **Gemini 2.5**: Google's multimodal AI model. Strong performance on handwritten text.
-   **GPT-4o-mini**: OpenAI's vision-language model. Good overall performance.
-   **Claude 4**: Anthropic's vision-capable model. Competitive accuracy.

### Open-Source Models
-   **Tesseract**: Traditional OCR engine. Fast processing speed, good for printed text.
-   **EasyOCR**: Deep learning-based OCR. Supports 80+ languages.
-   **TrOCR**: Transformer-based OCR. Excellent for handwritten text but slower.
-   **DocTR**: Document text recognition. Good for typed documents.

## Installation

### Prerequisites
-   Python 3.8 or higher
-   pip package manager
-   Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/DouaaEdd/Project_OCR.git
cd Project_OCR
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract (for Tesseract OCR)
-   **Windows**: Download installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.
-   **Linux**: `sudo apt-get install tesseract-ocr`
-   **macOS**: `brew install tesseract`

## Configuration

### API Keys Setup
Create or update the `app/ocr_services.py` file and place credentials in the `app/` directory:

1.  **Google Vision**: Place your credentials JSON file in `app/` directory.
    ```python
    GOOGLE_CREDS_FILE = 'Credentials_Google_Cloud.json'
    ```
2.  **Gemini API**: Set in `app/ocr_services.py`.
    ```python
    GEMINI_API_KEY = 'your-gemini-api-key'
    ```
3.  **OpenAI API**: Set in `app/ocr_services.py`.
    ```python
    GPT_API_KEY = 'your-openai-api-key'
    ```
4.  **Anthropic API**: Set in `app/ocr_services.py`.
    ```python
    CLAUDE_API_KEY = 'your-anthropic-api-key'
    ```

## Usage

### Running the Web Application
Navigate to the app directory and start the Flask server:
```bash
cd app
python app.py
```
Open your browser and search for: `http://localhost:5000`

### Using the Web Interface
1.  **Get Recommendations**: Select document type, language, overlap, preference, and model type. Click "Get Recommendation".
2.  **Test Models**: Upload an image, select a specific OCR model, and view extracted text and processing time.

### Running Benchmarks
Open Jupyter Notebook:
```bash
jupyter notebook
```
Open one of the comparison notebooks in the `Comparative Study/` folder:
-   `ocr_comparison_closed.ipynb`: Benchmarks closed-source models
-   `ocr_comparison_open.ipynb`: Benchmarks open-source models
-   `ocr_comparaison_combined.ipynb`: Benchmarks combined performance

Run cells sequentially to load models, test on datasets, and generate metrics.

## Benchmarking Results

### Key Performance Metrics
-   **Accuracy**: Overall text recognition accuracy (%)
-   **CER (Character Error Rate)**: Character-level error rate
-   **WER (Word Error Rate)**: Word-level error rate
-   **Speed**: Processing time per image (seconds)

### General Findings

#### Handwritten Text
-   **Best Accuracy**: Gemini 2.5 (94.63%)
-   **Fastest**: Google Vision (0.301s)
-   **Best Open-Source**: TrOCR (70.75%)

#### Typed Text (English)
-   **Best Accuracy**: DocTR (96.01%)
-   **Fastest**: Google Vision (0.342s)
-   **Most Balanced**: DocTR

#### Combined Dataset (Mixed Types)
-   **Best Accuracy**: Gemini 2.5 (37.45%)
-   **Fastest**: Google Vision (0.28s)
-   **Best Open-Source**: DocTR (25.06%)

#### Multilingual
-   Closed-source models generally outperform open-source.
-   Google Vision offers best speed across all languages.
-   Gemini 2.5 shows strong multilingual capabilities.

## Project Structure

```text
Project_OCR/
├── app/
│   ├── app.py                      # Main Flask application
│   ├── ocr_services.py             # OCR model implementations
│   ├── recommendation_engine.py    # Recommendation logic
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Application styles
│   │   ├── js/
│   │   │   └── script.js           # Frontend logic
│   │   └── uploads/                # Temporary upload folder
│   └── templates/
│       └── index.html              # Main web interface
├── Data/
│   ├── Handwritten_dataset/
│   ├── Multilangual_dataset/
│   ├── Overlap_dataset/
│   └── Combined_dataset/           # Diverse mixed dataset
├── Comparative Study/
│   ├── ocr_comparison_closed.ipynb # Closed-source model benchmarks
│   ├── ocr_comparison_open.ipynb   # Open-source model benchmarks
│   ├── ocr_comparaison_combined.ipynb # Combined benchmarks
│   └── Benchmark.pdf               # Complete benchmark results and analysis
├── Article.pdf                     # Research Article
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```