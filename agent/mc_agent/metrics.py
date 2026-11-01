from pathlib import Path


def sample():
    cpu_line = Path("/proc/stat").read_text().splitlines()[0].split()
    values = [int(value) for value in cpu_line[1:]]
    if cpu_line[0] != "cpu" or len(values) < 4:
        raise ValueError("Invalid /proc/stat")
    total = sum(values[:8])
    idle = values[3] + (values[4] if len(values) > 4 else 0)
    memory = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, _, value = line.partition(":")
        if key in ("MemTotal", "MemAvailable"):
            memory[key] = int(value.split()[0]) * 1024
    return total, idle, memory["MemTotal"], memory["MemAvailable"]


def cpu_percent(previous, current):
    total = current[0] - previous[0]
    idle = current[1] - previous[1]
    if total <= 0 or idle < 0:
        return None
    return round(max(0.0, min(100.0, (total - idle) * 100 / total)), 1)
