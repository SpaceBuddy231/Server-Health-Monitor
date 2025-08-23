import subprocess
import os

# Getting every CPU Information
cpu_raw = subprocess.run(['lscpu'], stdout=subprocess.PIPE) # cpu_raw is a 'CompletedProcess' object that is not accesible by string-necessery fucntions

# Decoding the bytes from the 'CompletedProcess' Object to an normal string
cpu_raw = cpu_raw.stdout.decode('utf-8')

def GetCPUTemp():
    # Linux >> There are 2 directorys that is containing temperture information about the cpu '/sys/class/thermal/thermal_zone/' and '/sys/class/hwmon/'
    # hwmon way
    # hwmon path should be the same on every linux system that is using hwmon
    hwmon_path = '/sys/class/hwmon/'
    # Check if the directory is exsiting
    if (os.path.isdir(hwmon_path)):
        # lists every subdirectorys of '/sys/class/hwmon/' and returns them as a array
        array_hwmon_dir = os.listdir(hwmon_path)

        for i in range(len(array_hwmon_dir)):
            # Starting > Find the path with the cpu name in it< procedure
            directory = os.path.join(hwmon_path, array_hwmon_dir[i], 'name')
            
            with open(directory, 'r') as namefile:
                content = namefile.read()

def GetCPUName():
    # Get position of the model name beginning and the end of the model name to get the following: "Model name: xxxxxxxxxx" <- xxxxxxxxxx = CPU model name
    MN_position_A = cpu_raw.find('Model name:')
    MN_position_B = cpu_raw.find('CPU family:')

    cpu_model = cpu_raw[MN_position_A+11:MN_position_B] # String between the two positions 'MN_position_A' and 'MN_position_B'
    cpu_model = cpu_model.strip() # Remove whitespace that we don't get something like '                  xxxxxxxxxx'
    
    return cpu_model

GetCPUTemp()