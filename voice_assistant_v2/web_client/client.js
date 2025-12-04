// HAL Voice Assistant Web Client

class HALClient {
    constructor() {
        this.ws = null;
        this.sessionId = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.isListening = false;
        
        // Server URL - using HAProxy reverse proxy with wildcard cert
        this.serverUrl = 'wss://hal2.lcs.ai';
        
        // DOM elements
        this.chat = document.getElementById('chat');
        this.textInput = document.getElementById('textInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.status = document.getElementById('status');
        this.voiceIndicator = document.getElementById('voiceIndicator');
        
        this.init();
    }
    
    init() {
        // Connect to server
        this.connect();
        
        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendText());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendText();
        });
        this.voiceBtn.addEventListener('click', () => this.toggleVoice());
        
        // Request microphone permissions on load
        this.requestMicrophoneAccess();
    }
    
    async requestMicrophoneAccess() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            console.log('[OK] Microphone access granted');
        } catch (err) {
            console.error('[ERROR] Microphone access denied:', err);
            this.addMessage('system', 'Microphone access denied. Voice mode unavailable.');
        }
    }
    
    connect() {
        this.updateStatus('Connecting...');
        
        this.ws = new WebSocket(this.serverUrl);
        
        this.ws.onopen = () => {
            console.log('[OK] Connected to HAL');
            this.updateStatus('Connected! Ready to chat.');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('[ERROR] WebSocket error:', error);
            this.updateStatus('Connection error');
        };
        
        this.ws.onclose = () => {
            console.log('[INFO] Disconnected');
            this.updateStatus('Disconnected. Reconnecting...');
            setTimeout(() => this.connect(), 3000);
        };
    }
    
    handleMessage(data) {
        console.log('[MSG]', data);
        
        switch (data.type) {
            case 'connected':
                this.sessionId = data.session_id;
                this.updateStatus(`Connected! Session: ${this.sessionId.substring(0, 8)}...`);
                break;
                
            case 'response':
                this.addMessage('hal', data.text);
                // Play TTS audio if available
                if (data.audio) {
                    this.playAudio(data.audio);
                }
                break;
                
            case 'processing':
                this.updateStatus('HAL is thinking...');
                break;
                
            case 'wake_word_detected':
                this.addMessage('system', '👂 Wake word detected! Listening...');
                this.voiceIndicator.textContent = '👂 Listening for command...';
                this.voiceIndicator.classList.add('active');
                break;
                
            case 'transcription':
                this.addMessage('user', `🎤 ${data.text}`);
                this.voiceIndicator.classList.remove('active');
                break;
                
            case 'error':
                this.addMessage('system', `⚠️ Error: ${data.message || 'Unknown error'}`);
                this.updateStatus('Ready');
                break;
        }
    }
    
    sendText() {
        const text = this.textInput.value.trim();
        if (!text) return;
        
        this.addMessage('user', text);
        this.textInput.value = '';
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'text_input',
                text: text,
                session_id: this.sessionId
            }));
        }
    }
    
    async toggleVoice() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }
    
    async startListening() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    channelCount: 1,
                    sampleRate: 16000,
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });
            
            this.isListening = true;
            this.voiceBtn.classList.add('listening');
            this.voiceBtn.textContent = '🔴';
            this.updateStatus('🎤 Listening for "Hey Jarvis"...');
            this.voiceIndicator.textContent = '🎤 Say "Hey Jarvis"';
            this.voiceIndicator.classList.add('active');
            
            // Create audio context for processing
            const audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            const source = audioContext.createMediaStreamSource(stream);
            const processor = audioContext.createScriptProcessor(4096, 1, 1);
            
            processor.onaudioprocess = (e) => {
                if (!this.isListening) return;
                
                const audioData = e.inputBuffer.getChannelData(0);
                const int16Array = this.float32ToInt16(audioData);
                
                // Send audio chunks to server for wake word detection
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send(JSON.stringify({
                        type: 'audio_stream',
                        audio: Array.from(int16Array),
                        session_id: this.sessionId
                    }));
                }
            };
            
            source.connect(processor);
            processor.connect(audioContext.destination);
            
            // Store for cleanup
            this.audioStream = stream;
            this.audioContext = audioContext;
            this.audioProcessor = processor;
            
        } catch (err) {
            console.error('[ERROR] Failed to start listening:', err);
            this.addMessage('system', 'Failed to access microphone');
        }
    }
    
    stopListening() {
        this.isListening = false;
        this.voiceBtn.classList.remove('listening');
        this.voiceBtn.textContent = '🎤';
        this.updateStatus('Ready');
        this.voiceIndicator.classList.remove('active');
        
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
    }
    
    float32ToInt16(float32Array) {
        const int16Array = new Int16Array(float32Array.length);
        for (let i = 0; i < float32Array.length; i++) {
            const val = Math.max(-1, Math.min(1, float32Array[i]));
            int16Array[i] = val < 0 ? val * 0x8000 : val * 0x7FFF;
        }
        return int16Array;
    }
    
    playAudio(base64Audio) {
        const audio = new Audio('data:audio/wav;base64,' + base64Audio);
        audio.play();
    }
    
    addMessage(type, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        this.chat.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chat.scrollTop = this.chat.scrollHeight;
    }
    
    updateStatus(text) {
        this.status.textContent = text;
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new HALClient();
});
