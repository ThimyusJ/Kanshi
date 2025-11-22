import typer
from rich.console import Console
from core import intents
from core import router
from typing import Mapping, Any

app = typer.Typer(help="Kanshi - CLI system monitoring agent for Linux")
console = Console()

def render_result(result: Mapping[str, Any]):
    """
    Pretty-print a command result dict using Rich, so the CLI
    stays nice even though our commands are now API-friendly.
    """
    if result is None:
        console.print("[red]No result returned[/red]")
        return

    ok = bool(result.get("ok", False))
    stdout = (result.get("stdout") or "").strip()
    stderr = (result.get("stderr") or "").strip()
    meta = result.get("meta") or {}

    
    cmd = meta.get("command")
    desc = meta.get("desc")
    if cmd or desc:
        header = desc or cmd
        console.print(f"[bold magenta]{header}[/bold magenta]")
        if cmd and desc:
            console.print(f"[dim]$ {cmd}[/dim]")

    # Body
    if stdout:
        console.print(stdout)

    if stderr:
        style = "red" if not ok else "yellow"
        console.print(f"[{style}]{stderr}[/{style}]")

    if not stdout and not stderr and not meta:
        # Fallback: show raw result for debugging
        console.print(result)



@app.command()
def start():
    console.print("[bold blue]Kanshi online. Type 'exit' to quit.[/bold blue]")
    while True:
        try: 
            user_input = input("> ").strip()

            if not user_input: continue
            if user_input.lower() in {"exit", "quit"}:
                console.print("[bold red]Shutting Down...[/bold red]"); break
            
            
            intent = intents.parse_intent(user_input)
            result = router.route(intent, user_input=user_input)
            render_result(result)
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Interrupted. Shutting Down...[/bold red]"); break
        except Exception as e:
            console.print(f"[red]Error[/red] {e}")

@app.command()
def run(command: str = typer.Argument(..., help="One Shot command, e.g. get OS info")):
    intent = intents.parse_intent(command)
    result = router.route(intent, user_input=command)
    render_result(result)

if __name__ == "__main__":
    app()
