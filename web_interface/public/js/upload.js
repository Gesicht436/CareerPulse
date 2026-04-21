import { apiClient } from './api.js';

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const filePreview = document.getElementById('file-preview');
const fileNameDisplay = document.getElementById('file-name');
const removeFileBtn = document.getElementById('remove-file');
const statusContainer = document.getElementById('status-container');
const progressDisplay = document.getElementById('upload-progress');

let selectedFile = null;

dropZone.addEventListener('click', (e) => {
    // Prevent double trigger if clicking elements inside
    if (e.target !== fileInput) {
        fileInput.click();
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-violet-400', 'bg-violet-50/30');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-violet-400', 'bg-violet-50/30');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-violet-400', 'bg-violet-50/30');
    if (e.dataTransfer.files.length) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFileSelect(e.target.files[0]);
    }
});

removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    filePreview.classList.add('hidden');
});

function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file.');
        return;
    }
    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    filePreview.classList.remove('hidden');
}

uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert('Please select a file first.');
        return;
    }

    try {
        uploadBtn.disabled = true;
        statusContainer.classList.remove('hidden');

        // Progress simulation (for UI feel)
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress <= 95) {
                progressDisplay.textContent = `${progress}%`;
            }
        }, 150);

        const formData = new FormData();
        formData.append('file', selectedFile);

        // Actual API call to the unified endpoint
        const response = await apiClient.post('/api/v1/analyze', formData);

        console.log('Analysis Complete:', response);

        clearInterval(interval);
        progressDisplay.textContent = '100%';

        // Store result in localStorage for the dashboard to pick up
        localStorage.setItem('latest_analysis', JSON.stringify(response));

        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 800);

    } catch (error) {
        console.error('Upload Error:', error);
        alert('Analysis failed: ' + error.message);
        statusContainer.classList.add('hidden');
    } finally {
        uploadBtn.disabled = false;
    }
});