import cpu
import gpu
import ram
import argparse
import curses
import time
import datetime
import os
import json
import pandas

# Configurating the arguments
parser = argparse.ArgumentParser(description='SHM - Server Health Monitor for automated information and alert handling.')
parser.add_argument('-c', '--cpu', help='Shows cpu information', action='store_true')
parser.add_argument('-g', '--gpu', help='Shows gpu information', action='store_true')
parser.add_argument('-r', '--ram', help='Shows ram information', action='store_true')
parser.add_argument('-a', '--all', help='Shows cpu, gpu and ram information', action='store_true')
parser.add_argument('-rec', '--record', type=int, help='Record the cpu, gpu and ram informatio and save it into a .json and .csv file')
args = parser.parse_args()

# Named constants for more clearance
CPU_ARG = args.cpu
GPU_ARG = args.gpu
RAM_ARG = args.ram
ALL_ARG = args.all
REC_ARG = args.record

if (type(REC_ARG) is int):
    if not (os.path.isdir('recordings')):  # Checks if the 'recordings' directory already exists, if not it creates one
        os.makedirs('recordings')
    recordings_data = []  # Final array that will be inserted into a .json + .csv file

    timestamp = datetime.datetime.now().strftime('%m-%d-%Y_%H-%M-%S')  # This timestamp will be used as an filename for the .json + .csv file

    for i in range(REC_ARG):  # For-loop that adds every seconds a new entry of every sensor into the 'json_array'

        CPUName = cpu.GetCPUName()
        CPUTemp = cpu.hwmon_GetCPUTemp()

        GPUName = gpu.GetGPUName()
        GPUTemp = gpu.hwmon_GetGPUTemp()

        RamTotal = ram.total_ram()
        RamAvailable = ram.available_ram()
        RamUsed = ram.used_ram()

        temp_array = {}
        sensor_reading = {  # This 'sensor_reading' is one entry of every sensor
            'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'CPU_Temperature': str(CPUTemp),
            'GPU_Temperature': str(GPUTemp),
            'RAM_Total': str(RamTotal),
            'RAM_Available': str(RamAvailable),
            'RAM_Used': str(RamUsed)
        }
        recordings_data.append(sensor_reading)
        time.sleep(1)  # Every second

    file_timestamp = datetime.datetime.now().strftime('%m-%d-%Y_%H-%M-%S')  # file_timestamp (other timestamp than the timestamp in the 'sensor_reading')
    json_file_path = os.path.join('recordings', file_timestamp + '.json')  # Filepath for the .json file
    csv_file_path = os.path.join('recordings', file_timestamp + '.csv')  # Filepath for the .csv file

    with open(json_file_path, 'w') as json_file:
        json.dump(recordings_data, fp=json_file, indent=2,)  # Saves 'recordings_data' into the a freshly created .json file

    #  This DataFrame will be for the .csv saving because the .json formatting is not as readable as the DataFrame
    df = pandas.DataFrame(recordings_data)

    #  Final step -> Creating a .csv file
    df.to_csv(csv_file_path, index=False)

    print(f'Saved recording in {json_file_path} and {csv_file_path}.')
    exit()


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
            stdscr.addstr(f'CPU-Name: {str(CPUName)}\n')
            stdscr.addstr(f'CPU-Temp: {str(CPUTemp)} °C\n')

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f'GPU-Name: {str(GPUName)}\n')
            stdscr.addstr(f'GPU-Temp: {str(GPUTemp)} °C\n')

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f'Ram-Total: {str(RamTotal)} GB\n')
            stdscr.addstr(f'Ram-Available: {str(RamAvailable)} GB\n')
            stdscr.addstr(f'Ram-Used: {str(RamUsed)} GB\n')

        # Output when cpu arg was given
        if (CPU_ARG):

            CPUName = cpu.GetCPUName()
            CPUTemp = cpu.hwmon_GetCPUTemp()

            stdscr.clear()
            stdscr.addstr('\n<< CPU information >>\n')
            stdscr.addstr(f'CPU-Name: {str(CPUName)}\n')
            stdscr.addstr(f'CPU-Temp: {str(CPUTemp)} °C\n')

        # Output when gpu arg was given
        if (GPU_ARG):

            GPUName = gpu.GetGPUName()
            GPUTemp = gpu.hwmon_GetGPUTemp()

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f'GPU-Name: {str(GPUName)}\n')
            stdscr.addstr(f'GPU-Temp: {str(GPUTemp)} °C\n')

        # Output when ram arg was given
        if (RAM_ARG):

            RamTotal = ram.total_ram()
            RamAvailable = ram.available_ram()
            RamUsed = ram.used_ram()

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f'Ram-Total: {str(RamTotal)} GB\n')
            stdscr.addstr(f'Ram-Available: {str(RamAvailable)} GB\n')
            stdscr.addstr(f'Ram-Used: {str(RamUsed)} GB\n')

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
            stdscr.addstr(f'CPU-Name: {str(CPUName)}\n')
            stdscr.addstr(f'CPU-Temp: {str(CPUTemp)} °C\n')

            stdscr.addstr('\n<< GPU information >>\n')
            stdscr.addstr(f'GPU-Name: {str(GPUName)}\n')
            stdscr.addstr(f'GPU-Temp: {str(GPUTemp)} °C\n')

            stdscr.addstr('\n<< RAM information >>\n')
            stdscr.addstr(f'Ram-Total: {str(RamTotal)} GB\n')
            stdscr.addstr(f'Ram-Available: {str(RamAvailable)} GB\n')
            stdscr.addstr(f'Ram-Used: {str(RamUsed)} GB\n')

        stdscr.addstr('\n\nPress "Q" to exit...')
        stdscr.refresh()

    while True:
        update_display()

        key = stdscr.getch()
        if key == ord('q'):
            break

        time.sleep(0.3)


curses.wrapper(output)
