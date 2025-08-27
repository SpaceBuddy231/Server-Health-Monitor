import cpu

CPUName = cpu.GetCPUName()
CPUTemp = cpu.hwmon_GetCPUTemp()

print('CPUName: ' + CPUName + '\nCPUTemp: ' + str(CPUTemp))