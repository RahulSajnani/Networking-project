import re
import os

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


def clear_cache(path, size_to_add, cache_size):
    '''
    Function to clear cache. Clears files having earliest access time
    
    '''

    download_flag = 1

    cache_directory_size = sum(os.path.getsize(f) for f in os.listdir(path) if os.path.isfile(f))

    print(cache_directory_size)
    
    if size_to_add > cache_size:
        print('File too bigger than cache')
        download_flag = 0

    elif size_to_add + cache_directory_size > cache_size:
        print('Deleting files to update cache')

    return download_flag
        