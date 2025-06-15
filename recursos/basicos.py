import os, time, json, pyttsx3
from datetime import datetime
from tkinter import simpledialog
import speech_recognition as controladorVoz
import speech_recognition as sr
reconhecedor = sr.Recognizer()
engine = pyttsx3.init()

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

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

recognizer = controladorVoz.Recognizer()
def ouvir():
    with sr.Microphone() as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        falar("Diga seu nome agora.")
        print("Escutando...")
        try:
            audio = reconhecedor.listen(source, timeout=5, phrase_time_limit=5)
            nome = reconhecedor.recognize_google(audio, language="pt-BR")
            print("Você disse:", nome)
            return nome
        except sr.UnknownValueError:
            print("Não entendi o que foi dito.")
            falar("Não entendi. Por favor, digite seu nome.")
        except sr.WaitTimeoutError:
            print("Tempo de escuta esgotado.")
            falar("Tempo esgotado. Por favor, digite seu nome.")
        except sr.RequestError:
            print("Erro no serviço de reconhecimento.")
            falar("Erro de serviço. Digite seu nome.")
    return None

    
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