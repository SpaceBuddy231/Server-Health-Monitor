import os

meminfo_raw = '/proc/meminfo'


class GetRam:
    def __init__(self):

        try:
            if not (os.path.isfile(meminfo_raw)):  # Checks if the file that is saved in the 'meminfo_raw' exists -> if not the function resturns a string =>
                return 'Could not find the memory info in the "/proc/meminfo" path.'
        finally:
            pass

        content = None
        try:
            # Read the 'meminfo' file and save it into the content var
            with open(meminfo_raw, 'r') as f:
                content = f.read()
        except (FileNotFoundError, OSError):
            return 'Could not read the "meminfo" file in "/proc/meminfo".'

        if not isinstance(content, str) or len(content) < 5:  # If the content could not be defined by the with open() function the system return a string =>
            return 'The "meminfo" file in "/proc/meminfo" is corrupted.'
        self.content = content

    def total_ram(self):
        # Process to get the total RAM
        mem_total_line = ''
        mem_total_line = next((line for line in self.content.splitlines() if 'MemTotal:' in line), None)
        mem_total = mem_total_line.split(':')[1].strip().split(' ')[0]
        mem_total_result = f'{(int(mem_total)/1000000):.2f}'

        return mem_total_result

    def available_ram(self):
        # Process to get the available RAM
        mem_available_line = ''
        mem_available_line = next((line for line in self.content.splitlines() if 'MemAvailable' in line), None)
        mem_available = mem_available_line.split(':')[1].strip().split(' ')[0]
        mem_available_result = f'{(int(mem_available)/1000000):.2f}'

        return mem_available_result

    def used_ram(self):
        # Process to get the used RAM
        mem_used = float(self.total_ram()) - float(self.available_ram())
        mem_used_result = f'{(int(mem_used)):.2f}'

        return mem_used_result


ram = GetRam()


def total_ram():
    return ram.total_ram()


def available_ram():
    return ram.available_ram()


def used_ram():
    return ram.used_ram()
