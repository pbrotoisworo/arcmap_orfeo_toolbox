import arcpy
import os
from datetime import datetime
from cl_tools import generate_command, execute_command

arcpy.AddMessage('\nCompute Images Second Order Statistics')
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
log_file = os.path.join(log_folder, 'COMPUTESTATISTICS' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_images = arcpy.GetParameterAsText(0)
input_background_value = arcpy.GetParameterAsText(1)
input_ram = arcpy.GetParameterAsText(2)
output_xml = arcpy.GetParameterAsText(3)

# Generate OTB commands
command_list = []

# Generate command for input images
otb_input_images = generate_command('-il ', True, input_images, True)
command_list.append(otb_input_images)

# Generate command for background image
otb_input_background_value = generate_command('-bv ', False, input_background_value, False)
command_list.append(otb_input_background_value)

# Generate command for RAM usage
otb_input_ram = generate_command('-ram ', False, input_ram, False)
command_list.append(otb_input_ram)

# Generate command for output XML file
otb_output_xml = generate_command('-out ', True, output_xml, False)
command_list.append(otb_output_xml)

# Generate full command for OTB
execute_command('otbcli_ComputeImagesStatistics ', command_list, workspace, otb_dir)