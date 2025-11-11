import os, time, asyncio, json, yaml, sys
import numpy as np, sounddevice as sd, webrtcvad, websockets, simpleaudio as sa
from dotenv import load_dotenv

# Optional: OpenWakeWord for true wake-word; fallback to Enter if not available
USE_WAKEWORD = True
try:
    from openwakeword import Model as OWWModel
except Exception:
    USE_WAKEWORD = False

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
cfg = yaml.safe_load(open(CONFIG_PATH))

UBUAI_WS = cfg["endpoints"]["ubuai_ws"]
SR = int(cfg["audio"]["sample_rate"])
PAUSE_SECS = float(cfg["audio"]["pause_secs"])
WAKE_PRIMARY = cfg["wakewords"]["primary"]
WAKE_FALLBACK = cfg["wakewords"]["fallback"]
TONE_PATH = cfg["tone"]

def play_tone():
    try:
        wave_obj = sa.WaveObject.from_wave_file(TONE_PATH); wave_obj.play().wait_done()
    except Exception as e:
        print("Ack tone error:", e, file=sys.stderr)

def record_until_silence():
    vad = webrtcvad.Vad(2)
    buf = bytearray()
    last_voice = time.time()
    chunk = int(SR * 0.02)  # 20ms
    stream = sd.InputStream(samplerate=SR, channels=1, dtype='int16')
    with stream:
        while True:
            data, _ = stream.read(chunk)
            pcm = data.tobytes()
            buf.extend(pcm)
            if vad.is_speech(pcm, SR): last_voice = time.time()
            if time.time() - last_voice >= PAUSE_SECS: break
    return bytes(buf)

async def send_to_ubuai(audio_bytes: bytes):
    async with websockets.connect(UBUAI_WS, max_size=None) as ws:
        await ws.send(audio_bytes)
        await ws.send(b"\x00\x00stop")
        # Optionally read small ack
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=0.3)
            if isinstance(msg, (bytes, bytearray)): print("[UBUAI] binary", len(msg))
            else: print("[UBUAI]", msg)
        except asyncio.TimeoutError:
            pass

def wakeword_loop():
    if not USE_WAKEWORD:
        input(f'Press Enter then speak "{WAKE_PRIMARY}"...')
        return True
    model = OWWModel(wake_words=[WAKE_PRIMARY, WAKE_FALLBACK])
    chunk_size = 512  # ~32ms at 16k mono
    with sd.InputStream(samplerate=SR, channels=1, dtype='int16', blocksize=chunk_size) as stream:
        print(f"Listening for '{WAKE_PRIMARY}' (fallback '{WAKE_FALLBACK}')...")
        while True:
            audio, _ = stream.read(chunk_size)
            scores = model.predict(audio.flatten().astype(np.float32) / 32768.0)
            # scores is dict {wakeword: prob}
            if scores.get(WAKE_PRIMARY, 0) > 0.5 or scores.get(WAKE_FALLBACK, 0) > 0.6:
                return True

async def main():
    while True:
        if wakeword_loop():
            play_tone()
            audio = record_until_silence()
            print(f"Captured {len(audio)//2} samples; sending.")
            await send_to_ubuai(audio)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting.")
