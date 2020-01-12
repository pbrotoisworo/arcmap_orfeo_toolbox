import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command, execute_command

arcpy.AddMessage('\nUnsupervised KMeans Classification')
arcpy.AddMessage('Orfeo Toolbox\n')

# Detect workspace, set up initial parameters
workspace = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(os.path.dirname(workspace), 'logs')
scratch_folder = os.path.join(workspace, 'scratch')
arcpy.env.overwriteOutput = True

# Set logging parameters
ts = datetime.now()
ts = ts.strftime("%Y-%m-%d %H:%M:%S")
ts_file_append = ts.replace('-', '')
ts_file_append = ts_file_append.replace(':', '')
ts_file_append = ts_file_append.replace(' ', '_')
log_file = os.path.join(log_folder, 'MULTIVARIATECD' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_before_image = arcpy.GetParameterAsText(0)
input_after_image = arcpy.GetParameterAsText(1)
input_ram = arcpy.GetParameterAsText(2)
output_change_map = arcpy.GetParameterAsText(3)

# Generate OTB commands
command_list = []

# Generate command for input image (before)
otb_input_before_image = generate_command('-in ', True, input_before_image, False)
command_list.append(otb_input_before_image)

# Generate command for input image (after)
otb_input_after_image = generate_command('-in1 ', True, input_after_image, False)
command_list.append(otb_input_after_image)

# Generate command for ram usage
otb_input_ram = generate_command('-in2 ', False, input_ram, False)
command_list.append(otb_input_ram)

# Generate command for output change map
otb_output_change_map = generate_command('-out ', True, output_change_map, False)
command_list.append(otb_output_change_map)

# Generate full command for OTB
otb_write_output = execute_command('otbcli_MultivariateAlterationDetector ', command_list, workspace, otb_dir)

# Save command to log
with open(log_file, 'w') as f:
    f.write('Multivariate Alteration Detector Log')
    f.write('\nTimestamp: {}'.format(ts))
    f.write('\nInput Before Image: {}'.format(input_before_image))
    f.write('\nInput After Image: {}'.format(input_after_image))
    f.write('\nInput RAM Limit: {}'.format(input_ram))
    f.write('\nOutput Change Map: {}'.format(output_change_map))
    f.write('\nOTB Command : {}'.format(otb_write_output))
