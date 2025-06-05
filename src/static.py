import os, shutil

#first delete all files in public
def clear_public(deleted_paths, directory):

    if os.path.exists(directory):
        shutil.rmtree(directory)


#next copy all files and folders from static
def copy_static(copied_paths, directory):

    if not os.path.exists("../docs"):
        os.mkdir("../docs")

    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            copied_paths.append(path)
            public_dir = path.replace("static", "docs", 1)
            os.mkdir(public_dir)
            copy_static(copied_paths, path)
        if os.path.isfile(path):
            shutil.copy(path, path.replace("static", "docs", 1))
    return copied_paths
