import os
import shutil
import subprocess
import psutil

def verificar_disco ():
    """Consulta o espaço total, usado e livre no drivel principal (C:)."""
    try:
        uso = psutil.disk_usage("C:\\")
        total_gb = round(uso.total / (1024 ** 3), 2)
        usado_gb = round(uso.used / (1024 ** 3), 2)
        livre_gb = round(uso.free / (1024 **3), 2)
        porcentagem = uso.percent

        return (
            f"Drive C: - Total: {total_gb} GB | "
            f"Usado: {usado_gb} GB ({porcentagem}%) | "
            f"Livre: {livre_gb} GB"
        )

    except Exception as e:
        return f"Erro ao acessar os dados de armazenamento: {str(e)}"


def abrir_programa(nome_programa: str):
    """Abre utilitários comuns do Windows pelo nome."""
    nome = nome_programa.lower().strip()

    atalhos = {

        # Ferramentas de Desenvolvimento e Design
        "vscode": "code",
        "vs code": "code",
        "visual studio code": "code",
        "gamemaker": "start GameMaker",
        "game maker": "start GameMaker",
        "krita": "start krita",
        "chitubox": "start CHITUBOX",

        # Comunicação e Redes
        "discord": "start discord:",
        "telegram": "start telegram:",
        "whatsapp": "start whatsapp:",

        # Navegadores de Internet
        "edge": "start msedge",
        "microsoft edge": "start msedge",
        "firefox": "start firefox",
        "navegador": "start firefox",

        # Multimédia e Som
        "spotify": "start spotify:",
        "musica": "start spotify:",

        # Plataformas de Jogos e Launchers
        "steam": "start steam:",
        "epic": "start com.epicgames.launcher:",
        "epic games": "start com.epicgames.launcher:",
        "prism launcher": "start prismlauncher",
        "minecraft": "start prismlauncher",

        # Segurança e Sistema
        "malwarebytes": "start malwarebytes",
        "antivirus": "start malwarebytes",
        "bloco de notas": "notepad.exe",
        "notepad": "notepad.exe",
        "calculadora": "calc.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "explorador": "explorer.exe",
        "ficheiros": "explorer.exe"

    }

    comando =  atalhos.get(nome, nome)

    try:
        subprocess.Popen(comando, shell=True)
        return f"Comando para abrir '{nome}' enviado com sucesso ao sistema operacional"
    except Exception as e:
        return f"Falha ao tentar executar '{nome}': {str(e)}"
    