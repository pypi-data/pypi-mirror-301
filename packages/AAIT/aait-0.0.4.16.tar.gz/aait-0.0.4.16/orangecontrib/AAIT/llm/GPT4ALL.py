import sys
from os.path import expanduser
import os
import re
import subprocess
import json
import time
import chardet
import psutil
from Orange.data import Domain, StringVariable, Table
import ftfy
import xml.etree.ElementTree as ET
import configparser 
# change this variable too choose a non standard path
gpt4all_path = ""
if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_local_store_path
    from Orange.widgets.orangecontrib.AAIT.utils import SimpleDialogQt
else:
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path
    from orangecontrib.AAIT.utils import SimpleDialogQt

def get_gpt4all_exe_path():
    # If OS is Windows
    if os.name == 'nt':
        if gpt4all_path != "":
            return gpt4all_path



        none_standard_path=sys.executable.replace("\\","/")
        none_standard_path=os.path.dirname(none_standard_path)
        none_standard_path = os.path.dirname(none_standard_path)
        none_standard_path=none_standard_path+"/gpt4all/bin/chat.exe"
        if os.path.isfile(none_standard_path):
            return none_standard_path

        if os.path.isfile(os.path.join(os.getenv('USERPROFILE'), "gpt4all", "bin", "chat.exe")):
            return os.path.join(os.getenv('USERPROFILE'), "gpt4all", "bin", "chat.exe").replace("\\","/")
        none_standard_path = sys.executable.replace("\\", "/")
        none_standard_path = os.path.dirname(none_standard_path)
        none_standard_path = os.path.dirname(none_standard_path)
        none_standard_path = none_standard_path + "/Orange/Lib/site-packages/forall/gpt4all/bin/chat.exe"
        if os.path.isfile(none_standard_path):
            return none_standard_path
        if os.path.isfile("C:/Program Files/Gpt4All – 3.2.1/bin/chat.exe"):
            return "C:/Program Files/Gpt4All – 3.2.1/bin/chat.exe"
    if os.name=="posix":# Macintosh and Unix
        if str(os.uname().sysname) == "Darwin":  # Machintosh"
            return "/Applications/gpt4all/bin/gpt4all.app"
        # case Unix not  implemented now
    SimpleDialogQt.BoxError("OS not suported")
    return ""

def get_gpt4all_ini_path():

    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        config_file_path = os.path.join(appdata_path, "nomic.ai", "GPT4All.ini")
        return config_file_path

    elif os.name=="posix":# Macintosh and Unix
        if str(os.uname().sysname) == "Darwin": # Machintosh
            config_file_path = os.path.expanduser("~")
            config_file_path = config_file_path.replace("\\", "/")
            config_file_path =config_file_path+"/.config/gpt4all.io/GPT4All.ini"
            return config_file_path
        # case Unix not  implemented now
    else:
        SimpleDialogQt.BoxError("OS not suported")
        return ""

def get_process_name():
    if os.name == 'nt':
        return "chat.exe"
    if os.name == "posix":
        return "gpt4all"
    SimpleDialogQt.BoxError("OS not suported")
    return ""

# write time in a temp file to be checked if necessary to kill process
def write_time_in_tempfile():
    print("maj horadatage")
    temp_dir = os.getenv('TEMP')
    file_path = os.path.join(temp_dir, 'date_heure.txt')
    current_time_seconds = int(time.time())
    with open(file_path, 'w') as file:
        file.write(str(current_time_seconds))

def open_gpt_4_all(table, progress_callback=None, widget=None):
    """
    Opens the GPT4All application if it is not already running. It waits for the application to be ready,
    then generates and cleans the response using the `generate_and_clean_response` function. If the generation
    and cleaning is successful, it creates a new table with an answer domain and returns it. If the application
    fails to open or the generation and cleaning times out, it returns None.

    :param table: The input table.
    :type table: Orange.data.Table
    :param progress_callback: A callback function to track progress.
    :type progress_callback: function
    :param widget: The widget calling this function.
    :type widget: Orange.widgets.Widget
    :return: A table with an answer domain or None.
    :rtype: Orange.data.Table or None
    """

    # Modify GPT4All configuration
    modify_gpt4all_config()

    # If table is None, return None
    if table is None:
        return None

    # Launch GPT4All application if not already running
    gpt4all_exe_path = get_gpt4all_exe_path()
    # If GPT4All is not already running, try to launch it
    if not is_process_running(get_process_name()):
        try:
            os_type = os.name
            show_window_gpt4all = False
            if os_type == "nt":
                if show_window_gpt4all == True:
                    subprocess.Popen([gpt4all_exe_path], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # Chemin vers ton fichier exécutable exe_path = "chemin/vers/ton_executable.exe"
                    # Créer une instance de STARTUPINFO
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    # Utiliser la fenêtre de démarrage
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                    # Masquer la fenêtre
                    # Lancer le processus avec la fenêtre masquée subprocess.run(exe_path, startupinfo=startupinfo)
                    subprocess.Popen([gpt4all_exe_path], startupinfo=startupinfo, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

                    # writing a timestamp to a time file
                    write_time_in_tempfile()
                    time.sleep(3)

                    file_py_killer = os.path.dirname(os.path.abspath(__file__)).replace("\\",
                                                                                        "/") + "/GPT4ALL_killer.py"
                    time.sleep(1)
                    #launch of a process that kills chat.exe after a certain period of time
                    subprocess.Popen([sys.executable, file_py_killer], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)





            elif str(os.uname().sysname) == "Darwin": # machintosh
                subprocess.run(["open", gpt4all_exe_path],shell=False)
            else:
                print("platform not suported")
                return None
                #subprocess.Popen([gpt4all_exe_path], shell=False)

        except Exception as e:
            print(f"Error opening GPT4All: {e}")
            if widget is not None:
                widget.error("GPT4All can't be reached check installation")
            return None

    # Wait for GPT4All to be ready
    timeout = 0
    rows = None

    # wait until gpt4all is opened
    nb_iter_max=10
    for i in range(nb_iter_max):
        time.sleep(0.5)
        if is_process_running(get_process_name()):
            break





    # Wait for GPT4All to be ready or timeout
    if rows is None :
        rows = generate_and_clean_responses(table, progress_callback)
    # If GPT4All is not ready after timeout, return None
    if rows is None:
        print("Timeout waiting for GPT4All to be ready")
        if widget is not None:
            widget.error("GPT4 must be running. Please launch it and try again.")
        return None

    # Create and return table with answer domain
    answer_dom = [StringVariable("Answer")]
    domain = Domain(attributes=table.domain.attributes, metas=(list(table.domain.metas)) + answer_dom,
                    class_vars=table.domain.class_vars)
    return Table.from_list(domain=domain, rows=rows)

def generate_and_clean_responses(data, progress_callback):
    """
    Generate and clean responses for each row in the input data.

    Parameters
    ----------
    data : Orange.data.Table
        The input data.
    progress_callback : function
        A callback function to track progress.

    Returns
    -------
    list of lists
        The rows of cleaned responses.
    """
    responses = []
    for i, row in enumerate(data):
        try:
            # Extract features and metas for the current row
            features = list(data[i])
            metas = list(data.metas[i])

            # Call the completion API to get the answer
            prompt = str(row["prompt"])
            for i in range(50):# try 50 time
                print("try to call gpt4all ",i)
                time.sleep(0.5)
                answer = call_completion_api("localhost:4891", prompt)
                if answer!=None:
                    break
            # Correct misencoded text and clean the response
            answer = clean_response(answer)

            # Append the answer to the metas list and the current row to the responses list
            metas.append(answer)
            responses.append(features + metas)
        except Exception:
            # If an error occurs, continue to the next row
            continue

        # If a progress callback is provided, call it with the progress value
        if progress_callback:
            progress_value = 100 * (i + 1) / len(data)
            print(progress_value)
            progress_callback(progress_value)

    # If no responses were generated, return None
    if not responses:
        return None

    # Return the rows of cleaned responses
    return responses

def get_model_in_gpt4all():
    """
    Get the name of the model in GPT4All.

    Returns
    -------
    str or None
        The name of the model if it exists, None otherwise.
    """
    # Define the path to the directory containing the models
    model_path = os.path.join(get_local_store_path(), "Models") + "/NLP"
    if os.path.isdir(model_path)==False:
        return
    # Iterate over the files in the directory
    for filename in os.listdir(model_path):
        # Check if the file name contains "solar" and ends with ".gguf"
        if "solar" in filename and filename.endswith(".gguf"):
            # Return the filename if it meets the conditions
            return filename
    # If no file meets the conditions, return None
    return None



def get_latest_version_from_xml(file_path, package_name="gpt4all"):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Search for the specific package and extract its version
        for package in root.findall('Package'):
            name = package.find('Name').text
            if name == package_name:
                version = package.find('Version').text
                return version
        return None  # If package not found
    except Exception as e:
        print(f"Error: {e}")
        return None

def modify_gpt4all_config():
    """
    Modify the GPT4All configuration to set the GPU device, enable server mode, and configure network settings.

    The function reads the existing configuration file, if it exists, and modifies the necessary sections to set the
    GPU device, server mode, model, and network settings. If a section does not exist, it is created.

    The configuration file is located at `os.getenv('APPDATA')/nomic.ai/GPT4All.ini`.

    Returns:
        None
    """
    if os.name != "nt":
        print("-------------------------------------")
        print("WARNING: Auto config file not provided for OS != Windows, please configure GPT4ALL before using these widgets")
        print("-------------------------------------")
        return

    config_file_path = get_gpt4all_ini_path()
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    gpu_name = get_gpu_name()
    model_name = get_model_in_gpt4all()
    local_store_path = get_local_store_path()
    model_path = os.path.join(local_store_path, "Models", "NLP").replace("\\", "/")
    GPT_version = get_latest_version_from_xml(expanduser("~") + r"\gpt4all\components.xml")

    config = configparser.ConfigParser()

    if os.path.exists(config_file_path):
        try:
            config.read(config_file_path)
        except Exception as e:
            print("Error reading config file:", e)
            print("Creating a new config file...")
            os.remove(config_file_path)

    if not config.has_section('General'):
        config.add_section('General')
    config['General'].update({
        'device': gpu_name if gpu_name else '',
        'serverChat': 'true',
        'userDefaultModel': model_name if model_name else '',
        'modelPath': model_path
    })

    model_section = f"model-{model_name}"
    if not config.has_section(model_section):
        config.add_section(model_section)
    config[model_section].update({
        'filename': str(model_name),
        'contextLength': '4096',
    })

    if not config.has_section('download'):
        config.add_section('download')
    config['download']['lastVersionStarted'] = str(GPT_version)

    if not config.has_section('network'):
        config.add_section('network')
    config['network'].update({
        'usageStatsActive': 'false',
        'isActive': 'false'
    })

    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
        print("writing config file to: ", config_file_path)

def is_process_running(process_name):
    """
    Check if a process with the given name is already running.

    Parameters:
    process_name (str): The name of the process to check.

    Returns:
    bool: True if a process with the given name is running, False otherwise.
    """

    # Iterate over the running processes and check if the process name matches.
    for process in psutil.process_iter(['name']):
        # Convert both the process name and the given process name to lowercase for case-insensitive comparison.
        if process_name.lower() in process.info['name'].lower():
            # If a match is found, return True.
            return True

    # If no match is found, return False.
    return False


def call_completion_api(localhost, message_content):
    """Calls the GPT4All completion API and returns the response."""
    print(f"Sending message to GPT-4All: {message_content}")
    #/!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
    # do not change the calling method because to date (year 2024) it is the
    # only method that can be configured with all computer environments
    #/!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\





    command = [
        "curl",
        "--noproxy", "*",
        "--location",
        f"http://{localhost}/v1/chat/completions",
        "--header",
        "Content-Type: application/json; charset=UTF-8",
        "--data",
        json.dumps({
            "temperature": 0.7,
            "model": "solar-10.7b-instruct-v1.0.Q6_K.gguf",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": message_content}]
        }, ensure_ascii=False)
    ]

    try:
        os_type = os.name
        # shell = False to use special character as "<" etc
        if os_type == "nt":
            # writing a timestamp to a time file
            write_time_in_tempfile()
            print("#########",command)
            # Adding the `creationflags` parameter to suppress the CMD window
            response = subprocess.check_output(
                command,
                universal_newlines=True,
                shell=False,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW,  # Prevents the CMD window from appearing
            )
            print("--------->", response)
            return response
        elif str(os.uname().sysname) == "Darwin":  # machintosh
            import requests
            # Define the request data to be sent to the API.
            request_data = {
                "temperature": 0.7,  # The temperature value for the API response.
                "model": "solar-10.7b-instruct-v1.0.Q6_K.gguf",  # The model to be used by the API.
                "max_tokens": 4096,  # The maximum number of tokens in the API response.
                "messages": [{"role": "user", "content": message_content}]  # The message to be sent to the API.
            }
            request_url = f"http://{localhost}/v1/chat/completions"
            request_headers = {"Content-Type": "application/json; charset=UTF-8"}
            response=None
            timeout=0
            try:
                # Send the POST request to the API with the request data.
                response = requests.post(
                    request_url,
                    headers=request_headers,
                    data=json.dumps(request_data),
                )

                # Raise an HTTPError if the request fails.
                response.raise_for_status()
                print("reponse (1)",response)
                # Return the response from the API.
                return response.text
            except Exception as e:
                # Print the error that occurred during the request and return None.
                print(f"Error during API call: {e}")
                timeout+=1
                response=None
        else:
            print("platform not suported")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error during API call: {e}")
        return None




def get_gpu_name():
    import subprocess
    import platform
    """
    Checks if an NVIDIA GPU is present on the system and retrieves its name.

    This function uses platform-specific commands to check for a GPU:
    - Windows: Uses 'wmic' and 'nvidia-smi'.
    - macOS: Uses 'system_profiler' and 'nvidia-smi' if NVIDIA GPUs are supported.
    - Linux (Ubuntu): Uses 'lspci' and 'nvidia-smi'.

    Returns:
        str: The GPU name prefixed with "CUDA: " if a GPU is found.
        None: If no GPU is found or an error occurs.
    """
    try:
        os_type = platform.system()

        if os_type == "Windows":
            # Check for GPU on Windows using wmic
            wmic_output = subprocess.check_output(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                text=True
            )
            if "NVIDIA" not in wmic_output:
                return None
        elif os_type == "Darwin":  # macOS
            # Check for GPU on macOS using system_profiler
            sp_output = subprocess.check_output(
                ['system_profiler', 'SPDisplaysDataType'],
                text=True
            )
            print(sp_output)
            if "NVIDIA" not in sp_output:
                return None
        elif os_type == "Linux":
            # Check for GPU on Linux using lspci
            lspci_output = subprocess.check_output(
                ['lspci'],
                text=True
            )
            if "NVIDIA" not in lspci_output:
                return None
        else:
            return None

        # If NVIDIA GPU is found, use nvidia-smi to get the GPU name
        nvidia_smi_output = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
            text=True
        )
        gpu_name = nvidia_smi_output.strip()
        return "CUDA: " + gpu_name

    except FileNotFoundError:
        # Command not found (wmic, system_profiler, lspci, or nvidia-smi)
        return None
    except subprocess.CalledProcessError:
        # If an error occurs while running the command, return None.
        return None
    except Exception:
        # Catch any other unexpected errors
        return None

def clean_response(response_data):
    """
    Cleans the response text by removing special characters and correcting encoding issues.

    Parameters:
    response_data (str): The response data from the API.

    Returns:
    str: The cleaned and corrected response text.
    """
    try:
        # Parse the response data as JSON
        data = json.loads(response_data)

        # Extract the message content from the response
        choices = data.get("choices", [{}])
        message_content = choices[0].get("message", {}).get("content", "") if choices else ""

        # Remove unwanted characters from the message content
        cleaned_text = re.sub(r'[^\w\s,.!?\'"àâçéèêëîïôûùüÿÀÂÇÉÈÊËÎÏÔÛÙÜŸ-]', '', message_content)

        # Correct the encoding issues in the cleaned text using ftfy
        corrected_text = ftfy.fix_text(cleaned_text)

        # Return the stripped corrected text
        return corrected_text.strip()

    except (json.JSONDecodeError, IndexError):
        # If an error occurs, return an empty string
        return ""
def correct_encoding(text):
    """
    Corrects misencoded text using ftfy.

    Parameters:
    text (str): The text to be corrected.

    Returns:
    str: The corrected text.
    """
    # Correct the encoding issues in the text using ftfy
    corrected_text = ftfy.fix_text(text)

    # Return the corrected text
    return corrected_text

def detect_encoding(file_path):
    """
    Detects the encoding of a file using the chardet library.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The detected encoding of the file.
    """
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file data
        file_data = file.read()

    # Detect the encoding of the file using chardet
    encoding_result = chardet.detect(file_data)

    # Return the detected encoding
    return encoding_result['encoding']

def extract_text_from_file(file_path):
    """
    Extracts and returns text content from a file with proper encoding detection.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The text content of the file.
    """
    # Define the supported encodings for the file
    supported_encodings = ['utf-8', 'latin-1', 'cp1252']

    # Iterate over the supported encodings
    for encoding in supported_encodings:
        try:
            # Open the file with the current encoding and read its content
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()

        # If a UnicodeDecodeError occurs, move to the next encoding
        except UnicodeDecodeError:
            continue

    # If no encoding works, return an empty string
    return ""

if __name__ == "__main__":
    modify_gpt4all_config()