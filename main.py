from subprocess import run
from time import localtime

import psutil

# Widget: time, cpu, memory, battery
WIDGET_ORDER = [
    "time",
    "cpu",
    "memory",
    "battery",
]
SEPARATOR = " | "

def get_time():  # Time
    now = localtime()
    return f"Time {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}"


def cpu_load():
    return f"Cpu {psutil.cpu_percent(interval=0.2)}%"


def memory_usage():
    return f"Mem {psutil.virtual_memory().percent}%"


def battery():
    battery = psutil.sensors_battery()
    return (
        f"Charging {battery.percent:0.0f}"
        if battery.power_plugged
        else f"Bat {battery.percent:0.0f}%"
    )


WIDGET_HANDLERS = {
    "time": get_time,
    "cpu": cpu_load,
    "memory": memory_usage,
    "battery": battery,
}

def metric():
    return SEPARATOR.join(
        WIDGET_HANDLERS[widget]()
        for widget in WIDGET_ORDER
        if widget in WIDGET_HANDLERS
    )


while True:
    run(["xsetroot", "-name", f"{metric()}"])
