import typer
from rich.console import Console

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
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Interrupted. Shutting Down...[/bold red]"); break
        except Exception as e:
            console.print(f"[red]Error[/red] {e}")

@app.command()
def run(command: str = typer.Argument(..., help="One Shot command, e.g. get OS info")):
    pass

if __name__ == "__main__":
    app()