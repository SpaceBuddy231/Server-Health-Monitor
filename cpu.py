
import subprocess
import os

# Get all CPU information
cpu_raw = subprocess.run(['lscpu'], stdout=subprocess.PIPE) # cpu_raw is a 'CompletedProcess' object that cannot be accessed by string functions

# Decode the bytes from the 'CompletedProcess' object to a normal string
cpu_raw = cpu_raw.stdout.decode('utf-8')


def GetCPUTemp():
    # Linux: There are two directories that contain temperature information about the CPU: '/sys/class/thermal/thermal_zone/' and '/sys/class/hwmon/'

    # hwmon method
    hwmon_cpu_directory = None # Will be defined later (this will be the directory that holds all CPU temperature information)

    # hwmon path should be the same on every Linux system that uses hwmon
    hwmon_path = '/sys/class/hwmon/'

    # Check if the directory exists
    if (os.path.isdir(hwmon_path)):
        # List all subdirectories of '/sys/class/hwmon/' and return them as an array
        array_hwmon_dir = os.listdir(hwmon_path)

        for i in range(len(array_hwmon_dir)):
            # Start: Find the path with the CPU name in it
            directory = os.path.join(hwmon_path, array_hwmon_dir[i], 'name')

            # Search for the file that contains the CPU type name
            with open(directory, 'r') as namefile:
                content = namefile.read()
                if ('k10temp' in content or 'coretemp' in content):
                    hwmon_cpu_directory = directory[0:len(directory)-len(array_hwmon_dir[i])+1] # Directory that contains all CPU temperature information
                    continue

    array_cpu_dir = os.listdir(hwmon_cpu_directory) # Get all files and directories in the directory that contains all CPU temperature information
    _removing_list = [] # This array will save all directories to remove them from 'array_cpu_dir' because the goal is to only have files, not directories

    for i in range(len(array_cpu_dir)):
        if (os.path.isdir(os.path.join(hwmon_cpu_directory, array_cpu_dir[i]))):
            _removing_list.append(array_cpu_dir[i]) # '_removing_list' now contains all the names of the folders

    for i in range(len(_removing_list)):
        array_cpu_dir.remove(_removing_list[i]) # After this process all directories are removed from the 'array_cpu_dir' array and only the file names are left


def GetCPUName():
    # Get the position of the start and end of the model name to extract: "Model name: xxxxxxxxxx" where xxxxxxxxxx is the CPU model name
    MN_position_A = cpu_raw.find('Model name:')
    MN_position_B = cpu_raw.find('CPU family:')

    cpu_model = cpu_raw[MN_position_A+11:MN_position_B] # String between the two positions 'MN_position_A' and 'MN_position_B'
    cpu_model = cpu_model.strip() # Remove whitespace so we don't get something like '                  xxxxxxxxxx'

    return cpu_model

GetCPUTemp()