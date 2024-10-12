import os
import json
import zipfile
from zipfile import ZipFile

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils import MetManagement, SimpleDialogQt
else:
    from orangecontrib.AAIT.utils import MetManagement, SimpleDialogQt

def generate_listing_json(directory_to_list):
    """
    generate a file file_info.json  with size of file in directory
    for low level devellopper only
    -> use create_index_file
    """
    output_json_file = directory_to_list+'/files_info.json'
    if os.path.isfile(output_json_file):
        os.remove(output_json_file)

    def list_files_recursive(directory):
        files_info = {}

        for root, dirs, files in os.walk(directory):
            for file in files:

                file_path = os.path.join(root, file).replace("\\","/")
                file_size = os.path.getsize(file_path)
                file_path=file_path[len(directory)+1:]
                files_info[file_path]=file_size

        return files_info

    def save_to_json(data, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    files_info = list_files_recursive(directory_to_list)
    save_to_json(files_info, output_json_file)
    return files_info

def add_file_to_zip_file(folder,file_in,zip_file):
    """
    folder : a point to start relative path
    file in : a file to add to zip file
    zip file : destination zip file
    for exemple I want to add C:/dir1/dir2/dir3/qwerty.txt to
    C:/dir1//dir2/example.zip and index dir3/qwerty.txt
    folder = C:/dir1/
    file_in=C:/dir1/dir2/dir3/qwerty.txt
    zip_file  C:/dir2/example.zip
    """
    path_in=folder+file_in
    with open(path_in, 'rb') as f:
        contenu = f.read()
    with zipfile.ZipFile(zip_file, 'a', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(file_in, contenu)

def create_index_file(in_repo_file,out_repo_file):
    """
    delete files_info.json and regenerate it
    with file contain a dictionnary filename:filesize
    out_repo_file is not used
    """
    if not os.path.isfile(in_repo_file):
        raise Exception("The specified path is not a file "+in_repo_file)
    if 0!=MetManagement.get_size(in_repo_file):
        raise Exception("The file " + in_repo_file+ " need to be empty to use this functions")
    print(MetManagement.get_size(in_repo_file))
    folder_to_process=os.path.dirname(in_repo_file).replace("\\","/")
    file_info=generate_listing_json(folder_to_process)
    return

def decode(repo_file,file_to_read):
    """
    /!\ be carrefull with big file (ram saturation)
    return containt of a zipped file
    """
    if os.path.isfile(repo_file)==False:
        return None
    file_to_read=os.path.splitext(os.path.basename(repo_file))[0]+"/"+file_to_read
    with zipfile.ZipFile(repo_file, 'r') as zip_ref:
        with zip_ref.open(file_to_read) as file:
            content = file.read()
            return content.decode('utf-8')
    return None
def decode_to_file(zip_path, target_path, output_path):
    """
    extract a file from a zip file and write it on hdd
    example : I want to extract dir1/qwerty.txt from C:/dir1/dir2/zipfile.zip to C:/dir_a/dir_b/dir1/qwerty.txt
    zip_path=C:/dir1/dir2/zipfile.zip
    target_path=dir1/qwerty.txt
    output_path=C:/dir_a/dir_b/
    """
    chunk_size = 1024 * 1024 * 100 # 100 Mo
    target_path=os.path.splitext(os.path.basename(zip_path))[0]+"/"+target_path
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        target_path = target_path.rstrip('/')
        files_to_extract = [f for f in zip_ref.namelist() if f.startswith(target_path)]

        if len(files_to_extract) == 0:
            raise FileNotFoundError(f"{target_path} not found in the archive.")

        if len(files_to_extract) == 1 and not files_to_extract[0].endswith('/'):
            # Cible est un fichier unique
            output_file_path = output_path
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with zip_ref.open(files_to_extract[0]) as source, open(output_file_path, 'wb') as target:
                #target.write(source.read())
                while True:
                    # read and write a chunk to avoid ram limitation
                    chunk = source.read(chunk_size)
                    if not chunk:
                        break
                    target.write(chunk)
        else:
            # Cible est un dossier ou plusieurs fichiers
            for file in files_to_extract:
                relative_path = os.path.relpath(file, start=target_path)
                destination_path = os.path.join(output_path, relative_path)

                if file.endswith('/'):
                    os.makedirs(destination_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    with zip_ref.open(file) as source, open(destination_path, 'wb') as target:
                        #target.write(source.read())
                        while True:
                            # read and write a chunk to avoid ram limitation
                            chunk = source.read(chunk_size)
                            if not chunk:
                                break
                            target.write(chunk)

if __name__ == "__main__":
    in_repo_file="C:/Users/jean-/Desktop/AAIT_v240916/repository.aait"
    out_repo_file="C:/Users/jean-/Desktop/AAIT_v240916/AAIT_v240828.aait"
    create_index_file(in_repo_file, out_repo_file)

