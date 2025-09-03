import cpu
import gpu
import ram
import argparse

CPUName = cpu.GetCPUName()
CPUTemp = cpu.hwmon_GetCPUTemp()

GPUName = gpu.GetGPUName()
GPUTemp = gpu.hwmon_GetGPUTemp()

RamTotal = ram.total_ram()
RamAvailable = ram.available_ram()
RamUsed = ram.used_ram()

parser = argparse.ArgumentParser(description='SHM - Server Health Monitor for automated information and alert handling.')
parser.add_argument('-c', '--cpu', help='Shows cpu information', action='store_true')
parser.add_argument('-g', '--gpu', help='Shows gpu information', action='store_true')
parser.add_argument('-r', '--ram', help='Shows ram information', action='store_true')
parser.add_argument('-a', '--all', help='Shows cpu, gpu and ram information', action='store_true')
args = parser.parse_args()

CPU_ARG = args.cpu
GPU_ARG = args.gpu
RAM_ARG = args.ram
ALL_ARG = args.all

if not (CPU_ARG or GPU_ARG or RAM_ARG or ALL_ARG):
    print(f'''
          << CPU information >>
          CPU-Name: {str(CPUName)}
          CPU-Temp: {str(CPUTemp)} °C

          << GPU information >>
          GPU-Name: {str(GPUName)}
          GPU-Temp: {str(GPUTemp)} °C

          << RAM information >>
          Ram-Total: {str(RamTotal)} GB
          Ram-Available: {str(RamAvailable)} GB
          Ram-Used: {str(RamUsed)} GB
          ''')

if (CPU_ARG):
    print(f'''
          << CPU information >>
          CPU-Name: {str(CPUName)}
          CPU-Temp: {str(CPUTemp)} °C
          ''')

if (GPU_ARG):
    print(f'''
          << GPU information >>
          GPU-Name: {str(GPUName)}
          GPU-Temp: {str(GPUTemp)} °C
          ''')

if (RAM_ARG):
    print(f'''
          << RAM information >>
          Ram-Total: {str(RamTotal)} GB
          Ram-Available: {str(RamAvailable)} GB
          Ram-Used: {str(RamUsed)} GB
          ''')

if (ALL_ARG):
    print(f'''
          << CPU information >>
          CPU-Name: {str(CPUName)}
          CPU-Temp: {str(CPUTemp)} °C

          << GPU information >>
          GPU-Name: {str(GPUName)}
          GPU-Temp: {str(GPUTemp)} °C

          << RAM information >>
          Ram-Total: {str(RamTotal)} GB
          Ram-Available: {str(RamAvailable)} GB
          Ram-Used: {str(RamUsed)} GB
          ''')
