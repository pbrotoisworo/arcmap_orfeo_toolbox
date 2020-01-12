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
log_file = os.path.join(log_folder, 'CLASSIFYKMEANS' + ts_file_append + '.log')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_image = arcpy.GetParameterAsText(0)
input_ram = arcpy.GetParameterAsText(1)
input_validity_mask = arcpy.GetParameterAsText(2)
input_training_set_size = arcpy.GetParameterAsText(3)
input_number_of_classes = arcpy.GetParameterAsText(4)
input_max_num_iterations = arcpy.GetParameterAsText(5)
input_sampler_type = arcpy.GetParameterAsText(6)
input_mask_value = arcpy.GetParameterAsText(7)
input_seed = arcpy.GetParameterAsText(8)
output_centroid_file = arcpy.GetParameterAsText(9)
output_file = arcpy.GetParameterAsText(10)

command_list = []

# Generate command for input image
otb_input_image = generate_command('-in ', True, input_image, False)
command_list.append(otb_input_image)

# Generate command for RAM limit
otb_input_ram = generate_command('-ram ', False, input_ram, False)
command_list.append(otb_input_ram)

# Generate command for validity mask
if len(input_validity_mask) > 0:
    otb_input_validity_mask = generate_command('-vm ', True, input_validity_mask, False)
    command_list.append(otb_input_validity_mask)

# Generate command for training set size
otb_input_training_set_size = generate_command('-ts ', False, input_training_set_size, False)
command_list.append(otb_input_training_set_size)

# Generate command for number of classes
otb_input_number_of_classes = generate_command('-nc ', False, input_number_of_classes, False)
command_list.append(otb_input_number_of_classes)

# Generate command for maximum number of iterations
otb_input_max_num_iterations = generate_command('-maxit ', False, input_max_num_iterations, False)
command_list.append(otb_input_max_num_iterations)

# Generate command for sampler type
otb_input_sampler_type = generate_command('-sampler ', False, input_sampler_type, False)
command_list.append(otb_input_sampler_type)

# Generate command for output centroid
if len(output_centroid_file) > 0:
    otb_output_centroid_file = generate_command('-outmeans ', True, output_centroid_file, False)
    command_list.append(otb_output_centroid_file)

# Generate command for input mask value
otb_input_mask_value = generate_command('-nodatalabel ', False, input_mask_value, False)
command_list.append(otb_input_mask_value)

# Generate user seed
otb_input_seed = generate_command('-rand ', False, input_seed, False)
command_list.append(otb_input_seed)

otb_output_file = generate_command('-out ', True, output_file, False)
command_list.append(otb_output_file)

# Generate full command for OTB
otb_write_output = execute_command('otbcli_KMeansClassification ', command_list, workspace, otb_dir)

# Save command to log
with open(log_file, 'w') as f:
    f.write('K Means Classification Log')
    f.write('\nTimestamp: {}'.format(ts))
    f.write('\nImage Input: {}'.format(input_image))
    f.write('\nValidity Mask: {}'.format(input_validity_mask))
    f.write('\nTraining Set Size: {}'.format(input_training_set_size))
    f.write('\nNumber of classes: {}'.format(input_number_of_classes))
    f.write('\nMax Number of Iterations: {}'.format(input_max_num_iterations))
    f.write('\nMask Value: {}'.format(input_mask_value))
    f.write('\nSampler Type: {}'.format(input_sampler_type))
    f.write('\nOutput centroid file: {}'.format(output_centroid_file))
    f.write('\nOutput image: {}'.format(output_file))
    f.write('\nOTB Command: {}'.format(otb_write_output))
