import { apiClient } from './api.js';

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const statusText = document.getElementById('status-text');

let selectedFile = null;

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-blue-500', 'bg-blue-50/50');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-blue-500', 'bg-blue-50/50');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-blue-500', 'bg-blue-50/50');
    if (e.dataTransfer.files.length) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file.');
        return;
    }
    selectedFile = file;
    dropZone.querySelector('p').textContent = `Selected: ${file.name}`;
    dropZone.classList.add('border-green-500');
}

uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert('Please select a file first.');
        return;
    }

    try {
        uploadBtn.disabled = true;
        statusText.classList.remove('hidden');
        
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Mock call until backend is ready
        console.log('Uploading...', selectedFile.name);
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        alert('Analysis complete! Redirecting to dashboard...');
        window.location.href = 'dashboard.html';
    } catch (error) {
        alert('Upload failed: ' + error.message);
    } finally {
        uploadBtn.disabled = false;
        statusText.classList.add('hidden');
    }
});
