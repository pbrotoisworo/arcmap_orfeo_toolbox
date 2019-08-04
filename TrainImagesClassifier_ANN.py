import arcpy
import os
import shutil
import subprocess

arcpy.AddMessage('\nTrain Artificial Neural Network Classifier')
arcpy.AddMessage('Orfeo Toolbox\n')

# Detect workspace, set up initial parameters
workspace = os.path.abspath(__file__)
log_folder = os.path.join(workspace, 'logs')
scratch_folder = os.path.join(workspace, 'scratch')
arcpy.env.overwriteOutput = True

# Load OTB Dir
with open('OTBDIR.ini', 'r') as f:
    otb_dir = f.read()
    otb_dir_devenv = os.path.join(otb_dir, 'start_devenv.bat')

if not os.path.exists(otb_dir):
    raise Exception('OTB files not found!')

# Input vars
input_images = arcpy.GetParameterAsText(0)
input_train_shp = arcpy.GetParameterAsText(1)
input_xml_stats = arcpy.GetParameterAsText(2)
input_default_elev = arcpy.GetParameterAsText(3)
input_max_class_train_sample = arcpy.GetParameterAsText(4)
input_max_class_valid_sample = arcpy.GetParameterAsText(5)
input_bound_sample_num_min = arcpy.GetParameterAsText(6)
input_on_edge_pixel_inclusion = arcpy.GetParameterAsText(7)
input_train_validation_ratio = arcpy.GetParameterAsText(8)
input_name_discrimination_field = arcpy.GetParameterAsText(9)
input_train_method = arcpy.GetParameterAsText(10)
input_number_neurons = arcpy.GetParameterAsText(11)
input_neuron_activation_type = arcpy.GetParameterAsText(12)
input_alpha_param_activation = arcpy.GetParameterAsText(13)
input_beta_param_activation = arcpy.GetParameterAsText(14)
input_strength_weight_gradient_backdrop = arcpy.GetParameterAsText(15)
input_strength_momentum_term = arcpy.GetParameterAsText(16)
input_initial_value_delta_bprop = arcpy.GetParameterAsText(17)
input_update_values_lower_lim_bprop = arcpy.GetParameterAsText(18)
input_termination_criteria = arcpy.GetParameterAsText(19)
input_epsilon_termination = arcpy.GetParameterAsText(20)
input_iter_termination = arcpy.GetParameter(21)
input_user_seed = arcpy.GetParameterAsText(22)
out_conf_matrix = arcpy.GetParameterAsText(23)
out_model = arcpy.GetParameterAsText(24)
classifier = 'ann'

# Generate OTB commands
command_list = []

# Generate command for input imagery
otb_input_images = '-io.il '
for item in input_images.split(';'):
    otb_input_images += item + ' '
otb_input_images = otb_input_images.rstrip(' ')
command_list.append(otb_input_images)

# Generate command for input shapefiles
otb_input_train_shp = '-io.vd '
for item in input_train_shp.split(';'):
    otb_input_train_shp += item + ' '
otb_input_train_shp = otb_input_train_shp.rstrip(' ')
command_list.append(otb_input_train_shp)

# Generate command for XML Stats
if not len(input_xml_stats) == 0:
    otb_input_xml_stats = '-io.imstat ' + input_xml_stats
    command_list.append(otb_input_xml_stats)

# Generate command for input elevation
if not len(input_default_elev) == 0:
    otb_input_default_elev = 'elev.default ' + input_default_elev
    command_list.append(otb_input_default_elev)

if not len(input_max_class_train_sample) == 0:
    otb_input_max_class_train_sample = '-sample.mt ' + input_max_class_train_sample
    command_list.append(otb_input_max_class_train_sample)

if not len(input_max_class_valid_sample) == 0:
    otb_input_max_class_valid_sample = '-sample.mv ' + input_max_class_valid_sample
    command_list.append(otb_input_max_class_valid_sample)

# Generate command for bound sample number by minimum
if not len(input_bound_sample_num_min) == 0:
    otb_input_bound_sample_num_min = '-sample.bm ' + input_bound_sample_num_min
    command_list.append(otb_input_bound_sample_num_min)

# Generate command for training and validation sample ratio
if not len(input_train_validation_ratio) == 0:
    otb_input_train_validation_ratio = '-sample.vtr ' + input_train_validation_ratio
    command_list.append(otb_input_train_validation_ratio)

if not len(input_name_discrimination_field) == 0:
    otb_input_name_discrimination_field = '-sample.vfn ' + input_name_discrimination_field
    command_list.append(otb_input_name_discrimination_field)

if not len(input_train_method) == 0:
    otb_input_train_method = '-classifier.ann.t ' + input_train_method
    command_list.append(otb_input_train_method)

if not len(input_number_neurons) == 0:
    otb_number_neurons = '-classifier.ann.sizes ' + input_number_neurons
    command_list.append(otb_number_neurons)

if not len(input_neuron_activation_type) == 0:
    otb_input_neuron_activation_type = '-classifier.ann.f ' + input_neuron_activation_type
    command_list.append(otb_input_neuron_activation_type)

if not len(input_alpha_param_activation) == 0:
    otb_input_alpha_param_activation = '-classifier.ann.a ' + input_alpha_param_activation
    command_list.append(otb_input_alpha_param_activation)

if not len(input_beta_param_activation) == 0:
    otb_input_beta_param_activation = '-classifier.ann.b ' + input_beta_param_activation
    command_list.append(otb_input_beta_param_activation)

if not len(input_strength_weight_gradient_backdrop) == 0:
    otb_input_strength_weight_gradient_backdrop = '-classifier.ann.bpdw ' + input_strength_weight_gradient_backdrop
    command_list.append(otb_input_strength_weight_gradient_backdrop)

if not len(input_strength_momentum_term) == 0:
    otb_input_strength_momentum_term = '-classifier.ann.bpms ' + input_strength_momentum_term
    command_list.append(otb_input_strength_momentum_term)

if not len(input_initial_value_delta_bprop) == 0:
    otb_input_initial_value_delta_bprop = '-classifier.ann.rdw ' + input_initial_value_delta_bprop
    command_list.append(otb_input_initial_value_delta_bprop)

if not len(input_update_values_lower_lim_bprop) == 0:
    otb_input_update_values_lower_lim_bprop = '-classifier.ann.rdwm ' + input_update_values_lower_lim_bprop
    command_list.append(otb_input_update_values_lower_lim_bprop)

if not len(input_termination_criteria) == 0:
    otb_input_termination_criteria = '-classifier.ann.term ' + input_termination_criteria
    command_list.append(otb_input_termination_criteria)

if not len(input_epsilon_termination) == 0:
    otb_input_epsilon_termination = '-classifier.ann.eps ' + input_epsilon_termination
    command_list.append(otb_input_epsilon_termination)

if not len(input_iter_termination) == 0:
    otb_input_iter_termination = '-classifier.ann.iter' + input_iter_termination
    command_list.append(otb_input_iter_termination)

if not len(input_user_seed) == 0:
    otb_input_user_seed = '-rand ' + input_user_seed
    command_list.append(otb_input_user_seed)

if not len(out_conf_matrix) == 0:
    otb_out_conf_matrix = '-io.confmatout ' + out_conf_matrix
    command_list.append(otb_out_conf_matrix)

if not len(out_model) == 0:
    otb_out_model = '-io.out ' + out_model
    command_list.append(otb_out_model)

# Generate full command for OTB
otb_write_output = 'obtcli_TrainImagesClassifier '
for item in command_list:
    otb_write_output += item + ' '
arcpy.AddMessage('OTB Command:\n\n')
arcpy.AddMessage(otb_write_output)
arcpy.AddMessage('\n\nCalling OTB software...')
# Template file
dev_ini_file = os.path.join(workspace, 'otb_devenv.ini')

# batch file containing commands
command_file = os.path.join(otb_dir, 'otb_command.bat')

# Modified start_devenv to launch our modified script
out_batch_file = os.path.join(otb_dir, 'process.bat')

shutil.copy(dev_ini_file, out_batch_file)

with open(out_batch_file, 'a') as f:
    f.write('start cmd.exe /k {}'.format(out_batch_file))

with open(command_file, 'w') as f:
    f.write(otb_write_output)

subprocess.call([out_batch_file])
os.remove(out_batch_file)
os.remove(command_file)
