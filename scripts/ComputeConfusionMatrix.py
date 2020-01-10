import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command, execute_command

arcpy.AddMessage('\nCompute Confusion Matrix')
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
log_file = os.path.join(log_folder, 'COMPUTECONFUSIONMATRIX' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_image = arcpy.GetParameterAsText(0)
input_ref_image = arcpy.GetParameterAsText(1)
input_value_for_nodata = arcpy.GetParameterAsText(2)
input_ram = arcpy.GetParameterAsText(3)
output_matrix_output = arcpy.GetParameterAsText(4)

# Generate OTB commands
command_list = []

# Generate command for input classified image
otb_input_train_shp = generate_command('-in ', True, input_image, False)
command_list.append(otb_input_train_shp)

# Generate command for truth type
otb_input_truth_type = generate_command('-ref ', False, 'raster', False)
command_list.append(otb_input_truth_type)

# Generate command for input ref image
otb_input_ref_image = generate_command('-ref.raster.in ', True, input_ref_image, False)
command_list.append(otb_input_ref_image)

# Generate command for value for nodata pixels
otb_input_value_for_nodata = generate_command('-ref.raster.nodata ', False, input_value_for_nodata, False)
command_list.append(otb_input_value_for_nodata)

# Generate command for matrix output
otb_output_matrix_output = generate_command('-out ', False, output_matrix_output, False)
command_list.append(otb_output_matrix_output)

# Generate full command for OTB
otb_write_output = execute_command('otbcli_ComputeConfusionMatrix ', command_list, workspace, otb_dir)

# Save command to log
with open(log_file, 'w') as f:
    f.write('Compute Confusion Matrix Log')
    f.write('Timestamp: {}'.format(ts))
    f.write('Input image: {}'.format(input_image))
    f.write('OTB Command: {}'.format(otb_write_output))

