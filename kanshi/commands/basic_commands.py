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

def os_info():
    result = subprocess.run("uname -a", shell=True, capture_output=True, text=True)
    console.print(result.stdout)


def ping_test():
    result = subprocess.run("ping -c 4 google.com", shell=True, capture_output=True, text=True)
    console.print(result.stdout)


def network_info():
    result = subprocess.run("ip a", shell=True, capture_output=True, text=True)
    console.print(result.stdout)


def running_processes():
    result = subprocess.run("ps -eo pid,cmd,%cpu,%mem --sort=-%cpu | head", 
                            shell=True, capture_output=True, text=True)
    console.print(result.stdout)


def uptime():
    result = subprocess.run("uptime -p", shell=True, capture_output=True, text=True)
    console.print(f"[cyan]System Uptime:[/cyan] {result.stdout}")


def disk_usage():
    result = subprocess.run("df -h", shell=True, capture_output=True, text=True)
    console.print(result.stdout)


def cpu_usage():
    result = subprocess.run("top -bn1 | grep 'Cpu(s)'", shell=True,
                            capture_output=True, text=True)
    console.print(result.stdout)


def cpu_info():
    result = subprocess.run("lscpu", shell=True, capture_output=True, text=True)
    console.print(result.stdout)




def handle_intent(intent: str, user_input: Optional[str] = None):
    if intent == "memory script": return memory_script
    if intent == "cpu info": return cpu_info
    if intent == "disk usage": return disk_usage
    if intent == "uptime": return uptime
    if intent == "process list": return running_processes
    if intent == "network info": return network_info
    if intent == "ping test": return ping_test
    if intent == "os info": return os_info

    console.print(f"[yellow]Unknown intent[/yellow] {intent}")
    return None