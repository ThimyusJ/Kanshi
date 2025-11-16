import subprocess
from typing import Optional
from rich.console import Console

console = Console()

def memory_script():
    cmd = "free -m"
    mem = {}

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if line.startswith("Mem:"):
                _, total, used, free, shared, buff_cache, available = line.split()
                mem["total"] = int(total)
                mem["used"] = int(used)
                mem["free"] = int(free)

        free_memory = round((mem['free']/mem['total']) * 100)

        if result.stdout:
            console.print(f"[cyan]Total Memory: {mem['total']} MB[/cyan]")
            console.print(f"[yellow]Memory Used: {mem['used']} MB {round((mem['used']/mem['total']) * 100)}%[/yellow]")
            console.print(f"[green]Memory Remaining: {mem['free']} MB {free_memory}%[/green]")
            if free_memory < 10:
                console.print(f"[red]Low Memory[/red]")
        if result.stderr:
            console.print(f"[red]{result.stderr}[/red]")
    except Exception as e:
        console.print(f"[red]Error exxecuting command: [/red] {e}")



def handle_intent(intent: str, user_input: Optional[str] = None):
    if intent == "memory script":
        #Return the function to be executed by the router
        return memory_script

    console.print(f"[yellow]Unknown intent[/yellow] {intent}")
    return None