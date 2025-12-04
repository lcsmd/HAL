# HAL Web Voice Client - TODO List

## CRITICAL - Must Fix Before Production

### 1. WebSocket Connection Issues ⚠️ **HIGH PRIORITY**

**Problem:** Browser connects briefly then disconnects in a loop

**Symptoms:**
- Status shows "Connecting..." → "Connected!" → "Disconnected" repeatedly
- Text input doesn't work (no response when typing)
- Microphone button does nothing
- HAProxy logs show requests going to `fallback_backend` instead of `hal2_backend`

**Diagnosis:**
- ✅ HAProxy configuration added: ACL `is_hal2` and routing `use_backend hal2_backend`
- ✅ Backend servers running: Port 8080 (HTTP) and Port 8768 (WebSocket)
- ✅ SSL certificate working (wildcard *.lcs.ai)
- ❌ WebSocket upgrade detection may not be working correctly
- ❌ Browser-side error handling needs investigation

**Next Steps:**
1. Check browser console for JavaScript errors
2. Verify WebSocket handshake is completing
3. Test WebSocket connection directly (wscat or similar)
4. Review HAProxy WebSocket routing logic
5. Add debug logging to Voice Gateway to see if connections are received
6. Check if browser is sending correct Upgrade headers

**Files to Check:**
- `/etc/haproxy/haproxy.cfg` - Backend hal2_backend section
- `voice_assistant_v2/web_client/client.js` - WebSocket connection logic
- `PY/voice_gateway_web.py` - Connection handling

---

### 2. Wake Word Detection Not Triggering

**Problem:** Saying "Hey Jarvis" doesn't trigger any response

**Possible Causes:**
- WebSocket not connected (primary issue - fix #1 first)
- Audio not streaming from browser to server
- Server-side wake word model not detecting properly
- Audio format mismatch (client sends wrong sample rate/format)

**Next Steps:**
1. First fix WebSocket connection issue (#1)
2. Add logging to show when audio chunks are received
3. Verify audio format: 16kHz, mono, int16
4. Test wake word detection threshold (currently 0.5)
5. Add visual feedback when audio is being streamed

---

### 3. Text Input Not Responding

**Problem:** Typing text and pressing Enter gives no response

**Root Cause:** Same as #1 - WebSocket not properly connected

**Verification:**
- Check if `send_message()` is being called
- Check if WebSocket `readyState` is OPEN
- Verify message format matches server expectations

---

## HIGH PRIORITY - Core Functionality

### 4. Implement Proper Error Handling

**Client-Side:**
- [ ] Show clear error messages to user
- [ ] Retry connection with exponential backoff
- [ ] Detect microphone permission denied
- [ ] Handle network disconnections gracefully
- [ ] Show loading states during processing

**Server-Side:**
- [ ] Log all errors with stack traces
- [ ] Send error messages to client
- [ ] Implement graceful shutdown
- [ ] Handle concurrent connection limits

### 5. Add Visual Feedback

- [ ] Show when audio is streaming (animated mic icon)
- [ ] Display transcription in real-time
- [ ] Show "HAL is thinking..." during processing
- [ ] Add sound effects (wake word detected, response ready)
- [ ] Progress indicator for long-running queries

### 6. Session Management

- [ ] Persist conversation history in session
- [ ] Implement session timeout (1 hour)
- [ ] Clear old sessions from memory
- [ ] Allow user to clear history
- [ ] Resume session on reconnect

---

## MEDIUM PRIORITY - Improvements

### 7. Auto-Start Services

**Windows Server:**
- [ ] Create Windows Service for Voice Gateway
- [ ] Create Windows Service for HTTP Server
- [ ] Set to auto-start on boot
- [ ] Add restart on failure

**Ubuntu Server:**
- [X] Whisper service already configured
- [X] Ollama service already configured
- [ ] Verify services start on boot

### 8. Monitoring & Logging

- [ ] Implement structured logging
- [ ] Add performance metrics (latency, success rate)
- [ ] Create monitoring dashboard
- [ ] Set up alerts for service failures
- [ ] Log query analytics (popular queries, errors)

### 9. Testing Suite

- [ ] Unit tests for query router
- [ ] Integration tests for voice pipeline
- [ ] Browser compatibility tests (Chrome, Firefox, Safari, Edge)
- [ ] Mobile device testing (iOS, Android)
- [ ] Load testing (concurrent users)
- [ ] End-to-end automated tests

### 10. Documentation

- [X] Architecture documentation (WEB_VOICE_CLIENT_ARCHITECTURE.md)
- [ ] API documentation
- [ ] Deployment guide
- [ ] User manual
- [ ] Troubleshooting guide (expand existing)
- [ ] Video tutorial

---

## LOW PRIORITY - Nice to Have

### 11. Authentication & Authorization

- [ ] Add user login system
- [ ] OAuth integration (Google, Microsoft)
- [ ] API key authentication
- [ ] Role-based access control
- [ ] Usage quotas per user

### 12. Enhanced Features

**Text-to-Speech:**
- [ ] Add TTS for voice responses
- [ ] Use ElevenLabs or similar for natural voices
- [ ] Allow user to choose voice
- [ ] Cache TTS responses

**Multi-Language Support:**
- [ ] Detect input language
- [ ] Support multiple Whisper models
- [ ] Translate responses if needed
- [ ] UI localization

**Advanced Voice Features:**
- [ ] Multiple wake word options ("Hey HAL", "Computer", etc.)
- [ ] Custom wake word training
- [ ] Continuous conversation mode (no wake word after first)
- [ ] Voice cloning for responses

### 13. Mobile App

- [ ] React Native wrapper for web client
- [ ] Native iOS app
- [ ] Native Android app
- [ ] Push notifications
- [ ] Offline mode with cached responses

### 14. Integration Enhancements

**Home Assistant:**
- [ ] Add more device types
- [ ] Scene control
- [ ] Automation triggers
- [ ] Status queries

**Database:**
- [ ] Natural language to SQL
- [ ] Visual query builder
- [ ] Export results to CSV/JSON
- [ ] Scheduled reports

**LLM:**
- [ ] Support multiple LLM providers
- [ ] Model switching per query type
- [ ] Fine-tuned models for specific domains
- [ ] RAG (Retrieval-Augmented Generation) with knowledge base

### 15. UI/UX Improvements

- [ ] Dark mode toggle
- [ ] Customizable themes
- [ ] Keyboard shortcuts
- [ ] Voice commands for UI (close, minimize, etc.)
- [ ] Desktop notifications
- [ ] Floating widget mode

### 16. Performance Optimization

- [ ] Implement audio compression before streaming
- [ ] WebSocket message batching
- [ ] Response caching for common queries
- [ ] Lazy loading for components
- [ ] Service worker for offline functionality

### 17. Advanced Analytics

- [ ] User behavior tracking
- [ ] Query success/failure rates
- [ ] Average response times
- [ ] Popular features usage
- [ ] Error patterns analysis

---

## BACKLOG - Future Ideas

### 18. Plugin System

- [ ] Define plugin API
- [ ] Plugin marketplace
- [ ] Custom handlers
- [ ] Third-party integrations
- [ ] Community contributions

### 19. Multi-User Collaboration

- [ ] Shared sessions
- [ ] User presence indicators
- [ ] Collaborative queries
- [ ] Team workspaces

### 20. Advanced AI Features

- [ ] Context-aware responses
- [ ] Personality customization
- [ ] Emotion detection in voice
- [ ] Proactive suggestions
- [ ] Learning from user corrections

---

## Completed ✅

- [X] Create web-based client (HTML/JS)
- [X] Implement WebSocket communication
- [X] Add server-side wake word detection
- [X] Integrate with Whisper STT
- [X] Integrate with Ollama LLM
- [X] Configure HAProxy reverse proxy
- [X] Add SSL certificate (wildcard *.lcs.ai)
- [X] Implement query routing system
- [X] Create beautiful UI
- [X] Add microphone capture
- [X] Stream audio to server
- [X] Detect wake word on server
- [X] Transcribe audio with Whisper
- [X] Route queries intelligently
- [X] Display responses in chat UI

---

## Known Issues

### Issue #1: WebSocket Connection Unstable
**Priority:** CRITICAL
**Status:** Investigating
**Assignee:** Droid
**Created:** 2025-12-03
**Last Updated:** 2025-12-03

**Description:**
Browser connects to wss://hal2.lcs.ai but connection doesn't stay stable. Client.js shows connect/disconnect loop.

**Reproduction:**
1. Open https://hal2.lcs.ai
2. Observe status indicator
3. Try typing text - no response

**Environment:**
- Browser: Chrome/Edge (Windows)
- Server: Windows Server 2022
- HAProxy: Version 2.8.5 (Ubuntu)

**Logs:**
- HAProxy shows requests going to fallback_backend
- Voice Gateway shows no connections received
- Browser console needs checking

**Related:**
- Issue #2 (Wake word)
- Issue #3 (Text input)

### Issue #2: Wake Word Not Detecting
**Priority:** HIGH
**Status:** Blocked by Issue #1
**Assignee:** Droid
**Created:** 2025-12-03

**Description:**
Saying "Hey Jarvis" with microphone button pressed doesn't trigger any response.

**Likely Cause:**
WebSocket not connected, so audio isn't reaching server.

**Next Steps:**
1. Fix Issue #1 first
2. Then test wake word detection

### Issue #3: Text Input No Response
**Priority:** HIGH
**Status:** Blocked by Issue #1
**Assignee:** Droid
**Created:** 2025-12-03

**Description:**
Typing text and pressing Enter/Send button gives no response.

**Likely Cause:**
WebSocket not properly connected.

---

## Testing Checklist

### Before Production Release

**Functionality:**
- [ ] Text queries work consistently
- [ ] Voice queries work consistently
- [ ] Wake word detects reliably
- [ ] Multiple users can connect
- [ ] Sessions are isolated
- [ ] Responses are accurate
- [ ] Error messages are clear

**Performance:**
- [ ] Response time < 5 seconds (voice)
- [ ] Response time < 1 second (text)
- [ ] No memory leaks
- [ ] Handles 10+ concurrent users
- [ ] Graceful degradation under load

**Security:**
- [ ] SSL certificate valid
- [ ] No sensitive data exposed
- [ ] Input validation in place
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Rate limiting works

**Compatibility:**
- [ ] Chrome (Windows)
- [ ] Edge (Windows)
- [ ] Firefox (Windows)
- [ ] Safari (Mac)
- [ ] Chrome (Mac)
- [ ] Safari (iOS)
- [ ] Chrome (Android)

**Reliability:**
- [ ] Survives server restart
- [ ] Reconnects after network loss
- [ ] Handles malformed input
- [ ] Recovers from errors
- [ ] No crashes in 24-hour test

---

## Timeline Estimate

**CRITICAL Issues (Must Fix First):**
- WebSocket connection: 2-4 hours
- Wake word detection: 1-2 hours (after WebSocket fixed)
- Text input: 0 hours (fixed automatically with WebSocket)

**HIGH PRIORITY:**
- Error handling: 4-6 hours
- Visual feedback: 2-3 hours
- Session management: 3-4 hours

**MEDIUM PRIORITY:**
- Auto-start services: 2-3 hours
- Monitoring: 4-6 hours
- Testing suite: 8-12 hours
- Documentation: 4-6 hours

**Total to MVP:** ~20-30 hours
**Total to Production:** ~40-60 hours
**Total for all features:** ~100-200 hours

---

## Resources Needed

**Development:**
- Browser dev tools
- WebSocket testing tools (wscat, Postman)
- Load testing tools (Apache Bench, Artillery)

**Deployment:**
- Windows Server (10.1.34.103) ✅
- Ubuntu Server (10.1.10.20) ✅
- HAProxy server (ubu6) ✅
- Domain name (hal2.lcs.ai) ✅
- SSL certificate (wildcard *.lcs.ai) ✅

**Documentation:**
- Architecture diagrams
- Sequence diagrams
- User flows
- API documentation

---

## Notes

- Web-based approach is the RIGHT solution - don't revert to Python client
- Focus on fixing WebSocket connection issue FIRST
- All other issues likely stem from connection problem
- HAProxy configuration looks correct but may need tweaking
- Server-side processing is working (tested directly)
- Browser audio capture works (tested)
- Issue is in the communication layer between browser and server

---

**Last Updated:** 2025-12-03 19:50 PST
**Next Review:** After fixing WebSocket connection issue
