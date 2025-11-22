from typing import Optional, Dict, Any
from commands import basic_commands


def route(intent: str, user_input: Optional[str] = None) -> Dict[str, Any]:
    """
    Core routing layer for Kanshi.

    - Looks up the function for a given intent.
    - Executes it.
    - Always returns a result dict the caller (CLI/API) can use.
    """
    command_fn = basic_commands.handle_intent(intent, user_input=user_input)

    if callable(command_fn):
        
        return command_fn()

   
    return {
        "ok": False,
        "stdout": "",
        "stderr": f"Unknown intent: {intent}",
        "meta": {
            "intent": intent,
            "source": "router",
        },
    }
