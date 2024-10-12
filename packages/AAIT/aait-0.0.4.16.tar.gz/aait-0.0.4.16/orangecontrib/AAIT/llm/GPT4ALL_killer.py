import os
import time


# A faire: Ecrire à quoi ça sert. 
def exit_chat_exe():
    ldc = '"taskkill /im chat.exe /t /f"'
    try:
        os.system(ldc)
    except Exception as e:
        print(e)
        print(e)


def need_to_quit(delta_time_in_second):
    # Obtenir le chemin du répertoire temp de Windows
    temp_dir = os.getenv('TEMP')

    # Créer le nom complet du fichier
    file_path = os.path.join(temp_dir, 'date_heure.txt')

    try:
        with open(file_path, 'r') as file:
            stored_time_seconds = int(file.read())

        current_time_seconds = int(time.time())
        time_difference = abs(current_time_seconds - stored_time_seconds)
        print(f"Temps écoulé depuis la dernière écriture : {time_difference} secondes")
        if time_difference < delta_time_in_second:
            return False
    except FileNotFoundError:
        print("File date_heure.txt not found")

        ## si le fichier n'existe pas on quitte pour éviter la fermeture si l'utisateur veut se servir de 4all
        return True
    return True


if os.name != 'nt':
    print("only windows -> exiting")
    exit(0)

print("debut attente")
time.sleep(30)
while True:
    # si horodatage non mis à jour au bout 1h on kill and quit
    if need_to_quit(3600) == True:
        print("need to quit")
        exit_chat_exe()
        exit(0)
    time.sleep(10)
print("fin attente")
