import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-jd-btn');
    const jdInput = document.getElementById('jd-input');
    const placeholder = document.getElementById('analysis-placeholder');
    const results = document.getElementById('analysis-results');

    analyzeBtn.addEventListener('click', async () => {
        const text = jdInput.value.trim();
        if (!text) {
            alert('Please paste a job description first.');
            return;
        }

        try {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';

            // Actual API call would go here
            // const matchResult = await apiClient.post('/smart_match/analyze_jd', { jd_text: text });
            
            console.log('Analyzing JD match...', text.substring(0, 50) + '...');
            await new Promise(resolve => setTimeout(resolve, 2000));

            placeholder.classList.add('hidden');
            results.classList.remove('hidden');
            
            // In a real app, we'd populate the results div with data from matchResult

        } catch (error) {
            alert('Analysis failed: ' + error.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Match';
        }
    });
});