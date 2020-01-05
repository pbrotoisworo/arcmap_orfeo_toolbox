###
# Generate command function used to generate command line functions
###

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