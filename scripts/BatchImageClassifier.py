import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command, execute_command

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
log_file = os.path.join(log_folder, 'BATCHIMAGECLASSIFICATION_' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_images = arcpy.GetParameterAsText(0)
input_model = arcpy.GetParameterAsText(1)
input_ram = arcpy.GetParameterAsText(2)
input_output_batch_prefix = arcpy.GetParameterAsText(3)
input_output_folder = arcpy.GetParameterAsText(4)
input_output_conf = arcpy.GetParameterAsText(5)

# Generate OTB commands
command_list = []

for idx, input_image in enumerate(input_images.split(';')):

    input_image = input_image.rstrip("'")
    input_image = input_image.lstrip("'")

    otb_input_image = generate_command('-in ', True, input_image)
    command_list.append(otb_input_image)

    otb_input_model = generate_command('-model ', True, input_model)
    command_list.append(otb_input_model)

    otb_input_ram = generate_command('-ram ', False, input_ram)
    command_list.append(otb_input_ram)

    output_file = str(idx) + '_' + input_output_batch_prefix + '.tif'
    input_output_image = os.path.join(input_output_folder, output_file)
    otb_input_output_image = generate_command('-out ', True, input_output_image, False)
    command_list.append(otb_input_output_image)

    if str(input_output_conf) == 'true':
        output_file = str(idx) + '_' + '_conf_' + input_output_batch_prefix + '.tif'
        output_dir = os.path.dirname(input_output_conf)
        input_output_conf = os.path.join(input_output_folder, output_file)
        otb_input_output_conf = generate_command('-confmap ', True, input_output_conf, False)
        command_list.append(otb_input_output_conf)

    command_list.append('& otbcli_ImageClassifier ')

# Generate full command for OTB
del command_list[-1]
otb_write_output = execute_command('otbcli_ImageClassifier ', command_list, workspace, otb_dir)

# Save command to log
with open(log_file, 'w') as f:
    f.write('Batch Image Classification Log')
    f.write('\nTimestamp: {}'.format(ts))
    f.write('\nTotal Items: {}'.format(len(input_images.split(';'))))
    f.write('\nInput Images: {}'.format(input_images))
    f.write('\nInput Model: {}'.format(input_model))
    f.write('\nInput RAM Limit: {}'.format(input_ram))
    f.write('\nOutput filename: {}'.format(input_output_batch_prefix))
    f.write('\nOutput folder: {}'.format(input_output_folder))
    f.write('\nGenerate confidence map: {}'.format(otb_input_output_conf))
    f.write('\nOTB Command: {}'.format(otb_write_output))