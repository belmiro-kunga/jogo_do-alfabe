import os
import sys
import shutil
import subprocess
from pathlib import Path

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def criar_executavel():
    """Cria o executável do jogo"""
    print("Criando executável...")
    subprocess.check_call([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=imagens/icone.ico",
        "--add-data=imagens;imagens",
        "--add-data=sons;sons",
        "jogo_alfabeto.py"
    ])

def criar_atalho():
    """Cria um atalho na área de trabalho"""
    desktop = str(Path.home() / "Desktop")
    executavel = os.path.join("dist", "jogo_alfabeto.exe")
    
    if os.path.exists(executavel):
        # Cria o atalho na área de trabalho
        atalho = os.path.join(desktop, "Jogo do Alfabeto.lnk")
        if not os.path.exists(atalho):
            print("Criando atalho na área de trabalho...")
            shutil.copy2(executavel, atalho)
            print("Atalho criado com sucesso!")

def main():
    print("Iniciando instalação do Jogo do Alfabeto...")
    
    try:
        instalar_dependencias()
        criar_executavel()
        criar_atalho()
        
        print("\nInstalação concluída com sucesso!")
        print("Você pode encontrar o jogo em:")
        print("1. Na pasta 'dist' deste diretório")
        print("2. Na área de trabalho (atalho)")
        print("\nPara jogar, basta dar um duplo clique no ícone do jogo!")
        
    except Exception as e:
        print(f"\nErro durante a instalação: {str(e)}")
        print("Por favor, tente novamente ou contate o suporte.")
    
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main() 