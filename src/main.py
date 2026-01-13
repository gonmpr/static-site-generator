import os, shutil

def copy_files(from_path, to_path, root='/'):
    print(f"--- MOVING FILES FROM {from_path} TO {to_path} ---")
    to_path = os.path.join(root, to_path)
    from_path = os.path.join(root, from_path)

    if not os.path.exists(from_path):
        raise Exception(f"mv_files: {from_path} doesn't exists")


    if os.path.exists(to_path):
        shutil.rmtree(to_path) 

    os.mkdir(to_path)    
    copyr_files(from_path, to_path)


def copyr_files(from_path, to_path):

    files = os.listdir(from_path)

    for file in files:
        file_path = os.path.join(from_path, file)

        if os.path.isfile(file_path):
            print(f"copying {file}: {file_path} -> {to_path}")
            shutil.copy(file_path, to_path)
        else:
            subfolder = os.path.join(to_path, file)
            print(f"\n ---subfolder {file}--- \n")
            if not os.path.exists(subfolder):
                os.mkdir(subfolder)
            copyr_files(file_path, subfolder)

    print(f"done with {files}")


def main():
    copy_files('static', 'public', os.getcwd())





if __name__ == '__main__':
    main()
