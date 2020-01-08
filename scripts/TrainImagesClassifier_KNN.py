import arcpy
import os
import shutil
import subprocess
from datetime import datetime
from cl_tools import generate_command, execute_command

arcpy.AddMessage('\nTrain Images Classifier (KNN)')
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
log_file = os.path.join(log_folder, 'TRAINCLASSKNN' + ts_file_append + '.log')

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
input_number_of_neighbors = arcpy.GetParameterAsText(9)
input_user_seed = arcpy.GetParameterAsText(10)
input_ram = arcpy.GetParameterAsText(11)
out_conf_matrix = arcpy.GetParameterAsText(12)
out_model = arcpy.GetParameterAsText(13)

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

# Generate command for number of k neighbors
otb_input_number_of_neighbors = generate_command('-classifier.knn.k ', False, input_number_of_neighbors, False)
command_list.append(otb_input_number_of_neighbors)

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
execute_command('otbcli_TrainImagesClassifier ', command_list, workspace, otb_dir)