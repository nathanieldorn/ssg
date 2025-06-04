import os

#first delete all files in public
def clear_public(directory):
    deleted_paths = []
    if os.path.exists(directory):
        for item in os.listdir(directory):
           path = os.path.join(directory, item)
           if os.path.isfile(path):
               deleted_paths.append(path)
               print("isfile")
               continue
           if os.path.isdir(path):
               print("isdir")
               deleted_paths.append(path)
               clear_public(path)
    print(deleted_paths)

            #os.remove(path)

#copy from static, all files and subs, to public recursively
#log path of each file as copied
