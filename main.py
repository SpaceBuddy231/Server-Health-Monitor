import cpu
import gpu
import ram
import argparse
import curses
import time

# Configurating the arguments
parser = argparse.ArgumentParser(description='SHM - Server Health Monitor for automated information and alert handling.')
parser.add_argument('-c', '--cpu', help='Shows cpu information', action='store_true')
parser.add_argument('-g', '--gpu', help='Shows gpu information', action='store_true')
parser.add_argument('-r', '--ram', help='Shows ram information', action='store_true')
parser.add_argument('-a', '--all', help='Shows cpu, gpu and ram information', action='store_true')
args = parser.parse_args()

# Named constants for more clearance
CPU_ARG = args.cpu
GPU_ARG = args.gpu
RAM_ARG = args.ram
ALL_ARG = args.all


def output(stdscr: curses.window):
    curses.curs_set(0)  # Sets the visibility of the curser in the CLI to invisible
    stdscr.nodelay(True)

    def update_display():

        # Output when no argument was given
        if not (CPU_ARG or GPU_ARG or RAM_ARG or ALL_ARG):

            CPUName = cpu.GetCPUName()
            CPUTemp = cpu.hwmon_GetCPUTemp()

            GPUName = gpu.GetGPUName()
            GPUTemp = gpu.hwmon_GetGPUTemp()

            RamTotal = ram.total_ram()
            RamAvailable = ram.available_ram()
            RamUsed = ram.used_ram()

            stdscr.clear()
            stdscr.addstr('\n<< CPU information >>\n')
            stdscr.addstr(f"CPU-Name: {str(CPUName)}\n")
            stdscr.addstr(f"CPU-Temp: {str(CPUTemp)} °C\n")

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f"GPU-Name: {str(GPUName)}\n")
            stdscr.addstr(f"GPU-Temp: {str(GPUTemp)} °C\n")

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f"Ram-Total: {str(RamTotal)} GB\n")
            stdscr.addstr(f"Ram-Available: {str(RamAvailable)} GB\n")
            stdscr.addstr(f"Ram-Used: {str(RamUsed)} GB\n")

        # Output when cpu arg was given
        if (CPU_ARG):

            CPUName = cpu.GetCPUName()
            CPUTemp = cpu.hwmon_GetCPUTemp()

            stdscr.clear()
            stdscr.addstr('\n<< CPU information >>\n')
            stdscr.addstr(f"CPU-Name: {str(CPUName)}\n")
            stdscr.addstr(f"CPU-Temp: {str(CPUTemp)} °C\n")

        # Output when gpu arg was given
        if (GPU_ARG):

            GPUName = gpu.GetGPUName()
            GPUTemp = gpu.hwmon_GetGPUTemp()

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f"GPU-Name: {str(GPUName)}\n")
            stdscr.addstr(f"GPU-Temp: {str(GPUTemp)} °C\n")

        # Output when ram arg was given
        if (RAM_ARG):

            RamTotal = ram.total_ram()
            RamAvailable = ram.available_ram()
            RamUsed = ram.used_ram()

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f"Ram-Total: {str(RamTotal)} GB\n")
            stdscr.addstr(f"Ram-Available: {str(RamAvailable)} GB\n")
            stdscr.addstr(f"Ram-Used: {str(RamUsed)} GB\n")

        # Output when all arg was given
        if (ALL_ARG):

            CPUName = cpu.GetCPUName()
            CPUTemp = cpu.hwmon_GetCPUTemp()

            GPUName = gpu.GetGPUName()
            GPUTemp = gpu.hwmon_GetGPUTemp()

            RamTotal = ram.total_ram()
            RamAvailable = ram.available_ram()
            RamUsed = ram.used_ram()

            stdscr.clear()
            stdscr.addstr('\n<< CPU information >>\n')
            stdscr.addstr(f"CPU-Name: {str(CPUName)}\n")
            stdscr.addstr(f"CPU-Temp: {str(CPUTemp)} °C\n")

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f"GPU-Name: {str(GPUName)}\n")
            stdscr.addstr(f"GPU-Temp: {str(GPUTemp)} °C\n")

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f"Ram-Total: {str(RamTotal)} GB\n")
            stdscr.addstr(f"Ram-Available: {str(RamAvailable)} GB\n")
            stdscr.addstr(f"Ram-Used: {str(RamUsed)} GB\n")

        stdscr.addstr('\n\nPress "Q" to exit...')
        stdscr.refresh()

    while True:
        update_display()

        key = stdscr.getch()
        if key == ord('q'):
            break

        time.sleep(0.3)


curses.wrapper(output)
