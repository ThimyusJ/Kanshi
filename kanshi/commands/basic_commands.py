import subprocess
from typing import Optional, Dict, Any


def _run_shell(cmd: str) -> Dict[str, Any]:
    """
    Helper to run a shell command and normalize the result into a
    common structure that both CLI and API can use.
    """
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )

    return {
        "ok": result.returncode == 0,
        "stdout": (result.stdout or "").strip(),
        "stderr": (result.stderr or "").strip(),
        "meta": {
            "command": cmd,
            "returncode": result.returncode,
        },
    }


def memory_script() -> Dict[str, Any]:
    """
    Show memory usage using `free -m` and attach a parsed summary
    in the `meta` field.
    """
    cmd = "free -m"
    base = _run_shell(cmd)

    parsed = {}
    try:
        lines = base["stdout"].splitlines()
        for line in lines:
            if line.startswith("Mem:"):
                _, total, used, free, *_ = line.split()
                total_i = int(total)
                used_i = int(used)
                free_i = int(free)
                free_pct = round((free_i / total_i) * 100, 1) if total_i else 0.0
                parsed = {
                    "total_mb": total_i,
                    "used_mb": used_i,
                    "free_mb": free_i,
                    "free_pct": free_pct,
                }
                break
    except Exception as exc:  
        base.setdefault("meta", {})["parse_error"] = str(exc)

    base["meta"]["parsed_memory"] = parsed
    return base


def cpu_info() -> Dict[str, Any]:
    """
    Basic CPU info. You can swap this for lscpu /proc parsing later.
    """
    
    cmd = "command -v lscpu >/dev/null 2>&1 && lscpu || grep -m1 'model name' /proc/cpuinfo"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "CPU information"
    return base


def disk_usage() -> Dict[str, Any]:
    cmd = "df -h"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "Disk usage (df -h)"
    return base


def uptime() -> Dict[str, Any]:
    cmd = "uptime"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "System uptime"
    return base


def running_processes() -> Dict[str, Any]:
    
    cmd = "ps aux --sort=-%mem | head -n 15"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "Top processes by memory"
    return base


def network_info() -> Dict[str, Any]:
    
    cmd = "command -v ip >/dev/null 2>&1 && ip a || ifconfig"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "Network interfaces"
    return base


def ping_test() -> Dict[str, Any]:
    
    cmd = "ping -c 4 8.8.8.8"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "Ping test to 8.8.8.8"
    return base


def os_info() -> Dict[str, Any]:
    cmd = "uname -a"
    base = _run_shell(cmd)
    base["meta"]["desc"] = "OS / kernel information"
    return base


def handle_intent(intent: str, user_input: Optional[str] = None):
    """
    Map an intent string to the underlying command function.
    Returns a callable, or None if we don't know this intent.
    """
    table = {
        "memory script": memory_script,
        "cpu info": cpu_info,
        "disk usage": disk_usage,
        "uptime": uptime,
        "process list": running_processes,
        "network info": network_info,
        "ping test": ping_test,
        "os info": os_info,
    }

    fn = table.get(intent)
    return fn
