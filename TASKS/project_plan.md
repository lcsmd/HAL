# QM BASED ASSISTANT  Task Plan (v1)

## 0. Bootstrap
- [ ] Create `PY\hal_agent.py` and run local agent
- [ ] Set env: `HAL_ROOT`, `HAL_AGENT_TOKEN`
- [ ] Smoke test `/health`, `/list`, `/read`, `/write`, `/run`, `/qm/exec`
- [ ] Start `NOTES\progress.md` logging

## 1. Schema + EQU Foundation

- [x] Create directories: `SCHEMA`, `BP`, `EQU`
- [x] Define workflow and dependency rules
- [x] Fix syntax errors in `BUILD.SCHEMA`
  - [x] Replace `READ.FILE()` with proper `READSEQ` line reader
  - [x] Ensure `DCOUNT` uses @FM, not @AM
  - [x] Add missing `END` statements
  - [x] Ensure FOR/NEXT loops match variable scope
- [x] Test EQU file creation
- [x] Create BP QM file and populate with programs
- [x] Compile BUILD.SCHEMA using QMClient Python API
- [x] Execute BUILD.SCHEMA - created 18 files with DICT entries
- [ ] Implement `SYNC.SCHEMA` (compare schema.csv vs QM files)
- [ ] Implement `OPEN.FILES` (populates `COMMON FILES()`)
- [ ] Add logging of schema operations to `LOG\SCHEMA.LOG`
- [ ] Resolve con.equ issue (Windows reserved word)
- [ ] Investigate MODEL file creation error

## 2. Core assistant loop
- [ ] `BP\ASSISTANT.CORE` read input  log  call LLM  write output
- [ ] `PY\llm_router.py` minimal: route all to `https://ollama.lcs.ai`
- [ ] Store sessions in `SESSION` file
- [ ] Program tests: round-trip latency, failure handling

## 3. Personas
- [ ] `PERSONAS` file + DICT + `EQU\psn.equ`
- [ ] Fields: NAME, WAKEWORD, MODEL, VOICE, GENERAL.DOMAIN, PRIVATE.DOMAIN
- [ ] `BP\ROUTER.PERSONA` select persona by wake word or arg
- [ ] Separate memory files per persona

## 4. Voice I/O via WebSockets
- [ ] Implement `WS` listener in QM for chat and voice control envelopes
- [ ] `PY\voice_engine.py` TTS baseline (local)
- [ ] Wake-word service integration (OpenWakeWord/Porcupine)
- [ ] Streaming path: LLM text  TTS  WS binary frames

## 5. Home Assistant
- [ ] `PY\home_link.py` REST + optional WS for HA
- [ ] QM wrapper `HA.SEND.CMD` to call Python
- [ ] Tests: toggle entities, query sensor state

## 6. Context memory
- [ ] Summarize old messages to keep prompt small
- [ ] `BP\MEMORY.SYNC` for domain merges
- [ ] Retrieval: `BP\FIND.MEMORY`

## 7. External LLMs
- [ ] `LLM.MODELS` file (name, endpoint, key, temp, maxtokens)
- [ ] Router rules per persona
- [ ] Benchmarks

## 8. Distributed presence
- [ ] Broadcast TTS to HA media players
- [ ] Open-WebUI connector for chat persona switch
- [ ] Mobile shortcut endpoints

## 9. Self-extension
- [ ] Voice-driven schema/task changes  write to `DEV.CHANGES`
- [ ] Approval flow  regenerate EQU/DICT


