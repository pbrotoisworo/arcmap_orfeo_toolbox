import arcpy
import os

arcpy.AddMessage('\nConnect OTB Folder\n')

# Detect workspace, set up initial parameters
workspace = os.path.abspath(__file__)
log_folder = os.path.join(workspace, 'logs')
scratch_folder = os.path.join(workspace, 'scratch')
arcpy.env.overwriteOutput = True

# Input vars
in_otb = arcpy.GetParameterAsText(0)

with open('OTBDIR.ini', 'w') as f:
    f.write(in_otb)

arcpy.AddMessage('Updated OTB path: {}\n'.format(in_otb))

# Make log folder
if not os.path.exists(log_folder):
    os.mkdir(log_folder)
