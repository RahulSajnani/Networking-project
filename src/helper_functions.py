import re

def string_split(string_input):

    '''
    Function to escape spaces with '\ ' and splitting strings correctly
    Input:
        string_input - input string
    Returns:
        string_output - output string
    
    '''

    string_list = re.split(r'(?<!\\) ', string_input)
    
    string_output = [ string.replace('\\ ', ' ') for string in string_list]
    
    return string_output

        