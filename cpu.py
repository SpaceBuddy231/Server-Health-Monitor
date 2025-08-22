import subprocess

# Getting every CPU Information
cpu_raw = subprocess.run(['lscpu'], stdout=subprocess.PIPE) # cpu_raw is a 'CompletedProcess' object that is not accesible by string-necessery fucntions

# Decoding the bytes from the 'CompletedProcess' Object to an normal string
cpu_raw = cpu_raw.stdout.decode('utf-8')

# Get position of the model name beginning and the end of the model name to get the following: "Model name: xxxxxxxxxx" <- xxxxxxxxxx = CPU model name
MN_position_A = cpu_raw.find('Model name:')
MN_position_B = cpu_raw.find('CPU family:')

cpu_model = cpu_raw[MN_position_A+11:MN_position_B] # String between the two positions 'MN_position_A' and 'MN_position_B'
cpu_model = cpu_model.strip() # Remove whitespace that we don't get something like '                  xxxxxxxxxx'

print(cpu_model)