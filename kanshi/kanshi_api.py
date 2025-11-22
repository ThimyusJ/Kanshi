# kanshi_api.py

from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel

from core import intents       
from core import router as kanshi_router

router = APIRouter(
    prefix="/api/agents/kanshi",
    tags=["kanshi"],
)


class CommandRequest(BaseModel):
    input: str
    type: str = "nlp"
    metadata: Dict[str, Any] = {}


@router.post("/command")
async def send_command(cmd: CommandRequest):
    """
    Web entrypoint for Kanshi.

    - Frontend sends raw text in `input`.
    - We run it through the same intent + route pipeline as the CLI.
    - We return the normalized result dict plus the resolved intent.
    """
    intent = intents.parse_intent(cmd.input)
    result = kanshi_router.route(intent, user_input=cmd.input) or {}

    return {
        "intent": intent,
        "input": cmd.input,
        "type": cmd.type,
        "metadata": cmd.metadata,
        **result,
    }
