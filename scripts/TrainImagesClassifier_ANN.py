import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import execute_command

arcpy.AddMessage('\nTrain Artificial Neural Network Classifier')
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
log_file = os.path.join(log_folder, 'TRAINCLASSANN_' + ts_file_append + '.log')

with open(log_file, 'w') as f:
    f.write('')

# Load OTB Dir
with open(os.path.join(workspace, 'OTBDIR.ini'), 'r') as f:
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
input_train_validation_ratio = arcpy.GetParameterAsText(7)
input_name_discrimination_field = arcpy.GetParameterAsText(8)
input_train_method = arcpy.GetParameterAsText(9)
input_number_neurons = arcpy.GetParameterAsText(10)
input_neuron_activation_type = arcpy.GetParameterAsText(11)
input_alpha_param_activation = arcpy.GetParameterAsText(12)
input_beta_param_activation = arcpy.GetParameterAsText(13)
input_strength_weight_gradient_backdrop = arcpy.GetParameterAsText(14)
input_strength_momentum_term = arcpy.GetParameterAsText(15)
input_initial_value_delta_bprop = arcpy.GetParameterAsText(16)
input_update_values_lower_lim_bprop = arcpy.GetParameterAsText(17)
input_termination_criteria = arcpy.GetParameterAsText(18)
input_epsilon_termination = arcpy.GetParameterAsText(19)
input_iter_termination = arcpy.GetParameter(20)
input_user_seed = arcpy.GetParameterAsText(21)
out_conf_matrix = arcpy.GetParameterAsText(22)
out_model = arcpy.GetParameterAsText(23)

# Generate OTB commands
command_list = []

# State which classifier is being used
input_classifier = '-classifier ann'
command_list.append(input_classifier)

# Generate command for input imagery
otb_input_images = '-io.il '
for item in input_images.split(';'):
    item = item.rstrip("'")
    item = item.lstrip("'")
    otb_input_images += '"' + item + '"' + ' '
otb_input_images = otb_input_images.rstrip(' ')
command_list.append(otb_input_images)

# Generate command for input shapefiles
otb_input_train_shp = '-io.vd '
for item in input_train_shp.split(';'):
    item = item.rstrip("'")
    item = item.lstrip("'")
    otb_input_train_shp += '"' + item + '"' + ' '
otb_input_train_shp = otb_input_train_shp.rstrip(' ')
command_list.append(otb_input_train_shp)

# Generate command for XML Stats
if not len(str(input_xml_stats)) == 0:
    otb_input_xml_stats = '-io.imstat ' + input_xml_stats
    command_list.append(otb_input_xml_stats)

# Generate command for input elevation
if not len(str(input_default_elev)) == 0:
    otb_input_default_elev = '-elev.default ' + str(input_default_elev)
    command_list.append(otb_input_default_elev)

if not len(str(input_max_class_train_sample)) == 0:
    otb_input_max_class_train_sample = '-sample.mt ' + str(input_max_class_train_sample)
    command_list.append(otb_input_max_class_train_sample)

if not len(str(input_max_class_valid_sample)) == 0:
    otb_input_max_class_valid_sample = '-sample.mv ' + str(input_max_class_valid_sample)
    command_list.append(otb_input_max_class_valid_sample)

# Generate command for bound sample number by minimum
if not len(str(input_bound_sample_num_min)) == 0:
    otb_input_bound_sample_num_min = '-sample.bm ' + str(input_bound_sample_num_min)
    command_list.append(otb_input_bound_sample_num_min)

# Generate command for training and validation sample ratio
if not len(str(input_train_validation_ratio)) == 0:
    otb_input_train_validation_ratio = '-sample.vtr ' + str(input_train_validation_ratio)
    command_list.append(otb_input_train_validation_ratio)

if not len(input_name_discrimination_field) == 0:
    otb_input_name_discrimination_field = '-sample.vfn ' + input_name_discrimination_field
    command_list.append(otb_input_name_discrimination_field)

if not len(input_train_method) == 0:
    if input_train_method == 'BACK-PROPOGATION':
        input_train_method = 'back'
    elif input_train_method == 'RESILIENT BACK-PROPOGATION':
        input_train_method = 'reg'
    else:
        raise Exception('Unknown train method argument')
    otb_input_train_method = '-classifier.ann.t ' + input_train_method
    command_list.append(otb_input_train_method)

if not len(str(input_number_neurons)) == 0:
    otb_number_neurons = '-classifier.ann.sizes ' + str(input_number_neurons)
    command_list.append(otb_number_neurons)

if not len(str(input_neuron_activation_type)) == 0:
    if input_neuron_activation_type == 'SYMMETRICAL SIGMOID FUNCTION':
        input_neuron_activation_type = 'sig'
    elif input_neuron_activation_type == 'IDENTITY FUNCTION':
        input_neuron_activation_type = 'ident'
    elif input_neuron_activation_type == 'GAUSSIAN FUNCTION':
        input_neuron_activation_type = 'gau'
    else:
        raise Exception('Unknown activation type')
    otb_input_neuron_activation_type = '-classifier.ann.f ' + input_neuron_activation_type
    command_list.append(otb_input_neuron_activation_type)

if not len(str(input_alpha_param_activation)) == 0:
    otb_input_alpha_param_activation = '-classifier.ann.a ' + input_alpha_param_activation
    command_list.append(otb_input_alpha_param_activation)

if not len(str(input_beta_param_activation)) == 0:
    otb_input_beta_param_activation = '-classifier.ann.b ' + input_beta_param_activation
    command_list.append(otb_input_beta_param_activation)

if not len(str(input_strength_weight_gradient_backdrop)) == 0:
    otb_input_strength_weight_gradient_backdrop = '-classifier.ann.bpdw ' + input_strength_weight_gradient_backdrop
    command_list.append(otb_input_strength_weight_gradient_backdrop)

if not len(str(input_strength_momentum_term)) == 0:
    otb_input_strength_momentum_term = '-classifier.ann.bpms ' + input_strength_momentum_term
    command_list.append(otb_input_strength_momentum_term)

if not len(str(input_initial_value_delta_bprop)) == 0:
    otb_input_initial_value_delta_bprop = '-classifier.ann.rdw ' + input_initial_value_delta_bprop
    command_list.append(otb_input_initial_value_delta_bprop)

if not len(str(input_update_values_lower_lim_bprop)) == 0:
    otb_input_update_values_lower_lim_bprop = '-classifier.ann.rdwm ' + input_update_values_lower_lim_bprop
    command_list.append(otb_input_update_values_lower_lim_bprop)

if not len(str(input_termination_criteria)) == 0:
    if input_termination_criteria == 'MAX ITERATIONS':
        input_termination_criteria = 'iter'
    elif input_termination_criteria == 'EPSILON':
        input_termination_criteria = 'eps'
    elif input_termination_criteria == 'MAX ITERATIONS + EPSILON':
        input_termination_criteria = 'all'
    else:
        raise Exception('Unknown termination criteria')
    otb_input_termination_criteria = '-classifier.ann.term ' + input_termination_criteria
    command_list.append(otb_input_termination_criteria)

if not len(str(input_epsilon_termination)) == 0:
    otb_input_epsilon_termination = '-classifier.ann.eps ' + str(input_epsilon_termination)
    command_list.append(otb_input_epsilon_termination)

if not len(str(input_iter_termination)) == 0:
    otb_input_iter_termination = '-classifier.ann.iter ' + str(input_iter_termination)
    command_list.append(otb_input_iter_termination)

if not len(str(input_user_seed)) == 0:
    otb_input_user_seed = '-rand ' + input_user_seed
    command_list.append(otb_input_user_seed)

if not len(str(out_conf_matrix)) == 0:
    otb_out_conf_matrix = '-io.confmatout ' + out_conf_matrix
    command_list.append(otb_out_conf_matrix)

if not len(str(out_model)) == 0:
    otb_out_model = '-io.out ' + '"' + out_model + '"'
    command_list.append(otb_out_model)

# Generate full command for OTB
execute_command('otbcli_TrainImagesClassifier ', command_list, workspace, otb_dir)