import os, shutil

#first delete all files in public
def clear_public(deleted_paths, directory):

    if os.path.exists(directory):
        for item in os.listdir(directory):
           path = os.path.join(directory, item)
           if os.path.isfile(path):
               deleted_paths.append(path)
               os.remove(path)
           if os.path.isdir(path):
               deleted_paths.append(path)
               clear_public(deleted_paths, path)
        for item in deleted_paths[::-1]:
            if os.path.isdir(item):
                os.rmdir(item)
        return deleted_paths
    else:
        return


#next copy all files and folders from static
def copy_static(copied_paths, directory):

    if not os.path.exists("../ssg/public"):
        os.mkdir("../ssg/public")

    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            copied_paths.append(path)
            public_dir = path.replace("static", "public", 1)
            os.mkdir(public_dir)
            copy_static(copied_paths, path)
        if os.path.isfile(path):
            shutil.copy(path, path.replace("static", "public", 1))
    return copied_paths
