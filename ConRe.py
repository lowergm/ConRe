#!/usr/bin/env python3

# Imports
import argparse

import sys
import subprocess
from io import StringIO

# Criar o parser
parser = argparse.ArgumentParser(description="ConRe ainda está em desenvolvimento, qualquer bug, mande em (github aqui)")

# Adicionar os argumentos
parser.add_argument("-r", "--run", help="Rodar o conre.cr e executar o container", action="store_true")

parser.add_argument("-m", "--main", help="Rodar o arquivo principal referenciado no conre.cr", action="store_true")

parser.add_argument("-i", "--init", help="Inicializar o container", action="store_true")

parser.add_argument("-v", "--version", help="Versão do ConRe", action="store_true")

args = parser.parse_args()

def run_command(comando: str):
    try:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = mystdout = StringIO()

        result = subprocess.run(comando, shell=True, check=True)
        print("\n\nComando executado com sucesso!")

        sys.stdout = old_stdout
    
        stdout_output = mystdout.getvalue()
    
        print(stdout_output, "\n\n")
    except Exception as e:
        print("Não foi possível executar o comando run")

def run_container():
    with open("conre.cr", "r", encoding="utf-8") as container:
        container_usavel = container.readlines()
    
    for linha in container_usavel:
        if "RUN_COMMAND" in linha:
            print(linha, "\n\n")
            linha_run_command = linha.split()
    for instrucao in linha_run_command:
        if "[" in instrucao:
            inicio_run_command = linha_run_command.index(instrucao)
    for instrucao in linha_run_command:
        if "]" in instrucao:
            fim_run_command = linha_run_command.index(instrucao) + 1
    comandos = linha_run_command[inicio_run_command:fim_run_command]
    comando_str = " ".join(comandos).strip("[]").replace("'","").replace(",", "")
    print("Executando o comando:", comando_str, "\n\n\n")
    run_command(comando_str)

def run_main():
    with open("conre.cr", "r") as container:
        linhas = container.readlines()
        for linha in linhas:
            if "MAIN:" in linha:
                print(linha, "\n\n")
                linha_main = linha.split()
                arquivo_main = linha_main[1]
                print("\n\n")
        if arquivo_main.endswith(".py"):
            run_command(f"python3 {arquivo_main}")

init_config = """MAIN: main.py
RUN_COMMAND: ['python3', 'main.py']
"""

def init_container():
    print("\n\n")
    print("""
\033[1;36;81mMAIN:\033[1;36;0m main.py
\033[1;36;81mRUN_COMMAND:\033[1;36;0m [\033[32m'python3'\033[0m, \033[32m'main.py'\033[0m]


""")
    with open("conre.cr", "w") as container:
        container.write(init_config)

if args.run:
	run_container()
if args.init:
    init_container()
if args.main:
    run_main()
if args.version:
    print("v1.0.0dev")
