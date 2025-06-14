import os, time
import json
from datetime import datetime
from tkinter import simpledialog

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)

def pedir_nome():
    global nome_jogador
    nome_jogador = simpledialog.askstring("Nome do Jogador", "Digite seu nome:")
    
def inicializarBancoDeDados():
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()