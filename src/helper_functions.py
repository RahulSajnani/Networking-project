import re
import os
import time



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

def directory_info(path):

    '''
    Function to calculate total directory size and returns list with size and access time information
    '''

    totalsize = 0
    list_files = []

    for folderpath, dirs, f in os.walk(path):
        for files in f:
            filepath = os.path.join(folderpath, files)
            file_size = os.path.getsize(filepath)
            file_atime = time.localtime(os.path.getatime(filepath))
            # file_atime = time.strftime('%Y-%m-%d %H:%M:%S',file_atime)
            totalsize += file_size
            list_files.append({'path': filepath, 'size': file_size, 'atime': file_atime})
    
    return totalsize, list_files


def clear_cache(path, size_to_add, cache_size):
    '''
    Function to clear cache. Clears files having earliest access time
    
    '''

    download_flag = 1

    cache_directory_size, file_list = directory_info(path)   

    
    file_list = (sorted(file_list, key = lambda i: i['atime']))
    print(cache_directory_size)

    if size_to_add > cache_size:
        print('File bigger than cache can not download')
        download_flag = 0

    elif size_to_add + cache_directory_size > cache_size:
        size_to_delete = size_to_add + cache_directory_size - cache_size

        print('Deleting files to update cache. To delete ' + str(size_to_delete) + ' bytes')
        running_size = 0
        
        print('Removing following files from cache :')
        
        for i in range(len(file_list)):

            running_size += file_list[i]['size']
            print(file_list[i]['path'] + ' having size ' + str(file_list[i]['size']))
            delete_file(file_list[i]['path'])
            if running_size > size_to_delete:
                break
        

    return download_flag


# def get_file_hash(path):

def string_search_txt(filename):
    '''
    Input:
    Filename as a string
    Returns:
    1 if txt file has the word 'programmer'
    0 otherwise
    '''
    if filename[-4:] == ".txt":
        with open(filename) as file:
            if 'Programmer' in file.read():
                # print ("yes")
                return 1
            else:
                # print ("No")
                return 0
    else:
        print ("File is not a txt file")

## testing helper functions
# file_storage_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), './file-storage-client/'))
# string_search_txt(file_storage_path+"/bonus_test.txt")
