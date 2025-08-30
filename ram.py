import os

meminfo_raw = '/proc/meminfo'


def GetRamUsage():
    if not (os.path.isfile(meminfo_raw)):  # Checks if the file that is saved in the 'meminfo_raw' exists -> if not the function resturns a string =>
        return 'Could not find the memory info in the "/proc/meminfo" path.'

    content = None
    # Read the 'meminfo' file and save it into the content var
    with open(meminfo_raw, 'r') as f:
        content = f.read()

    if not isinstance(content, str) or len(content) < 5:  # If the content could not be defined by the with open() function the system return a string =>
        return 'The "meminfo" file in "/proc/meminfo" is corrupted.'

    print(content.splitlines())  # Later use


GetRamUsage()
