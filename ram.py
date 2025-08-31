import os

meminfo_raw = '/proc/meminfo'


class GetRam:
    def __init__(self):

        if not (os.path.isfile(meminfo_raw)):  # Checks if the file that is saved in the 'meminfo_raw' exists -> if not the function resturns a string =>
            return 'Could not find the memory info in the "/proc/meminfo" path.'

        content = None
        # Read the 'meminfo' file and save it into the content var
        with open(meminfo_raw, 'r') as f:
            content = f.read()

        if not isinstance(content, str) or len(content) < 5:  # If the content could not be defined by the with open() function the system return a string =>
            return 'The "meminfo" file in "/proc/meminfo" is corrupted.'
        self.content = content

    def TotalRam(self):
        # Process to get the total RAM
        MemTotal_Line = ''
        MemTotal_Line = next((line for line in self.content.splitlines() if 'MemTotal:' in line), None)
        MemTotal = MemTotal_Line.split(':')[1].strip().split(' ')[0]
        MemTotal_Result = f'{(int(MemTotal)/1000000):.2f}'
        print(MemTotal_Result)

        return MemTotal_Result

    def AvailableRam(self):
        # Process to get the available RAM
        MemAvailable_Line = ''
        MemAvailable_Line = next((line for line in self.content.splitlines() if 'MemAvailable' in line), None)
        MemAvailable = MemAvailable_Line.split(':')[1].strip().split(' ')[0]
        MemAvailable_Result = f'{(int(MemAvailable)/1000000):.2f}'
        print(MemAvailable_Result)

        return MemAvailable_Result

    def UsedRam(self):
        # Process to get the used RAM
        MemUsed = float(self.TotalRam()) - float(self.AvailableRam())
        MemUsed_Result = f'{(int(MemUsed)):.2f}'
        print(MemUsed_Result)

        return MemUsed_Result


ram = GetRam()


def TotalRam():
    return ram.TotalRam()


def AvailableRam():
    return ram.AvailableRam()


def UsedRam():
    return ram.UsedRam()
