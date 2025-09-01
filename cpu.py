import subprocess
import os

# Get all CPU information
cpu_raw = subprocess.run(['lscpu'], stdout=subprocess.PIPE)  # cpu_raw is a 'CompletedProcess' object that cannot be accessed using string functions

# Decode the bytes from the 'CompletedProcess' object to a normal string
cpu_raw = cpu_raw.stdout.decode('utf-8')


def thermal_GetCPUTemp():
    thermal_path = '/sys/class/thermal/'

    thermal_cpu_directory = None

    # Check if the directory exists
    if (os.path.isdir(thermal_path)):
        # List all subdirectories of '/sys/class/thermal/' and return them as an array
        array_thermal_dir = os.listdir(thermal_path)

        for i in range(len(array_thermal_dir)):
            if not array_thermal_dir[i].startswith('thermal_zone'):
                continue
            # Start: Find the path with the CPU type in it
            directory = os.path.join(thermal_path, array_thermal_dir[i], 'type')

            # Search for the file that contains the CPU type name
            try:
                with open(directory, 'r') as namefile:
                    content = namefile.read()
                    if any(cputype in content for cputype in ('pkg', 'cpu', 'core', 'acpitz', 'cpu-therm', 'cpu_thermal', 'soc')):
                        thermal_cpu_directory = os.path.dirname(directory)  # This is the directory that contains all CPU temperature information
                        if not (os.path.isdir(thermal_cpu_directory)):
                            return 'The directory defined for "thermal_cpu_directory" is not a directory.'
                        break
            except (FileNotFoundError, OSError):
                continue

    # Get all files and directories in the directory that contains all CPU temperature information
    if thermal_cpu_directory is None:
        return 'Could not find any thermal_zone.'
    try:
        array_cpu_dir = os.listdir(thermal_cpu_directory)
    except UnboundLocalError:
        return 'Could not find any thermal_zone.'

    temperature = None
    # Get temperature from the temp file
    for i in range(len(array_cpu_dir)):
        if ('temp' == array_cpu_dir[i]):
            with open(os.path.join(thermal_cpu_directory, array_cpu_dir[i]), 'r') as namefile:
                temperature = namefile.read()

    try:
        temperature = int(temperature.strip())/1000
    except AttributeError:
        return 'Could not calculate the temperature (thermal_GetCPUTemp). Temperature string is propably empty.'
    return int(temperature)


def hwmon_GetCPUTemp():
    # Linux: There are two directories that contain temperature information about the CPU: '/sys/class/thermal/thermal_zone/' and '/sys/class/hwmon/'

    # This will be the directory that holds all CPU temperature information
    # the hwmon path should be the same on every Linux system that uses hwmon
    hwmon_path = '/sys/class/hwmon/'

    # Check if the directory exists
    if (os.path.isdir(hwmon_path)):
        # List all subdirectories of '/sys/class/hwmon/' and return them as an array
        array_hwmon_dir = os.listdir(hwmon_path)

        for i in range(len(array_hwmon_dir)):
            # Start: Find the path with the CPU name in it
            directory = os.path.join(hwmon_path, array_hwmon_dir[i], 'name')

            # Search for the file that contains the CPU type name
            try:
                with open(directory, 'r') as namefile:
                    content = namefile.read()
                    if 'k10temp' in content or 'coretemp' in content:
                        hwmon_cpu_directory = directory[0:len(directory)-len(array_hwmon_dir[i])+1]  # This is the directory that contains all CPU temperature information
                        break
            # If there is no file with a normal CPU indicator the program will try to use the '/sys/class/thermal/' directory as a fallback
            except FileNotFoundError:
                thermal_GetCPUTemp()

    # Get all files and directories in the directory that contains all CPU temperature information
    array_cpu_dir = os.listdir(hwmon_cpu_directory)
    _removing_list = []  # This array will save all unnecessary items that need to be removed from 'array_cpu_dir'

    # Save every unnecessary file (every directory or file that is not named tempX_input, where X represents a number) into the '_removing_list' array
    for i in range(len(array_cpu_dir)):
        if not ('temp' in array_cpu_dir[i] and 'input' in array_cpu_dir[i]):
            _removing_list.append(array_cpu_dir[i])

    # Remove unnecessary files and directories from 'array_cpu_dir' to have a clean and usable array of all important files for temperature calculation
    for i in range(len(_removing_list)):
        array_cpu_dir.remove(_removing_list[i])

    # Array where the different temperature rates of the different sensors are saved in
    temperature = []
    # Get every temperature value and save it into the temperature array
    for i in range(len(array_cpu_dir)):
        with open(os.path.join(hwmon_cpu_directory,  array_cpu_dir[i]), 'r') as namefile:
            temperature.append(namefile.read().strip())

    temperature_average = 0
    equation = '0'
    divisor = 0
    # Calculate the average value of every measured temperature in the temperature array
    for i in range(len(temperature)):
        equation = equation + '+' + str(temperature[i])
        divisor = len(temperature)

    temperature_average = (eval(equation)/divisor)/1000  # Final average temperature value of every sensor
    return int(temperature_average)


def GetCPUName():
    # Get the position of the start and end of the model name to extract: "Model name: xxxxxxxxxx" where xxxxxxxxxx is the CPU model name
    MN_position_A = cpu_raw.find('Model name:')
    MN_position_B = cpu_raw.find('CPU family:')

    cpu_model = cpu_raw[MN_position_A+11:MN_position_B]  # String between the two positions 'MN_position_A' and 'MN_position_B'
    cpu_model = cpu_model.strip()  # Remove whitespace so we don't get something like '                  xxxxxxxxxx'

    return str(cpu_model)
