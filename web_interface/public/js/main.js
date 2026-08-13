import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Highlight Active Nav Link
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('text-violet-600', 'font-bold');
            link.classList.remove('text-gray-600', 'text-slate-400');
        }
    });

    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
            } else {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    // 3. User Session Avatar / Sign In badge rendering
    const authUserRaw = localStorage.getItem('auth_user');
    const adminToken = localStorage.getItem('admin_token');
    const userNavBadge = document.getElementById('user-nav-badge');
    const userNavInitial = document.getElementById('user-nav-initial');

    if (userNavBadge) {
        if (authUserRaw) {
            try {
                const user = JSON.parse(authUserRaw);
                const name = user.full_name || user.email || 'User';
                const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
                
                if (userNavInitial) {
                    userNavInitial.textContent = initials;
                }
                userNavBadge.setAttribute('title', `Logged in as ${name}`);
            } catch (e) {
                console.warn('Could not parse auth_user:', e);
            }
        }
    }

    // 4. Render Live Announcement Banner if published by Admin
    try {
        const settings = await apiClient.get('/api/v1/admin/settings');
        if (settings && settings.announcement_active && settings.announcement_banner) {
            renderAnnouncementBanner(settings.announcement_banner);
        }
    } catch (e) {
        // Silent catch if backend is not running live
    }

    function renderAnnouncementBanner(text) {
        const existingBanner = document.getElementById('global-announcement-banner');
        if (existingBanner) return;

        const banner = document.createElement('div');
        banner.id = 'global-announcement-banner';
        banner.className = 'bg-gradient-to-r from-violet-600 via-indigo-600 to-emerald-500 text-white text-xs font-bold py-2 px-4 text-center shadow-md relative z-50 flex items-center justify-center gap-2';
        banner.innerHTML = `
            <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
            <span>${text}</span>
            <button onclick="this.parentElement.remove()" class="ml-4 text-white/80 hover:text-white font-bold">&times;</button>
        `;
        document.body.prepend(banner);
    }
});
