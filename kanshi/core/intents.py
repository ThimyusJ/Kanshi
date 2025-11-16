from typing import Optional, Dict

def parse_intent(user_input):
    text = (user_input or "").strip()
    lower = text.lower()


    
    if "free" in text or "memory" in text:
        return "memory script"
    if "cpu" in text or "load" in text:
        return "cpu info"
    if "disk" in text or "storage" in text:
        return "disk usage"
    if "uptime" in text:
        return "uptime"
    if "process" in text or "ps" in text:
        return "process list"
    if "network" in text or "ip" in text:
        return "network info"
    if "ping" in text:
        return "ping test"
    if "os" in text or "kernel" in text or "version" in text:
        return "os info"

    else:
         intent = user_input

    return intent
