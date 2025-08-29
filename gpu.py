import subprocess
import os


def GetGPUName():
    gpu_raw = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True) # gpu_raw saves some information about the GPU among them is the name of the GPU

    vga_line = [line for line in gpu_raw.stdout.split('\n')
                if 'vga' in line.lower()] # This is the vga line that it from the gpu_raw output

    potential_gpu_name = ["GeForce", "RTX", "GTX", "TITAN", "Quadro", "Tesla", "NVS", "Radeon", "RX", "HD", "R9", "R7", "R5", "Pro", "FirePro"] # List of potential GPU names that could be listed in the vga line

    match = next((name for name in potential_gpu_name if name in vga_line[0]), None) # Find the first matching GPU name from the potential_gpu_name list in the vga_line

    gpu_name_position = vga_line[0].find(match) # Find the position of the GPU name in the vga_line

    _gpu_name_plus_trash = [vga_line[0][gpu_name_position:-1].split(']')] # This array contains the GPU name and some trash (not necessery characters after the GPU name)

    gpu_name = _gpu_name_plus_trash[0][0].strip() # This isolates the GPU name from the trash

    return gpu_name

def thermal_GetGPUTemp():
    thermal_path = '/sys/class/thermal/'

    thermal_gpu_directory = None

     # Check if the directory exists
    if (os.path.isdir(thermal_path)):
        # List all subdirectories of '/sys/class/thermal/' and return them as an array
        array_thermal_dir = os.listdir(thermal_path)

        for i in range(len(array_thermal_dir)):
            if not array_thermal_dir[i].startswith('thermal_zone'):
                continue
            # Start: Find the path with the gpu type in it
            directory = os.path.join(thermal_path, array_thermal_dir[i], 'type')

            # Search for the file that contains the gpu type name
            try:
                with open(directory, 'r') as namefile:
                    content = namefile.read()
                    if any(gputype in content for gputype in ('gpu-thermal', 'GPU-therm', 'g3d-thermal')):
                            thermal_gpu_directory = os.path.dirname(directory)  # This is the directory that contains all gpu temperature information
                            if not (os.path.isdir(thermal_gpu_directory)):
                                return 'The directory defined for "thermal_gpu_directory" is not a directory.'
                            break
            except: continue

    # Get all files and directories in the directory that contains all gpu temperature information
    if thermal_gpu_directory is None:
        return 'Could not find any thermal_zone'
    try: array_gpu_dir = os.listdir(thermal_gpu_directory)
    except UnboundLocalError: return 'Could not find any thermal_zone'

    temperature = None
    # Get temperature from the temp file
    for i in range(len(array_gpu_dir)):
        if ('temp' == array_gpu_dir[i]):
            with open(os.path.join(thermal_gpu_directory, array_gpu_dir[i]), 'r') as namefile:
                temperature = namefile.read()

    try: temperature = int(temperature.strip())/1000
    except AttributeError: return 'Could not calculate the temperature (thermal_GetgpuTemp). Temperature string is propably empty.'
    return int(temperature)

def hwmon_GetGPUTemp():
    hwmon_path = '/sys/class/hwmon/'

    if (os.path.isdir(hwmon_path)):
        # List all subdirectories of '/sys/class/hwmon/' and return them as an array
        array_hwmon_dir = os.listdir(hwmon_path)

        for i in range(len(array_hwmon_dir)):
            # Start: Find the path with the GPU name in it
            directory = os.path.join(hwmon_path, array_hwmon_dir[i], 'name')

            # Search for the file that contains the GPU type name
            try:
                with open(directory, 'r') as namefile:
                    content = namefile.read()
                    if 'amdgpu' in content or 'radeon' in content or 'nouveau' in content or 'iGPU' in content or 'dGPU' in content or 'i915' in content or 'xe' in content:
                        hwmon_gpu_directory = directory[0:len(directory)-len(array_hwmon_dir[i])+1]  # This is the directory that contains all GPU temperature information
                        break
            # If there is no file with a normal gpu indicator the program will try to use the '/sys/class/thermal/' directory as a fallback
            except FileNotFoundError:
                thermal_GetGPUTemp()

    # Get all files and directories in the directory that contains all gpu temperature information
    array_gpu_dir = os.listdir(hwmon_gpu_directory)
    _removing_list = []  # This array will save all unnecessary items that need to be removed from 'array_gpu_dir'

    # Save every unnecessary file (every directory or file that is not named tempX_input, where X represents a number) into the '_removing_list' array
    for i in range(len(array_gpu_dir)):
        if not ('temp' in array_gpu_dir[i] and 'input' in array_gpu_dir[i]):
            _removing_list.append(array_gpu_dir[i])

    # Remove unnecessary files and directories from 'array_gpu_dir' to have a clean and usable array of all important files for temperature calculation
    for i in range(len(_removing_list)):
        array_gpu_dir.remove(_removing_list[i])

    # Array where the different temperature rates of the different sensors are saved in
    temperature = []
    # Get every temperature value and save it into the temperature array
    for i in range(len(array_gpu_dir)):
        with open(os.path.join(hwmon_gpu_directory,  array_gpu_dir[i]), 'r') as namefile:
            temperature.append(namefile.read().strip())

    temperature_average = 0
    equation = '0'
    divisor = 0
    # Calculate the average value of every measured temperature in the temperature array
    for i in range(len(temperature)):
        equation = equation + '+' + str(temperature[i])
        divisor = len(temperature)

    temperature_average = (eval(equation)/divisor)/1000 # Final average temperature value of every sensor
    return int(temperature_average)
