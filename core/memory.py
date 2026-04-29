from core.db import save_memory, get_memory

def update_memory(uid, msg):
    save_memory(uid, msg)

def build_context(uid):
    msgs = get_memory(uid)
    return "\n".join(msgs)