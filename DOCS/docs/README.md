# HAL Assistance Stack — Revision 4

Minimal, low‑latency voice interface with a single wake word (**HAL**, fallback **computer**). 
Audio → `UBUAI` (GPU Faster‑Whisper) → `OpenQM` routing → LLM/HA/internal → text reply → TTS on `UBUAI` → audio back to client.

## Components
- **Client (macOS)**: Wake‑word detection (OpenWakeWord), ack tone, VAD with ~3 s silence cutoff, WS send to UBUAI.
- **UBUAI (FastAPI)**: `/transcribe` WS for audio, `/route` WS to OpenQM, `/speak` TTS (ElevenLabs primary → pyttsx3 fallback).
- **OpenQM**: WS listener at `ws://10.1.34.103:8765/route` that accepts `{session_id, text, wakeword}` and returns `{text, voice}`.

## Hosts/Ports
- UBUAI: `10.1.10.20:8001` (WS/HTTP)
- OpenQM: `10.1.34.103:8765` (WS)
- Proxy (optional): `hal.lcs.ai` → `10.1.50.100`

## Voice
- Default voice: **Bryan** (ElevenLabs voice ID configurable).

## Flow
1. Wake word **HAL** detected → play ack tone; begin recording.
2. Record until ~3 s silence. Send PCM to `ws://10.1.10.20:8001/transcribe`.
3. UBUAI transcribes with Faster‑Whisper (GPU) and forwards text to OpenQM over WS.
4. OpenQM routes to LLM, HA, or internal logic. Returns `{text, voice?}`.
5. UBUAI `/speak` synthesizes speech (ElevenLabs; fallback pyttsx3), streams back to client.
