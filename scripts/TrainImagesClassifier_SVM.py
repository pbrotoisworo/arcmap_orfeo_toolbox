import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command, execute_command

arcpy.AddMessage('\nTrain Images Classifier (libsvm)')
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
log_file = os.path.join(log_folder, 'TRAINCLASSSVM' + ts_file_append + '.log')

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
input_kernel_type = arcpy.GetParameterAsText(9)
input_svm_model_type = arcpy.GetParameterAsText(10)
input_cost_param_c = arcpy.GetParameterAsText(11)
input_cost_param_nu = arcpy.GetParameterAsText(12)
input_parameter_optimization = arcpy.GetParameterAsText(13)
input_probability_estimation = arcpy.GetParameterAsText(14)
input_user_seed = arcpy.GetParameterAsText(15)
input_ram = arcpy.GetParameterAsText(16)
out_conf_matrix = arcpy.GetParameterAsText(17)
out_model = arcpy.GetParameterAsText(18)

# Generate OTB commands
command_list = []

# State which classifier is being used
input_classifier = '-classifier libsvm'
command_list.append(input_classifier)

# Generate command for input shapefiles
otb_input_train_shp = generate_command('-io.vd ', True, input_train_shp, True)
command_list.append(otb_input_train_shp)

# Generate command for XML Stats
if len(input_xml_stats) > 0:
    otb_input_xml_stats = generate_command('-io.imstat ', True, input_xml_stats, False)
    command_list.append(otb_input_xml_stats)

# Generate command for default elevation
otb_input_default_elev = generate_command('-elev.default ', False, input_default_elev, False)
command_list.append(otb_input_default_elev)

# Generate command for max train class sample
otb_input_max_class_train_sample = generate_command('-sample.mt ', False, input_max_class_train_sample, False)
command_list.append(otb_input_max_class_train_sample)

# Generate command for max valid class sample
otb_input_max_class_valid_sample = generate_command('-sample.mv ', False, input_max_class_valid_sample, False)
command_list.append(otb_input_max_class_valid_sample)

# Generate command for bound sample number by minimum
otb_input_bound_sample_num_min = generate_command('-sample.bm ', False, input_bound_sample_num_min, False)
command_list.append(otb_input_bound_sample_num_min)

# Generate command for training and validation sample ratio
otb_input_train_validation_ratio = generate_command('-sample.vtr ', False, input_train_validation_ratio, False)
command_list.append(otb_input_train_validation_ratio)

# Generate command for discrimination field
otb_input_name_discrimination_field = generate_command('-sample.vfn ', False, input_name_discrimination_field, False)
command_list.append(otb_input_name_discrimination_field)

# Generate command for SVM kernel type
otb_input_kernel_type = generate_command('-classifier.libsvm.k ', False, input_kernel_type, False)
command_list.append(otb_input_kernel_type)

# Generate command for SVM model type
otb_input_svm_model_type = generate_command('-classifier.libsvm.m ', False, input_svm_model_type, False)
command_list.append(otb_input_svm_model_type)

# Generate command for cost parameter C
otb_input_cost_param_c = generate_command('-classifier.libsvm.c ', False, input_cost_param_c, False)
command_list.append(otb_input_cost_param_c)

# Generate command for cost parameter Nu
otb_input_cost_param_nu = generate_command('-classifier.libsvm.nu ', False, input_cost_param_nu, False)
command_list.append(otb_input_cost_param_nu)

# Generate command for parameters optimization
otb_input_parameter_optimization = generate_command('-classifier.libsvm.opt ', False, input_parameter_optimization, False)
command_list.append(otb_input_parameter_optimization)

# Generate command for probability estimation
otb_input_probability_estimation = generate_command('-classifier.libsvm.prob ', False, input_probability_estimation, False)
command_list.append(otb_input_probability_estimation)

# Generate command for user defined seed
otb_input_user_seed = generate_command('-rand ', False, input_user_seed, False)
command_list.append(otb_input_user_seed)

# Generate command for available RAM
otb_input_ram = generate_command('-ram ', False, input_ram, False)
command_list.append(otb_input_ram)

# Generate command for output confusion matrix
if len(out_conf_matrix) > 0:
    otb_out_conf_matrix = generate_command('-io.confmatout ', True, out_conf_matrix, False)
    command_list.append(otb_out_conf_matrix)

# Generate command for output model file
otb_out_model = generate_command('-io.out ', True, out_model, False)
command_list.append(otb_out_model)

# Generate full command for OTB
otb_write_output = execute_command('otbcli_TrainImagesClassifier ', command_list, workspace, otb_dir)

# Save command to log
with open(log_file, 'w') as f:
    f.write('Train Images Classifier (SVM)')
    f.write('Timestamp: {}'.format(ts))
    f.write('Input Images: {}'.format(input_images.split(';')))
    f.write('Train/Validation Sample Ratio: {}'.format(input_train_validation_ratio))
    f.write('Bound sample number minimum: {}'.format(input_bound_sample_num_min))
    f.write('Default Elevation: {}'.format(input_default_elev))
    f.write('SVM Kernel Type: {}'.format(input_kernel_type))
    f.write('SVM Model Type: {}'.format(input_svm_model_type))
    f.write('Cost Parameter C: {}'.format(input_cost_param_c))
    f.write('Cost Parameter Nu: {}'.format(input_cost_param_nu))
    f.write('Parameters Optimization: {}'.format(input_parameter_optimization))
    f.write('Probability Estimation: {}'.format(input_probability_estimation))
    f.write('User Seed: {}'.format(input_user_seed))
    f.write('Output Confusion Matrix: {}'.format(out_conf_matrix))
    f.write('Output Model: {}'.format(out_model))
    f.write('OTB Command: {}'.format(otb_write_output))