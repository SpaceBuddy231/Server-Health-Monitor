import cpu
import gpu

CPUName = cpu.GetCPUName()
CPUTemp = cpu.hwmon_GetCPUTemp()
GPUName = gpu.GetGPUName()

print('\nCPUName: ' + CPUName + '\nCPUTemp: ' + str(CPUTemp) + '\n\nGPUName: ' + str(GPUName))