import subprocess
import os

gpu_raw = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True) # gpu_raw saves some information about the GPU among them is the name of the GPU

gpu_lines = [line for line in gpu_raw.stdout.split('\n')
             if 'vga' in line.lower()] # Later use