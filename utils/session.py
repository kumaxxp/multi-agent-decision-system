import uuid, time, json, pathlib

class SessionLogger:
    def __init__(self, root="sessions"):
        self.root = pathlib.Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.session_id = time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
        (self.root/self.session_id).mkdir(parents=True, exist_ok=True)

    def save_step(self, n:int, obj:dict):
        p = self.root/self.session_id/f"step_{n:03d}.json"
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)
