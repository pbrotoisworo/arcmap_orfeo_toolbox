import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command

arcpy.AddMessage('\nImage Classification')
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
log_file = os.path.join(log_folder, 'IMAGECLASSIFICATION_' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_image = arcpy.GetParameterAsText(0)
input_mask = arcpy.GetParameterAsText(1)
input_model = arcpy.GetParameterAsText(2)
input_ram = arcpy.GetParameterAsText(3)
input_statistics = arcpy.GetParameterAsText(4)
input_no_data_label = arcpy.GetParameterAsText(5)
input_output_image = arcpy.GetParameterAsText(6)
input_output_conf = arcpy.GetParameterAsText(7)


# def generate_command(otb_command=None, quotes=None, input_variable=None):
#     """Generate OTB command.
#     Quotes argument is if the command requires quotes wrapped around it
#     which are useful for system paths"""
#
#     if not quotes:
#         if len(str(input_variable)) != 0:
#             output_command = otb_command + input_variable
#         else:
#             return ''
#
#     elif quotes:
#         if len(str(input_variable)) != 0:
#             output_command = otb_command + '"' + input_variable + '"'
#         else:
#             return ''
#
#     return output_command

# Generate OTB commands
command_list = []

otb_input_image = generate_command('-in ', True, input_image)
command_list.append(otb_input_image)

otb_input_mask = generate_command('-mask ', True, input_mask)
command_list.append(otb_input_mask)

otb_input_model = generate_command('-model ', True, input_model)
command_list.append(otb_input_model)

otb_input_ram = generate_command('-ram ', False, input_ram)
command_list.append(otb_input_ram)

otb_input_statistics = generate_command('-imstat ', True, input_statistics)
command_list.append(otb_input_statistics)

otb_input_no_data_label = generate_command('-nodatalabel ', False, input_no_data_label)
command_list.append(otb_input_no_data_label)

otb_input_output_image = generate_command('-out ', True, input_output_image)
command_list.append(otb_input_output_image)

otb_input_output_conf = generate_command('-confmap ', True, input_output_conf)
command_list.append(otb_input_output_conf)

# Generate full command for OTB
otb_write_output = 'otbcli_ImageClassifier '
for item in command_list:
    otb_write_output += item + ' '
otb_write_output = otb_write_output.rstrip(' ')

arcpy.AddMessage('OTB Command:\n\n')
arcpy.AddMessage(otb_write_output)
arcpy.AddMessage('\n\nCalling OTB software...\n\n')
# Template file
dev_ini_file = os.path.join(workspace, 'otb_devenv.ini')

# batch file containing commands
command_file = os.path.join(otb_dir, 'otb_command.bat')

# Modified start_devenv to launch our modified script
out_batch_file = os.path.join(otb_dir, 'arcmap_orfeo_process.bat')
shutil.copy(dev_ini_file, out_batch_file)

with open(out_batch_file, 'a') as f:
    f.write('\n\n:: @cmd')
    f.write('\nstart cmd.exe /C {}'.format(command_file))

with open(command_file, 'w') as f:
    f.write('@echo on\n')
    f.write(otb_write_output)
    f.write('\n@echo off')
    f.write('\nPAUSE')

subprocess.call([out_batch_file])
# os.remove(out_batch_file)
# os.remove(command_file)
