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

def delete_file(path):
    '''
    Function to delete file given a path
    '''
    try:
        os.remove(path)
    except OSError as e:
        print ("Error: %s: %s"% (path, e.strerror))
def directory_size(path):
    totalsize = 0
    for folderpath, dirs, f in os.walk(path):
        for files in f:
            filepath = os.path.join(folderpath, files)
            totalsize += os.path.getsize(filepath)
    return totalsize


# cache_directory_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './client-cache/'))
# delete_file(cache_directory_path+"/cache_test.txt")
# print (directory_size(cache_directory_path))

# print (os.path.getsize(cache_testhe_directory_path+"/cache_test.txt"))