import os, sys, time, subprocess, win32serviceutil, win32service, win32event, logging

SERVICE_NAME = "HALAgent"
DISPLAY_NAME = "HAL Local Agent"
DESCRIPTION = "Local API bridge between OpenQM and external AI services."

HAL_ROOT = r"C:\QMSYS\HAL"
PYTHON_EXE = r"C:\Python313\python.exe"
AGENT_SCRIPT = os.path.join(HAL_ROOT, "PY", "hal_agent.py")
LOG_FILE = os.path.join(HAL_ROOT, "PY", "hal_agent_service.log")
REQ_FILE = os.path.join(HAL_ROOT, "PY", "requirements.txt")

FALLBACK_PACKAGES = [
    "fastapi", "uvicorn", "pydantic", "requests",
    "typing-extensions", "typing-inspection",
    "anyio", "sniffio", "h11"
]

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HALService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = DISPLAY_NAME
    _svc_description_ = DESCRIPTION

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.proc = None
        self.stop_requested = False

    def SvcStop(self):
        logging.info("Service stop requested.")
        self.stop_requested = True
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            time.sleep(2)
            if self.proc.poll() is None:
                self.proc.kill()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        logging.info("Service stopped.")

    def SvcDoRun(self):
        logging.info(f"Service starting  Python={PYTHON_EXE}, Script={AGENT_SCRIPT}")
        self.main_loop()

    def ensure_dependencies(self):
        """Install required packages using requirements.txt or fallback list."""
        try:
            if os.path.exists(REQ_FILE):
                logging.info("Installing from requirements.txt...")
                subprocess.run([PYTHON_EXE, "-m", "pip", "install", "-r", REQ_FILE],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            else:
                logging.warning("requirements.txt missing  installing fallback packages...")
                subprocess.run([PYTHON_EXE, "-m", "pip", "install"] + FALLBACK_PACKAGES,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            logging.info("Dependency installation complete.")
        except Exception as e:
            logging.error(f"Dependency installation failed: {e}")

    def main_loop(self):
        backoff = 5
        while not self.stop_requested:
            try:
                self.proc = subprocess.Popen(
                    [PYTHON_EXE, AGENT_SCRIPT],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(AGENT_SCRIPT),
                    text=True
                )
                logging.info("HAL Agent subprocess started.")
                for line in self.proc.stdout:
                    logging.info("[HAL] " + line.strip())
                exit_code = self.proc.wait()
                logging.warning(f"HAL Agent exited with code {exit_code}")
            except Exception as e:
                logging.error(f"HAL Agent crashed: {e}")

            if self.stop_requested:
                break

            # Check logs for missing module errors
            try:
                with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as log:
                    last_lines = log.readlines()[-30:]
                    if any("ModuleNotFoundError" in line for line in last_lines):
                        logging.info("Missing module detected  running self-repair.")
                        self.ensure_dependencies()
                        backoff = 5
                        continue
            except Exception as e:
                logging.error(f"Error reading log for dependency check: {e}")

            backoff = min(backoff * 2, 300)
            logging.info(f"Restarting HAL Agent in {backoff}s...")
            time.sleep(backoff)

if __name__ == "__main__":
    import servicemanager
    servicemanager.Initialize()
    win32serviceutil.HandleCommandLine(HALService)

