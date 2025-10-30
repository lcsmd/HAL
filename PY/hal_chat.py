# hal_chat.py
# Small CLI for issuing agent ops quickly.

import os, sys, json, argparse, requests

HOST = os.environ.get("HAL_AGENT_HOST", "127.0.0.1")
PORT = int(os.environ.get("HAL_AGENT_PORT", "8766"))
TOKEN = os.environ.get("HAL_AGENT_TOKEN", "CHANGEME-STRONG-TOKEN")
BASE = f"http://{HOST}:{PORT}"

def _h(): return {"X-Auth": TOKEN}

def do_list(p): print(json.dumps(requests.get(f"{BASE}/list", headers=_h(), params={"path": p}).json(), indent=2))
def do_read(f): print(requests.get(f"{BASE}/read", headers=_h(), params={"file": f}).text)
def do_write(f, content): print(requests.post(f"{BASE}/write", headers=_h(), json={"path": f, "content": content}).json())
def do_run(cmd): print(json.dumps(requests.post(f"{BASE}/run", headers=_h(), json={"cmd": cmd}).json(), indent=2))
def do_qm(cmd): print(json.dumps(requests.post(f"{BASE}/qm/exec", headers=_h(), json={"cmd": cmd}).json(), indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="op", required=True)
    s1 = sub.add_parser("list"); s1.add_argument("path")
    s2 = sub.add_parser("read"); s2.add_argument("file")
    s3 = sub.add_parser("write"); s3.add_argument("file"); s3.add_argument("text")
    s4 = sub.add_parser("run"); s4.add_argument("cmd")
    s5 = sub.add_parser("qm");  s5.add_argument("cmd")
    args = ap.parse_args()
    if args.op == "list": do_list(args.path)
    elif args.op == "read": do_read(args.file)
    elif args.op == "write": do_write(args.file, args.text)
    elif args.op == "run": do_run(args.cmd)
    elif args.op == "qm": do_qm(args.cmd)

