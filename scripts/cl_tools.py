###
# Generate command function used to generate command line functions
###

import arcpy
import shutil
import os
import subprocess

def execute_command(command, arguments, workspace, otb_dir):
    """Combines and then executes the OTB command
    The filenames do not change."""
    # Generate full command for OTB
    otb_write_output = command
    for item in arguments:
        otb_write_output += item + ' '
    otb_write_output = otb_write_output.rstrip(' ')

    arcpy.AddMessage('\nOTB Command:\n')
    arcpy.AddMessage(otb_write_output)
    arcpy.AddMessage('\nCalling OTB software...\n')

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

    return otb_write_output


def generate_command(otb_command=None, quotes=None, input_variable=None, multi_list=False):
    """Generate OTB command.
    Quotes argument is if the command requires quotes wrapped around it
    which are useful for system paths"""

    # If there is an input, generate a command, else output nothing
    if input_variable > 0:

        if not quotes:
            if len(str(input_variable)) != 0:
                if not multi_list:
                    output_command = otb_command + input_variable
                elif multi_list:
                    output_command = otb_command
                    for item in input_variable.split(';'):
                        item = item.rstrip("'")
                        item = item.lstrip("'")
                        output_command += item + ' '
                    output_command = output_command.rstrip(' ')
            else:
                return ''

        elif quotes:
            if len(str(input_variable)) != 0:
                if not multi_list:
                    output_command = otb_command + '"' + input_variable + '"'
                elif multi_list:
                    output_command = otb_command
                    for item in input_variable.split(';'):
                        item = item.rstrip("'")
                        item = item.lstrip("'")
                        item = '"' + item + '"'
                        output_command += item + ' '
                    output_command = output_command.rstrip(' ')
            else:
                return ''

        return output_command

    else:
        return ''

if __name__ == '__main__':
    pass