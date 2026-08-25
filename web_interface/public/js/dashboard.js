import { apiClient } from './api.js';

let isStrictQualification = true;
let userQualification = 'B.Tech / B.E.';
let allTopMatches = [];

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard Initialized');

    // Setup Modal Close Event Listeners
    const modal = document.getElementById('job-inspect-modal');
    const closeBtn = document.getElementById('close-modal-btn');
    const footerCloseBtn = document.getElementById('modal-footer-close-btn');

    const closeModal = () => {
        if (modal) modal.classList.add('hidden');
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (footerCloseBtn) footerCloseBtn.addEventListener('click', closeModal);
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }

    // Setup Educational Qualification Toggle Button Listener
    const toggleQualBtn = document.getElementById('toggle-qual-filter-btn');
    if (toggleQualBtn) {
        toggleQualBtn.addEventListener('click', handleQualificationToggle);
    }

    // Retrieve analysis result from localStorage
    const storedData = localStorage.getItem('latest_analysis');

    if (!storedData) {
        console.warn('No analysis data found in localStorage.');
        return;
    }

    try {
        const fullResponse = JSON.parse(storedData);
        userQualification = fullResponse.qualification || 'B.Tech / B.E.';
        allTopMatches = fullResponse.top_matches || (fullResponse.analysis ? [fullResponse.analysis] : []);
        
        updateQualificationBadge(userQualification, isStrictQualification);

        if (allTopMatches.length > 0) {
            renderTop5Recommendations(allTopMatches);
            renderSelectedJob(allTopMatches[0]);
        } else {
            console.error('No top matches available in analysis response.');
        }
    } catch (e) {
        console.error('Error parsing stored analysis data:', e);
    }
});

function updateQualificationBadge(qual, strict) {
    const badge = document.getElementById('qual-filter-badge');
    const desc = document.getElementById('qual-filter-desc');
    const btnText = document.getElementById('toggle-qual-btn-text');

    if (strict) {
        if (badge) {
            badge.className = 'inline-flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30';
            badge.textContent = `🎓 Qualification Filter: STRICT (${qual})`;
        }
        if (desc) desc.textContent = `Recommendations restricted strictly to jobs requiring your educational field (${qual}).`;
        if (btnText) btnText.textContent = `Disable Qualification Filter (Show All Fields)`;
    } else {
        if (badge) {
            badge.className = 'inline-flex items-center gap-1 px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-bold border border-amber-500/30';
            badge.textContent = `🌐 Qualification Filter: DISABLED (All Career Fields)`;
        }
        if (desc) desc.textContent = `Showing job recommendations across all career fields without educational degree restrictions.`;
        if (btnText) btnText.textContent = `Enable Qualification Filter (Restrict to ${qual})`;
    }
}

function handleQualificationToggle() {
    isStrictQualification = !isStrictQualification;
    updateQualificationBadge(userQualification, isStrictQualification);

    if (allTopMatches.length === 0) return;

    let displayMatches = allTopMatches;

    if (isStrictQualification && userQualification) {
        // Filter jobs matching qualification keywords
        const qualLower = userQualification.toLowerCase();
        const filtered = allTopMatches.filter(m => {
            const text = ((m.qualifications || "") + " " + (m.description || "") + " " + (m.job_title || "")).toLowerCase();
            return text.includes(qualLower) || text.includes('bachelor') || text.includes('engineering') || text.includes('computer science');
        });
        if (filtered.length > 0) displayMatches = filtered;
    }

    renderTop5Recommendations(displayMatches);
    if (displayMatches.length > 0) {
        renderSelectedJob(displayMatches[0]);
    }
}

function renderTop5Recommendations(matches) {
    const container = document.getElementById('top-5-recommendations-container');
    if (!container) return;

    container.innerHTML = matches.slice(0, 5).map((match, idx) => {
        const score = Math.round(match.match_details ? match.match_details.overall_score : 0);
        let badgeColor = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
        if (score < 50) badgeColor = 'bg-amber-500/20 text-amber-300 border-amber-500/40';

        const isFirst = idx === 0;
        const activeStyles = isFirst 
            ? 'ring-2 ring-violet-400 bg-violet-600/30 border-violet-500 shadow-lg shadow-violet-500/20' 
            : 'bg-slate-800/80 border-slate-700/80 hover:bg-slate-800 hover:border-violet-400/60';

        return `
            <div data-index="${idx}" class="rec-card cursor-pointer p-4 rounded-2xl border transition-all duration-200 flex flex-col justify-between group ${activeStyles}">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-[10px] font-extrabold uppercase tracking-widest text-slate-400">#${idx + 1} Match</span>
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold border ${badgeColor}">
                            ${score}%
                        </span>
                    </div>
                    <h4 class="font-extrabold text-white text-sm group-hover:text-violet-300 transition-colors line-clamp-1">${match.job_title}</h4>
                    <p class="text-xs text-slate-400 font-medium truncate mb-3">${match.company || 'Unknown Company'}</p>
                </div>
                <div class="pt-2 border-t border-slate-700/60 flex items-center justify-between text-[11px] text-slate-400">
                    <span class="truncate max-w-[90px] text-slate-400">${match.location || 'Remote'}</span>
                    <button data-index="${idx}" class="inspect-btn font-extrabold text-violet-400 group-hover:text-violet-300 hover:underline flex items-center gap-0.5 px-2 py-1 bg-violet-500/10 rounded-lg border border-violet-500/20">
                        Inspect →
                    </button>
                </div>
            </div>
        `;
    }).join('');

    // Attach click listeners to card & inspect button
    document.querySelectorAll('.rec-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const index = parseInt(card.getAttribute('data-index'), 10);
            
            document.querySelectorAll('.rec-card').forEach(c => {
                c.classList.remove('ring-2', 'ring-violet-400', 'bg-violet-600/30', 'border-violet-500', 'shadow-lg', 'shadow-violet-500/20');
                c.classList.add('bg-slate-800/80', 'border-slate-700/80');
            });
            
            card.classList.remove('bg-slate-800/80', 'border-slate-700/80');
            card.classList.add('ring-2', 'ring-violet-400', 'bg-violet-600/30', 'border-violet-500', 'shadow-lg', 'shadow-violet-500/20');
            
            renderSelectedJob(matches[index]);

            if (e.target.closest('.inspect-btn')) {
                e.stopPropagation();
                openInspectModal(matches[index]);
            }
        });
    });
}

function openInspectModal(match) {
    if (!match) return;

    const modal = document.getElementById('job-inspect-modal');
    if (!modal) return;

    const matchDetails = match.match_details || {};
    const score = Math.round(matchDetails.overall_score || 0);

    document.getElementById('modal-job-title').textContent = match.job_title || 'Target Job Role';
    
    const roleEl = document.getElementById('modal-role');
    if (roleEl) {
        roleEl.textContent = match.role ? `Specialization / Role: ${match.role}` : `Role: ${match.job_title}`;
    }

    document.getElementById('modal-company').textContent = match.company || 'Enterprise Partner';
    document.getElementById('modal-work-type').textContent = match.work_type || 'Full-time';

    const portalBadge = document.getElementById('modal-portal-badge');
    if (portalBadge) {
        if (match.job_portal) {
            portalBadge.textContent = `Source: ${match.job_portal}`;
            portalBadge.classList.remove('hidden');
        } else {
            portalBadge.classList.add('hidden');
        }
    }

    const matchBadge = document.getElementById('modal-match-badge');
    if (matchBadge) {
        matchBadge.textContent = `${score}% ATS Match`;
        if (score >= 70) {
            matchBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        } else {
            matchBadge.className = 'px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30';
        }
    }

    document.getElementById('modal-location').textContent = [match.location, match.country].filter(Boolean).join(', ') || 'Remote';
    document.getElementById('modal-experience').textContent = match.experience ? `${match.experience} Years` : 'Not specified';
    document.getElementById('modal-salary').textContent = match.salary_range || 'Competitive / Industry standard';
    document.getElementById('modal-qualifications').textContent = match.qualifications || "Bachelor's Degree";

    // Populate Company Profile
    const profileContainer = document.getElementById('modal-company-profile-container');
    const profileDetails = document.getElementById('modal-company-profile-details');
    if (profileContainer && profileDetails) {
        const cp = match.company_profile || {};
        if (typeof cp === 'object' && Object.keys(cp).length > 0) {
            profileContainer.classList.remove('hidden');
            let profileHtml = '';
            if (cp.Sector) profileHtml += `<div><span class="font-bold text-slate-700">Sector:</span> ${cp.Sector}</div>`;
            if (cp.Industry) profileHtml += `<div><span class="font-bold text-slate-700">Industry:</span> ${cp.Industry}</div>`;
            if (cp.CEO) profileHtml += `<div><span class="font-bold text-slate-700">CEO:</span> ${cp.CEO}</div>`;
            if (cp.Website) {
                const url = cp.Website.startsWith('http') ? cp.Website : `https://${cp.Website}`;
                profileHtml += `<div><span class="font-bold text-slate-700">Website:</span> <a href="${url}" target="_blank" rel="noopener" class="text-violet-600 font-bold hover:underline">${cp.Website}</a></div>`;
            }
            if (cp.Ticker) profileHtml += `<div><span class="font-bold text-slate-700">Ticker:</span> <span class="px-1.5 py-0.5 bg-slate-200 rounded font-mono text-[10px]">${cp.Ticker}</span></div>`;
            profileDetails.innerHTML = profileHtml || '<div>Enterprise Profile verified</div>';
        } else {
            profileContainer.classList.add('hidden');
        }
    }

    // Populate Responsibilities
    const respContainer = document.getElementById('modal-responsibilities-container');
    const respEl = document.getElementById('modal-responsibilities');
    if (respContainer && respEl) {
        if (match.responsibilities && match.responsibilities.length > 5) {
            respContainer.classList.remove('hidden');
            respEl.textContent = match.responsibilities;
        } else {
            respContainer.classList.add('hidden');
        }
    }

    const descEl = document.getElementById('modal-description');
    if (descEl) {
        descEl.textContent = match.description || 'Full description not provided.';
    }

    const skillsContainer = document.getElementById('modal-skills');
    if (skillsContainer) {
        const matched = matchDetails.matched_skills || [];
        const missing = matchDetails.missing_skills || [];

        let skillsHtml = '';
        matched.forEach(s => {
            skillsHtml += `<span class="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-xs font-bold border border-emerald-200 shadow-xs flex items-center gap-1">✓ ${s} (Matched)</span>`;
        });
        missing.forEach(s => {
            skillsHtml += `<span class="px-3 py-1.5 bg-rose-50 text-rose-600 rounded-full text-xs font-bold border border-rose-200 shadow-xs flex items-center gap-1">! ${s} (Missing Gap)</span>`;
        });

        if (!skillsHtml) {
            skillsHtml = '<span class="text-xs text-slate-400">Technical skills dynamically evaluated via AI vector space.</span>';
        }

        skillsContainer.innerHTML = skillsHtml;
    }

    // Recruiter Contact
    const contactContainer = document.getElementById('modal-contact-container');
    const contactText = document.getElementById('modal-contact-text');
    if (contactContainer && contactText) {
        if (match.contact_person || match.contact) {
            contactContainer.classList.remove('hidden');
            contactText.innerHTML = `<strong>Recruiter:</strong> ${match.contact_person || 'HR Department'} (${match.contact || 'Direct application on portal'})`;
        } else {
            contactContainer.classList.add('hidden');
        }
    }

    modal.classList.remove('hidden');
}

function renderSelectedJob(analysis) {
    if (!analysis) return;

    const matchDetails = analysis.match_details;

    const titleEl = document.getElementById('job-title');
    if (titleEl) titleEl.textContent = analysis.job_title;

    const companyEl = document.getElementById('company-name');
    if (companyEl) companyEl.textContent = analysis.company || 'Unknown Company';

    const locationEl = document.getElementById('job-location');
    if (locationEl) {
        const locStr = [analysis.location, analysis.country].filter(Boolean).join(', ');
        locationEl.innerHTML = `
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            ${locStr || 'Remote / Unspecified'}
        `;
    }

    const salaryEl = document.getElementById('salary-range');
    if (salaryEl) {
        salaryEl.innerHTML = `
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            ${analysis.salary_range || 'N/A'}
        `;
    }

    const expEl = document.getElementById('experience-level');
    if (expEl) {
        expEl.innerHTML = `
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            ${analysis.experience || 'Not specified'}
        `;
    }

    if (matchDetails) {
        renderDashboard(matchDetails);
    }
}

function renderDashboard(data) {
    const scoreRing = document.getElementById('score-ring');
    if (scoreRing) scoreRing.textContent = `${Math.round(data.overall_score)}%`;

    const justificationList = document.getElementById('justification-list');
    if (justificationList) {
        justificationList.innerHTML = (data.justification || []).map(j => `
            <div class="flex gap-3 text-xs text-slate-600 items-start">
                <span class="text-teal-600 font-bold shrink-0 mt-0.5">✓</span>
                <span class="leading-relaxed">${j}</span>
            </div>
        `).join('');
    }

    const matchedContainer = document.getElementById('matched-skills');
    if (matchedContainer) {
        matchedContainer.innerHTML = (data.matched_skills || []).map(s => 
            `<span class="px-3 py-1.5 bg-teal-50 text-teal-700 rounded-full text-xs font-bold border border-teal-100">${s}</span>`
        ).join('');
    }

    const missingContainer = document.getElementById('missing-skills');
    if (missingContainer) {
        missingContainer.innerHTML = (data.missing_skills || []).map(s => 
            `<span class="px-3 py-1.5 bg-rose-50 text-rose-600 rounded-full text-xs font-bold border border-rose-100">${s}</span>`
        ).join('');
    }

    const roadmapContainer = document.getElementById('roadmap-container');
    if (roadmapContainer) {
        roadmapContainer.innerHTML = (data.career_roadmap || []).map((item, index) => `
            <div class="relative pl-8 ${index === (data.career_roadmap || []).length - 1 ? '' : 'border-l-2 border-slate-700'} pb-4">
                <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-violet-500 shadow-lg shadow-violet-500/50"></div>
                <h4 class="font-bold text-violet-400 text-xs uppercase tracking-widest mb-1">${item.week}</h4>
                <h3 class="font-bold text-base text-white mb-1">${item.topic}</h3>
                <p class="text-xs text-slate-300 leading-relaxed max-w-3xl">${item.description}</p>
            </div>
        `).join('');
    }
}