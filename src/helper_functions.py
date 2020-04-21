import re
import os
<<<<<<< HEAD

=======
>>>>>>> 0b9cf7488b36638f1e2160099d2a13fc4132fb49
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
        print('File bigger than cache can not download')
        download_flag = 0

    elif size_to_add + cache_directory_size > cache_size:
        print('Deleting files to update cache')

        

    return download_flag
        
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
