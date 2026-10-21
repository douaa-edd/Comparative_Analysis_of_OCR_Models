document.addEventListener('DOMContentLoaded', () => {
    console.log("Script loaded successfully!");

    const form = document.getElementById('recommendation-form');
    const inputSection = document.getElementById('input-section');
    const resultsSection = document.getElementById('results-section');
    const resetBtn = document.getElementById('reset-btn');
    const testBtn = document.getElementById('test-btn');
    const testArea = document.getElementById('test-area');
    const testResults = document.getElementById('test-results');
    const loadingSpinner = document.getElementById('loading-spinner');
    const ocrOutput = document.getElementById('ocr-output');
    const ocrTime = document.getElementById('ocr-time');

    let currentRecommendedModel = null;
    let selectedFile = null;
    let modelToTest = null;

    try {
        toggleLanguage();
    } catch (e) {
        console.error("Init Error", e);
    }

    const fileUpload = document.getElementById('file-upload');
    if (fileUpload) {
        fileUpload.addEventListener('change', (e) => {
            selectedFile = e.target.files[0];
            console.log("File selected:", selectedFile ? selectedFile.name : "none");
        });
    }

    // Doc Type listener
    const docTypeCheckboxes = document.querySelectorAll('input[name="doc_type"]');
    docTypeCheckboxes.forEach(cb => {
        cb.addEventListener('change', toggleLanguage);
    });

    if (!form) {
        console.error("FATAL: Form not found!");
        alert("Error: Form not found. Please refresh the page.");
        return;
    }

    console.log("Form found, attaching submit handler...");

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        e.stopPropagation();

        console.log("Form submitted!");

        const formData = new FormData(form);
        const data = {
            doc_type: formData.getAll('doc_type'),
            language: formData.getAll('language'),
            overlap: formData.get('overlap') === 'on',
            preference: formData.get('preference'),
            model_type: formData.get('model_type')
        };

        console.log("DEBUG - Sending data:", data);

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            console.log("DEBUG - Received result:", result);

            if (result.error) {
                alert("Error: " + result.error);
                return;
            }

            currentRecommendedModel = result.recommended_model;
            displayResults(result);

            if (selectedFile) {
                testArea.classList.remove('hidden');
                testResults.classList.add('hidden');

                if (isSupportedModel(currentRecommendedModel.name)) {
                    modelToTest = currentRecommendedModel;
                    testBtn.innerText = `Test ${currentRecommendedModel.name}`;
                    testBtn.disabled = false;
                } else {
                    const fallback = result.all_candidates.find(m => isSupportedModel(m.name));
                    if (fallback) {
                        modelToTest = fallback;
                        testBtn.innerText = `Test with ${fallback.name} (Recommended not available online)`;
                        testBtn.disabled = false;
                    } else {
                        modelToTest = null;
                        testBtn.innerText = "No online test available for these models";
                        testBtn.disabled = true;
                    }
                }
            } else {
                testArea.classList.add('hidden');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred: ' + error.message);
        }
    });

    testBtn.addEventListener('click', () => {
        if (!selectedFile) return;

        const manualSelect = document.getElementById('manual-model-select');
        let finalModelName = null;

        if (manualSelect && manualSelect.value) {
            finalModelName = manualSelect.value;
        } else if (modelToTest) {
            finalModelName = modelToTest.name;
        }

        if (finalModelName) {
            runOcrTest(finalModelName);
        } else {
            alert("No model selected or available for testing.");
        }
    });

    resetBtn.addEventListener('click', () => {
        resultsSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        inputSection.classList.add('animate-up');
        window.scrollTo({ top: 0, behavior: 'smooth' });

        form.reset();
        toggleLanguage();
        selectedFile = null;
        testArea.classList.add('hidden');
    });

    function toggleLanguage() {
        const checkedTypes = Array.from(document.querySelectorAll('input[name="doc_type"]:checked')).map(cb => cb.value);
        const languageGroup = document.getElementById('language-group');

        if (checkedTypes.length === 1 && checkedTypes[0] === 'Handwritten') {
            languageGroup.style.display = 'none';
        } else {
            languageGroup.style.display = 'block';
            languageGroup.classList.add('animate-up');
        }
    }

    async function runOcrTest(modelName) {
        testResults.classList.remove('hidden');
        loadingSpinner.classList.remove('hidden');
        ocrOutput.innerText = '';
        ocrTime.innerText = '';

        const allBtns = document.querySelectorAll('.test-candidate-btn, #test-btn');
        allBtns.forEach(b => b.disabled = true);

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('model_name', modelName);
        try {
            const langEl = document.querySelector('input[name="language"]:checked');
            const langVal = langEl ? langEl.value : 'English';

            formData.append('language', langVal);

            const response = await fetch('/test_model', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            loadingSpinner.classList.add('hidden');
            allBtns.forEach(b => b.disabled = false);

            if (result.error) {
                ocrOutput.innerText = result.error;
                ocrOutput.style.color = 'red';
            } else {
                ocrOutput.innerText = result.text;
                ocrOutput.style.color = 'var(--text-primary)';
                ocrTime.innerText = `Model: ${modelName} | Time: ${result.time}s`;
            }

            testResults.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            console.error('Error:', error);
            loadingSpinner.classList.add('hidden');
            allBtns.forEach(b => b.disabled = false);
            alert('Error connecting to server.');
        }
    }

    function isSupportedModel(modelName) {
        const supported = ['Google Vision', 'Gemini 2.5', 'GPT-4o', 'Claude 4', 'EasyOCR', 'Tesseract', 'TrOCR', 'DocTR'];
        return supported.includes(modelName);
    }

    function displayResults(data) {
        console.log("displayResults called with:", data);
        try {
            const inputSection = document.getElementById('input-section');
            const resultsSection = document.getElementById('results-section');
            const bestModelCard = document.getElementById('best-model-card');
            const otherCandidatesDiv = document.getElementById('other-candidates');

            console.log("Elements found:", {
                inputSection: !!inputSection,
                resultsSection: !!resultsSection,
                bestModelCard: !!bestModelCard,
                otherCandidatesDiv: !!otherCandidatesDiv
            });

            inputSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            resultsSection.classList.add('animate-up');

            console.log("Sections toggled");

            window.scrollTo({ top: 0, behavior: 'smooth' });

            const best = data.recommended_model;
            const prefEl = document.querySelector('input[name="preference"]:checked');
            const prefVal = prefEl ? prefEl.value : 'Accuracy';

            console.log("Building card for:", best.name);

            bestModelCard.innerHTML = `
                <div class="model-name">${best.name}</div>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-label">Accuracy</div>
                        <div class="stat-value" style="color: var(--success-color)">${best.accuracy}%</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Speed</div>
                        <div class="stat-value">${best.speed}s</div>
                    </div>
                </div>
                <div style="margin-top: 1rem; text-align: center; color: var(--text-secondary); font-size: 0.9rem;">
                    Best match for <strong>${data.category}</strong> with priority on <strong>${prefVal}</strong>
                </div>
            `;

            console.log("Card HTML set, building candidates list");

            otherCandidatesDiv.innerHTML = '';
            data.all_candidates.slice(1).forEach(model => {
                const div = document.createElement('div');
                div.className = 'candidate-card';

                let btnHtml = '';
                if (isSupportedModel(model.name) && selectedFile) {
                    btnHtml = `<button class="btn-secondary test-candidate-btn" data-model="${model.name}" style="margin-top:0.5rem; padding: 0.3rem 0.8rem; font-size: 0.8rem;">Test This</button>`;
                }

                div.innerHTML = `
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">${model.name}</div>
                    <div style="font-size: 0.9rem; color: var(--text-secondary);">
                        <div>Acc: ${model.accuracy}%</div>
                        <div>Speed: ${model.speed}s</div>
                    </div>
                    ${btnHtml}
                `;
                otherCandidatesDiv.appendChild(div);
            });

            document.querySelectorAll('.test-candidate-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    runOcrTest(e.target.dataset.model);
                });
            });

            console.log("displayResults completed successfully!");

        } catch (e) {
            console.error("Display Error", e);
            alert("Display Error: " + e.message);
        }
    }
});
