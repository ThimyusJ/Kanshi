from typing import Optional, Dict

def parse_intent(user_input):
    text = (user_input or "").strip()
    lower = text.lower()


    if "free" in lower: intent = "memory script"

    else:
         intent = user_input

    return intent
