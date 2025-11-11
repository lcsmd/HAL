# Architecture

## Protocol
WebSocket for client→UBUAI and UBUAI↔OpenQM. HTTP for external TTS APIs.

## Schemas
### UBUAI → OpenQM
```json
{ "session_id": "s-001", "wakeword": "HAL", "text": "turn on the lights", "confidence": 0.94 }
```
### OpenQM → UBUAI
```json
{ "session_id": "s-001", "text": "Turning on the living room lights.", "voice": "Bryan" }
```

## Timing targets
- Wake word: 50–150 ms
- STT (GPU): 50–300 ms
- Routing + LLM: 100–800 ms
- TTS: 200–600 ms
