import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing WebRTC 1-on-1 Expert Session...');

    // 1. Extract or generate Room ID
    const urlParams = new URLSearchParams(window.location.search);
    let roomId = urlParams.get('room_id');
    if (!roomId) {
        roomId = 'room-demo-101';
        urlParams.set('room_id', roomId);
        window.history.replaceState({}, '', `${window.location.pathname}?${urlParams.toString()}`);
    }

    document.getElementById('room-id-display').textContent = roomId;

    // DOM Elements
    const localVideo = document.getElementById('local-video');
    const remoteVideo = document.getElementById('remote-video');
    const videoPlaceholder = document.getElementById('video-placeholder');
    const sessionStatus = document.getElementById('session-status');
    const toggleMicBtn = document.getElementById('toggle-mic-btn');
    const toggleCamBtn = document.getElementById('toggle-cam-btn');
    const endCallTopBtn = document.getElementById('end-call-top-btn');
    const endCallMainBtn = document.getElementById('end-call-main-btn');

    const tabBriefingBtn = document.getElementById('tab-briefing-btn');
    const tabChatBtn = document.getElementById('tab-chat-btn');
    const tabBriefingContent = document.getElementById('tab-briefing-content');
    const tabChatContent = document.getElementById('tab-chat-content');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // WebRTC & Media Variables
    let localStream = null;
    let peerConnection = null;
    let ws = null;
    let isAudioMuted = false;
    let isVideoMuted = false;

    const rtcConfig = {
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' }
        ]
    };

    // 2. Initialize Media & WebSockets
    try {
        // Capture local camera & microphone
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;
        console.log('Local camera/microphone captured successfully.');

        // Initialize WebSocket connection to FastAPI signaling server
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//localhost:8000/api/v1/expert/ws/${roomId}`;
        
        ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            sessionStatus.textContent = 'Signaling Connected (Waiting for peer)';
            console.log('WebSocket signaling connected.');
        };

        ws.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            console.log('WebSocket message received:', data.type);

            switch (data.type) {
                case 'room_joined':
                    sessionStatus.textContent = `Room Joined (${data.peer_count} peer active)`;
                    break;

                case 'peer_ready':
                    sessionStatus.textContent = 'Peer Joined! Negotiating WebRTC Connection...';
                    // Initiate WebRTC Call (Sender)
                    createPeerConnection();
                    const offer = await peerConnection.createOffer();
                    await peerConnection.setLocalDescription(offer);
                    ws.send(JSON.stringify({ type: 'offer', offer: offer }));
                    break;

                case 'offer':
                    sessionStatus.textContent = 'Receiving Incoming Call...';
                    createPeerConnection();
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    ws.send(JSON.stringify({ type: 'answer', answer: answer }));
                    break;

                case 'answer':
                    sessionStatus.textContent = 'Call Connected 🟢';
                    if (peerConnection) {
                        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
                    }
                    break;

                case 'ice_candidate':
                    if (peerConnection && data.candidate) {
                        try {
                            await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
                        } catch (e) {
                            console.error('Error adding ICE candidate:', e);
                        }
                    }
                    break;

                case 'chat_message':
                    renderChatMessage(data.sender || 'Peer', data.text, false);
                    break;

                case 'peer_disconnected':
                    sessionStatus.textContent = 'Peer Disconnected';
                    videoPlaceholder.classList.remove('hidden');
                    if (remoteVideo.srcObject) {
                        remoteVideo.srcObject = null;
                    }
                    break;

                case 'hangup':
                    sessionStatus.textContent = 'Call Ended by Peer';
                    videoPlaceholder.classList.remove('hidden');
                    if (remoteVideo.srcObject) {
                        remoteVideo.srcObject = null;
                    }
                    break;

                default:
                    break;
            }
        };

        ws.onclose = () => {
            sessionStatus.textContent = 'Disconnected from Server';
        };

    } catch (e) {
        console.error('Failed to initialize local media or WebSockets:', e);
        sessionStatus.textContent = 'Media Permission Error';
        alert('Please allow camera & microphone permissions to join the 1-on-1 session.');
    }

    // 3. WebRTC Peer Connection Setup
    function createPeerConnection() {
        if (peerConnection) return;

        peerConnection = new RTCPeerConnection(rtcConfig);

        // Add local tracks to WebRTC peer connection
        if (localStream) {
            localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, localStream);
            });
        }

        // Handle remote media track arrival
        peerConnection.ontrack = (event) => {
            console.log('Remote track received:', event.streams[0]);
            remoteVideo.srcObject = event.streams[0];
            videoPlaceholder.classList.add('hidden');
            sessionStatus.textContent = 'Live Session Active 🟢';
        };

        // Handle ICE candidate generation
        peerConnection.onicecandidate = (event) => {
            if (event.candidate && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'ice_candidate',
                    candidate: event.candidate
                }));
            }
        };

        peerConnection.oniceconnectionstatechange = () => {
            console.log('ICE Connection State:', peerConnection.iceConnectionState);
            if (peerConnection.iceConnectionState === 'disconnected' || peerConnection.iceConnectionState === 'failed') {
                videoPlaceholder.classList.remove('hidden');
                sessionStatus.textContent = 'Connection Interrupted';
            }
        };
    }

    // 4. Load AI Expert Briefing Dossier
    async function loadAIBriefing() {
        try {
            const storedData = localStorage.getItem('latest_analysis');
            let payload = {};
            if (storedData) {
                payload = JSON.parse(storedData);
            }

            const briefing = await apiClient.post(`/api/v1/expert/briefing/${roomId}`, payload);
            console.log('AI Briefing Loaded:', briefing);

            document.getElementById('briefing-candidate-name').textContent = briefing.candidate_name;
            document.getElementById('briefing-target-role').textContent = `Target Role: ${briefing.latest_job_title}`;
            document.getElementById('briefing-score-badge').textContent = `Match: ${Math.round(briefing.overall_match_score)}%`;

            // Render matched skills
            const matchedContainer = document.getElementById('briefing-matched-skills');
            if (briefing.matched_skills && briefing.matched_skills.length) {
                matchedContainer.innerHTML = briefing.matched_skills.map(s => 
                    `<span class="px-2.5 py-1 bg-teal-950/60 border border-teal-500/40 text-teal-300 rounded-lg text-[11px] font-semibold">${s}</span>`
                ).join('');
            } else {
                matchedContainer.innerHTML = '<span class="text-xs text-slate-500">None recorded</span>';
            }

            // Render missing skills
            const missingContainer = document.getElementById('briefing-missing-skills');
            if (briefing.missing_skills && briefing.missing_skills.length) {
                missingContainer.innerHTML = briefing.missing_skills.map(s => 
                    `<span class="px-2.5 py-1 bg-rose-950/60 border border-rose-500/40 text-rose-300 rounded-lg text-[11px] font-semibold">${s}</span>`
                ).join('');
            } else {
                missingContainer.innerHTML = '<span class="text-xs text-slate-500">None detected</span>';
            }

            // Render discussion points
            const agendaContainer = document.getElementById('briefing-discussion-points');
            if (briefing.key_discussion_points && briefing.key_discussion_points.length) {
                agendaContainer.innerHTML = briefing.key_discussion_points.map(pt => 
                    `<li class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-700/60 leading-relaxed text-slate-300">• ${pt}</li>`
                ).join('');
            }

        } catch (e) {
            console.error('Error fetching AI briefing dossier:', e);
        }
    }

    loadAIBriefing();

    // 5. In-Call Chat & UI Event Controls
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'chat_message',
                sender: 'You',
                text: text
            }));
            renderChatMessage('You', text, true);
            chatInput.value = '';
        }
    });

    function renderChatMessage(sender, text, isSelf) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `flex flex-col ${isSelf ? 'items-end' : 'items-start'}`;
        msgDiv.innerHTML = `
            <span class="text-[10px] font-bold ${isSelf ? 'text-violet-400' : 'text-slate-400'} mb-0.5">${sender}</span>
            <div class="${isSelf ? 'bg-violet-600 text-white' : 'bg-slate-700 text-slate-200'} text-xs py-2 px-3 rounded-2xl max-w-[85%] leading-relaxed shadow">
                ${escapeHtml(text)}
            </div>
        `;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHtml(text) {
        return text.replace(/[&<>"']/g, function(m) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
        });
    }

    // Audio & Video Toggles
    toggleMicBtn.addEventListener('click', () => {
        if (!localStream) return;
        isAudioMuted = !isAudioMuted;
        localStream.getAudioTracks().forEach(t => t.enabled = !isAudioMuted);
        toggleMicBtn.classList.toggle('bg-rose-600', isAudioMuted);
        toggleMicBtn.classList.toggle('bg-slate-700', !isAudioMuted);
    });

    toggleCamBtn.addEventListener('click', () => {
        if (!localStream) return;
        isVideoMuted = !isVideoMuted;
        localStream.getVideoTracks().forEach(t => t.enabled = !isVideoMuted);
        toggleCamBtn.classList.toggle('bg-rose-600', isVideoMuted);
        toggleCamBtn.classList.toggle('bg-slate-700', !isVideoMuted);
    });

    // Tab Switching
    tabBriefingBtn.addEventListener('click', () => {
        tabBriefingBtn.classList.add('text-violet-400', 'border-violet-500');
        tabBriefingBtn.classList.remove('text-slate-400', 'border-transparent');
        tabChatBtn.classList.remove('text-violet-400', 'border-violet-500');
        tabChatBtn.classList.add('text-slate-400', 'border-transparent');

        tabBriefingContent.classList.remove('hidden');
        tabChatContent.classList.add('hidden');
        tabChatContent.classList.remove('flex');
    });

    tabChatBtn.addEventListener('click', () => {
        tabChatBtn.classList.add('text-violet-400', 'border-violet-500');
        tabChatBtn.classList.remove('text-slate-400', 'border-transparent');
        tabBriefingBtn.classList.remove('text-violet-400', 'border-violet-500');
        tabBriefingBtn.classList.add('text-slate-400', 'border-transparent');

        tabBriefingContent.classList.add('hidden');
        tabChatContent.classList.remove('hidden');
        tabChatContent.classList.add('flex');
    });

    // End Call Buttons
    const handleHangup = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'hangup' }));
        }
        if (peerConnection) {
            peerConnection.close();
        }
        if (localStream) {
            localStream.getTracks().forEach(t => t.stop());
        }
        window.location.href = 'dashboard.html';
    };

    endCallTopBtn.addEventListener('click', handleHangup);
    endCallMainBtn.addEventListener('click', handleHangup);
});
