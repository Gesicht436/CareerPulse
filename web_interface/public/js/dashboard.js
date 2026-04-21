import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard Initialized');

    // Retrieve the analysis result from localStorage
    const storedData = localStorage.getItem('latest_analysis');

    if (!storedData) {
        console.warn('No analysis data found in localStorage. Showing mock data for demonstration.');
        // Optional: Redirect to upload.html or show a message
        return;
    }

    try {
        const fullResponse = JSON.parse(storedData);
        // The endpoint returns { filename, security_report, analysis: { job_title, match_details: { ... } } }
        const analysisData = fullResponse.analysis ? fullResponse.analysis.match_details : null;

        if (analysisData) {
            // Update the UI with real data
            if (fullResponse.analysis.job_title) {
                const titleEl = document.querySelector('header h1');
                if (titleEl) titleEl.textContent = `Match for ${fullResponse.analysis.job_title}`;

                const descEl = document.querySelector('header p');
                if (descEl) descEl.textContent = `Best match found at ${fullResponse.analysis.company || 'External Platform'}`;
            }

            renderDashboard(analysisData);
        } else {
            console.error('Analysis data is incomplete.');
        }
    } catch (e) {
        console.error('Error parsing stored analysis data:', e);
    }
});

function renderDashboard(data) {
    // 1. Update Score
    const scoreRing = document.getElementById('score-ring');
    scoreRing.textContent = `${Math.round(data.overall_score)}%`;

    // 2. Update Justification
    const justificationList = document.getElementById('justification-list');
    justificationList.innerHTML = data.justification.map(j => `
        <div class="flex gap-4 p-3 rounded-2xl hover:bg-slate-50 transition-colors">
            <div class="w-6 h-6 rounded-full bg-teal-50 shrink-0 flex items-center justify-center mt-0.5">
                <svg class="w-3 h-3 text-teal-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
            </div>
            <p class="text-slate-600 leading-relaxed text-sm">${j}</p>
        </div>
    `).join('');

    // 3. Update Skills
    const matchedContainer = document.getElementById('matched-skills');
    matchedContainer.innerHTML = data.matched_skills.map(s => 
        `<span class="px-4 py-1.5 bg-teal-50 text-teal-700 rounded-full text-xs font-bold border border-teal-100">${s}</span>`
    ).join('');

    const missingContainer = document.getElementById('missing-skills');
    missingContainer.innerHTML = data.missing_skills.map(s => 
        `<span class="px-4 py-1.5 bg-rose-50 text-rose-600 rounded-full text-xs font-bold border border-rose-100">${s}</span>`
    ).join('');

    // 4. Update Roadmap
    const roadmapContainer = document.getElementById('roadmap-container');
    roadmapContainer.innerHTML = data.career_roadmap.map((item, index) => `
        <div class="relative pl-8 ${index === data.career_roadmap.length - 1 ? '' : 'border-l-2 border-white/20'} pb-2">
            <div class="absolute -left-2.25 top-0 w-4 h-4 rounded-full bg-white shadow-lg"></div>
            <h4 class="font-bold text-white/70 text-sm uppercase tracking-widest mb-1">${item.week}</h4>
            <h3 class="font-bold text-lg text-white mb-1">${item.topic}</h3>
            <p class="text-xs text-white/70 leading-relaxed">${item.description}</p>
        </div>
    `).join('');
}