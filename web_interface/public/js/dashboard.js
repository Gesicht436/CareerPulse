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
        // The endpoint returns { filename, security_report, analysis: { job_title, match_details: { ... }, ... } }
        const analysis = fullResponse.analysis;
        const matchDetails = analysis ? analysis.match_details : null;

        if (matchDetails) {
            // Update the UI with real data
            if (analysis.job_title) {
                const titleEl = document.getElementById('job-title');
                if (titleEl) titleEl.textContent = analysis.job_title;

                const companyEl = document.getElementById('company-name');
                if (companyEl) companyEl.textContent = analysis.company || 'Unknown Company';

                const locationEl = document.getElementById('job-location');
                if (locationEl) {
                    const locStr = [analysis.location, analysis.country].filter(Boolean).join(', ');
                    locationEl.innerHTML = `
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        ${locStr || 'Remote / Unspecified'}
                    `;
                }

                const salaryEl = document.getElementById('salary-range');
                if (salaryEl) {
                    salaryEl.innerHTML = `
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        ${analysis.salary_range || 'N/A'}
                    `;
                }

                const expEl = document.getElementById('experience-level');
                if (expEl) {
                    expEl.innerHTML = `
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                        ${analysis.experience || 'Not specified'}
                    `;
                }
            }

            renderDashboard(matchDetails);
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