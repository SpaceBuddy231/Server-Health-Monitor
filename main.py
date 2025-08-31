import cpu
import gpu
import ram

CPUName = cpu.GetCPUName()
CPUTemp = cpu.hwmon_GetCPUTemp()
GPUName = gpu.GetGPUName()
GPUTemp = gpu.hwmon_GetGPUTemp()
RamTotal = ram.TotalRam()
RamAvailable = ram.AvailableRam()
RamUsed = ram.UsedRam()


print('\nCPUName: ' + CPUName + '\nCPUTemp: ' + str(CPUTemp))

print('\nGPUName: ' + str(GPUName) + '\nGPUTemp: ' + str(GPUTemp))

print('\nRamTotal: ' + str(RamTotal) + '\nRamAvailable: ' + str(RamAvailable) + '\nRamUsed: ' + str(RamUsed) + '\n')
