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