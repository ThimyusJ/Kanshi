import typer
from rich.console import Console
from core import intents
from core import router

app = typer.Typer(help="Kanshi - CLI system monitoring agent for Linux")
console = Console()

@app.command()
def start():
    console.print("[bold blue]Kanshi online. Type 'exit' to quit.[/bold blue]")
    while True:
        try: 
            user_input = input("> ").strip()

            if not user_input: continue
            if user_input.lower() in {"exit", "quit"}:
                console.print("[bold red]Shutting Down...[/bold red]"); break
            
            payload = intents.parse_intent(user_input)
            router.route(payload)
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Interrupted. Shutting Down...[/bold red]"); break
        except Exception as e:
            console.print(f"[red]Error[/red] {e}")

@app.command()
def run(command: str = typer.Argument(..., help="One Shot command, e.g. get OS info")):
    payload = intents.parse_intent(command)

    router.route(payload)

if __name__ == "__main__":
    app()