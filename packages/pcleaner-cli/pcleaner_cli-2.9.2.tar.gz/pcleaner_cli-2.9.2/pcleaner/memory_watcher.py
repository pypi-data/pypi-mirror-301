import threading
import time

import psutil
import torch


def memory_watcher():
    # Monitor system memory usage to warn of impending OOM errors.

    while True:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Print warnings based on RAM and swap status.
        if swap.total == 0:  # No swap available.
            if mem.percent >= 80:
                print_warning_banner(f"Warning: RAM usage has reached {round(mem.percent)}%")
        else:
            if mem.percent >= 90:
                print_warning_banner(f"Warning: RAM usage has reached {round(mem.percent)}%.")

        # Monitor VRAM if torch is available and GPU is detected.
        if torch.cuda.is_available() and torch.cuda.device_count() > 0:
            vram_total = torch.cuda.get_device_properties(0).total_memory
            vram_used = torch.cuda.memory_allocated(0)
            vram_percent = (vram_used / vram_total) * 100

            if vram_percent >= 80:
                print_warning_banner(f"Warning: VRAM usage has reached {round(vram_percent)}%")

        time.sleep(5)


def start_memory_watcher():
    watcher_thread = threading.Thread(target=memory_watcher, daemon=True)
    watcher_thread.start()


def print_warning_banner(message: str) -> None:
    trim = "=" * len(message)
    print("\n\033[91m" + trim + "\n" + message + "\n" + trim + "\033[0m\n")
