import cpu
import gpu

CPUName = cpu.GetCPUName()
CPUTemp = cpu.hwmon_GetCPUTemp()
GPUName = gpu.GetGPUName()
GPUTemp = gpu.hwmon_GetGPUTemp()

print('\nCPUName: ' + CPUName + '\nCPUTemp: ' + str(CPUTemp) + '\n\nGPUName: ' + str(GPUName) + '\nGPUTemp: ' + str(GPUTemp))