import os
import json
import pygame
import random
import ctypes
import pyttsx3
import tkinter as tk
import speech_recognition as sr
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkinter import messagebox, font
from recursos.basicos import pedir_nome, ouvir, falar
from recursos.basicos import limpar_tela, aguarde, inicializarBancoDeDados, escreverDados

pygame.init()
pygame.mixer.init()
inicializarBancoDeDados()
tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("A Jornada de Luz")
icone = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
branco = (255, 255, 255)
preto = (0, 0, 0)

tela_inicial = pygame.image.load("recursos/telaInicial.png")
tela_inicial = pygame.transform.scale(tela_inicial, (1000, 700))
tela_jogo = pygame.image.load("recursos/telaJogo.jpeg")
tela_jogo = pygame.transform.scale(tela_jogo, (1000, 700))
tela_final = pygame.image.load("recursos/telaFinal.png")
tela_final = pygame.transform.scale(tela_final, (1000, 700))
tela_objetivo = pygame.image.load("recursos/objetivo.png")
tela_objetivo = pygame.transform.scale(tela_objetivo, (1000, 700))
tela_tutorial = pygame.image.load("recursos/tutorial1.png")
tela_tutorial = pygame.transform.scale(tela_tutorial, (1000, 700))
personagem = pygame.image.load("recursos/personagem (2).png")
personagem = pygame.transform.scale(personagem, (250, 250))
orbe = pygame.image.load("recursos/orbe (1).png")
orbe = pygame.transform.scale(orbe, (150, 200))
espinho = pygame.image.load("recursos/espinho (1).png")
espinho = pygame.transform.scale(espinho, (150, 200))
fumaca = pygame.image.load("recursos/fumaça (1).png")
fumaca = pygame.transform.scale(fumaca, (150, 200))
sol = pygame.image.load("recursos/sol5.png")
sol = pygame.transform.scale(sol, (200, 200))
nuvem = pygame.image.load("recursos/nuvem3.png")
nuvem = pygame.transform.scale(nuvem, (200, 200))
pause = pygame.image.load("recursos/pause.jpeg")
pause = pygame.transform.scale(pause, (1000, 700))

som_orbe = pygame.mixer.Sound("recursos/orbeSound.mp3")
fonteMenu = pygame.font.SysFont("Bahnschrift", 25)
pygame.mixer.music.load("recursos/musicaFundo.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.load("recursos/musicaFundo.mp3")
pygame.mixer.music.play(-1)
musicaFinal = "recursos/musicaFinal.mp3"
reconhecedor = sr.Recognizer()
engine = pyttsx3.init()

posicaoX = 250
movimento = 0
posicao_orbeX, posicao_orbeY = 100, -100
posicao_fumacaX, posicao_fumacaY = 400, -100
posicao_espinhoX, posicao_espinhoY = 500, 800
velocidade_orbe = velocidade_fumaca = 5
velocidade_espinho = 1
direcao_espinho = -1
travado = False
tempo_travado = 0
pontos = 0
virar_esquerda = False
pausado = False
personagem_original = personagem
personagem_atual = personagem_original
escala_sol = 1.0
direcao_escala = 1
escala_minima = 0.95
escala_maxima = 1.05
velocidade_pulsacao = 0.002
posicaoNuvemX, posicaoNuvemY = 10, -80
posicaoSolX, posicaoSolY = 865, -50
nome_jogador = ""
frases_morte = ['Você é mais forte do que pensa.',
                'Mesmo na escuridão, a luz interior brilha.',
                'Tentar novamente é um sinal de coragem.',
                'As quedas ensinam a levantar com mais firmeza.',
                'O importante é nunca desistir.',
                'Você está evoluindo, mesmo quando não percebe.',
                'Derrotas também fazem parte da jornada.',
                'Grandes vitórias nascem de pequenos fracassos.',
                'Tudo bem descansar, só não pare.',
                'A luz que você busca está dentro de você.',
                'Você tem potencial para superar qualquer desafio.',
                'A jornada é feita de altos e baixos. Continue.',
                'Não existe fracasso, apenas aprendizado.',
                'Cada tentativa te aproxima do seu objetivo.',
                'Recomeçar é sinal de força, não de fraqueza.',
                'Coragem é seguir em frente apesar do medo.',
                'Você já chegou longe. Continue.',
                'Só erra quem tenta, continue em frente!',
                'A luz volta a brilhar para quem não desiste.',
                'Você não está sozinho nessa caminhada.',
                'Acreditar em si é o primeiro passo.',
                'A derrota é só um capítulo, não o final da história.',
                'Grandes jornadas têm obstáculos. Supere-os.',
                'Se cair, levante mais forte, você consegue.',
                'Os dias difíceis também constroem heróis.',
                'Você é a esperança que o mundo precisa.',
                'Cada esforço vale a pena.',
                'Você já venceu muitas vezes antes. Vai vencer de novo.',
                'Toda escuridão passa e a luz volta!',
                'Confie no processo.',
                'Você faz a diferença.',
                'Erros constroem sabedoria.',
                'Nada é em vão quando se aprende.',
                'A luz está logo ali. Continue caminhando.',
                'Acredite: sua jornada inspira.',
                'O hoje é só um passo do amanhã brilhante.',
                'Desistir não combina com você.',
                'Sua força está nos seus recomeços.',
                'Nunca subestime sua capacidade de mudar.',
                'Sempre há uma nova chance.',
                'Cada fim traz um recomeço mais sábio.',
                'Respire fundo e recomece com o coração leve.',
                'Você está no caminho certo.',
                'Não tenha medo de errar. Tenha coragem de continuar.',
                'A escuridão só revela o brilho da sua luz.',
                'Seu esforço tem valor, mesmo que ninguém veja.',
                'A queda não te define, eu acredito em você!',
                'Persista, mesmo quando tudo parecer difícil.',
                'O brilho do amanhã começa com sua persistência hoje.']

def resetar_jogo():
    global movimento, posicaoX, posicao_orbeX, posicao_orbeY
    global posicao_fumacaX, posicao_fumacaY, posicao_espinhoX, posicao_espinhoY
    global velocidade_orbe, velocidade_fumaca, direcao_espinho
    global pontos, travado, tempo_travado, personagem_atual
    global virar_esquerda, posicaoNuvemX, escala_sol, direcao_escala
    global pausado

    movimento = 0
    posicaoX = 450

    posicao_orbeX = random.randint(0, 950)
    posicao_orbeY = -100

    posicao_fumacaX = random.randint(0, 950)
    posicao_fumacaY = -100

    posicao_espinhoX = random.randint(0, 850)
    posicao_espinhoY = 750
    direcao_espinho = -1

    velocidade_orbe = 5
    velocidade_fumaca = 7

    pontos = 0
    travado = False
    tempo_travado = 0
    personagem_atual = personagem_original
    virar_esquerda = False
    pausado = False

    posicaoNuvemX = -100
    escala_sol = 1.0
    direcao_escala = 1

def voltar_ao_menu():
        tela_morte.destroy()
        menu()
        return

def tela_morte():
    pygame.mixer.music.load("recursos/musicaFinal.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)

    fonte_titulo = pygame.font.SysFont("Bahnschrift", 60, bold=True)
    fonte_instrucao = pygame.font.SysFont("Bahnschrift", 30, bold=True)
    fonte_frase = pygame.font.SysFont("Impact", 35, bold=False)
    frase_escolhida = random.choice(frases_morte)
    fonte_agradecimento = pygame.font.SysFont("Impact", 30, bold=False)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    try:
                        root.destroy()
                    except:
                        pass
                    menu()
                elif evento.key == pygame.K_s:
                    pygame.quit()
                    quit()

        tela.blit(tela_final, (0, 0))
        texto_frase = fonte_frase.render(frase_escolhida, True, (9, 15, 43))
        tela.blit(texto_frase, (174, 60))
        instrucao_w = fonte_instrucao.render("Aperte W para voltar ao menu", True, (9, 15, 43))
        instrucao_s = fonte_instrucao.render("Aperte S para sair do jogo", True, (9, 15, 43))
        tela.blit(instrucao_w, (50, 300))
        tela.blit(instrucao_s, (50, 360))
        agradecimento = fonte_agradecimento.render("Obrigada por jogar!", True, (9, 15, 43))
        tela.blit(agradecimento, (tela.get_width() // 2 - agradecimento.get_width() // 2, tela.get_height() - 50))

        pygame.display.update()
        relogio.tick(60)

def jogar():
    pygame.mixer.music.load("recursos/musicaFundo.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)
    global movimento, posicaoX, posicao_orbeX, posicao_orbeY
    global posicao_fumacaX, posicao_fumacaY, posicao_espinhoX, posicao_espinhoY
    global velocidade_orbe, velocidade_fumaca, direcao_espinho
    global pontos, travado, tempo_travado, personagem_atual
    global virar_esquerda, posicaoNuvemX, escala_sol, direcao_escala
    global pausado
    global nome_jogador

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                if not pausado and not travado:
                    if evento.key == pygame.K_LEFT:
                        movimento = -5
                        if not virar_esquerda:
                            personagem_atual = pygame.transform.flip(personagem_original, True, False)
                            virar_esquerda = True
                    elif evento.key == pygame.K_RIGHT:
                        movimento = 5
                        if virar_esquerda:
                            personagem_atual = personagem_original
                            virar_esquerda = False
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT] and not travado:
                    movimento = 0

        if pausado:
            tela.blit(pause, (0,0))
            fonte_titulo = pygame.font.SysFont("Bahnschrift", 60, bold=True)
            texto_titulo = fonte_titulo.render("JOGO PAUSADO", True, (255, 255, 255))
            tela.blit(texto_titulo, (tela.get_width() // 2 - texto_titulo.get_width() // 2, 150))
            fonte_icone = pygame.font.SysFont("Arial", 100)
            icone_pausa = fonte_icone.render("⏸️⏸️", True, (200, 200, 200))
            tela.blit(icone_pausa, (tela.get_width() // 2 - icone_pausa.get_width() // 2, 250))
            fonte_instrucao = pygame.font.SysFont("Bahnschrift", 30)
            texto_instrucao = fonte_instrucao.render("Clique em 'espaço' para voltar à jornada", True, (180, 180, 180))
            tela.blit(texto_instrucao, (tela.get_width() // 2 - texto_instrucao.get_width() // 2, 400))

            pygame.display.update()
            relogio.tick(60)
            continue

        if travado:
            movimento = 0

        posicaoX += movimento
        posicaoX = max(-50, min(posicaoX, 850))

        rect_persona = pygame.Rect(posicaoX + 50, 470, 150, 250)
        rect_orbe = pygame.Rect(posicao_orbeX, posicao_orbeY, 120, 120)
        rect_fumaca = pygame.Rect(posicao_fumacaX, posicao_fumacaY, 120, 120)
        rect_espinho = pygame.Rect(posicao_espinhoX, posicao_espinhoY, 100, 190)

        posicao_orbeY += velocidade_orbe
        if rect_persona.colliderect(rect_orbe):
            posicao_orbeY = -100
            pontos += 1
            som_orbe.play()
            posicao_orbeX = random.randint(0, 950)
        elif posicao_orbeY > 700:
            posicao_orbeY = -100
            posicao_orbeX = random.randint(0, 950)

        posicao_fumacaY += velocidade_fumaca
        if rect_persona.colliderect(rect_fumaca):
            salvar_historico(nome_jogador, pontos)
            tela_morte()
            return
        elif posicao_fumacaY > 700:
            posicao_fumacaY = -100
            posicao_fumacaX = random.randint(0, 950)

        posicao_espinhoY += velocidade_espinho * direcao_espinho
        agora = pygame.time.get_ticks()

        if rect_persona.colliderect(rect_espinho) and not travado:
            travado = True
            tempo_travado = agora
            posicao_espinhoY = 750
            posicao_espinhoX = random.randint(0, 850)
            direcao_espinho = -1

        if not travado:
            if posicao_espinhoY <= 550:
                direcao_espinho = 1
            elif posicao_espinhoY >= 750:
                direcao_espinho = -1
                posicao_espinhoY = 750
                posicao_espinhoX = random.randint(0, 850)
        if travado and agora - tempo_travado >= 3000:
            travado = False

        posicaoNuvemX += 1
        if posicaoNuvemX > 1000:
            posicaoNuvemX = -200

        escala_sol += direcao_escala * velocidade_pulsacao
        if escala_sol >= escala_maxima or escala_sol <= escala_minima:
            direcao_escala *= -1
            escala_sol = max(min(escala_sol, escala_maxima), escala_minima)

        sol_pulsante = pygame.transform.scale(sol, (
            int(200 * escala_sol),
            int(200 * escala_sol)
        ))

        tela.fill(branco)
        tela.blit(tela_jogo, (0, 0))
        tela.blit(sol_pulsante, (posicaoSolX, posicaoSolY))
        tela.blit(nuvem, (posicaoNuvemX, posicaoNuvemY))
        tela.blit(personagem_atual, (posicaoX, 450))
        tela.blit(orbe, (posicao_orbeX, posicao_orbeY))
        tela.blit(fumaca, (posicao_fumacaX, posicao_fumacaY))
        tela.blit(espinho, (posicao_espinhoX, posicao_espinhoY))
        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        mensagemPause = fonteMenu.render("Press space to Pause Game", True, branco)
        tela.blit(texto, (20, 20))
        tela.blit(mensagemPause, (20, 45))

        pygame.display.update()
        relogio.tick(60)

def iniciar_jogo():
    global nome_jogador
    escolha = messagebox.askyesno("Entrada de Nome", "Deseja falar o nome em vez de digitar?")

    if escolha:
        pygame.mixer.music.stop()
        nome_voz = ouvir()
        if nome_voz:
            nome_jogador = nome_voz
        else:
            nome_jogador = simpledialog.askstring("Nome do Jogador", "Digite seu nome:", parent=root)
    else:
        nome_jogador = simpledialog.askstring("Nome do Jogador", "Digite seu nome:", parent=root)

    if nome_jogador:
        root.withdraw()
        resetar_jogo()
        jogar()
    else:
        messagebox.showinfo("Aviso", "Nome obrigatório para jogar.")

def mostrar_tutorial():
    tutorial_window = tk.Toplevel(root)
    tutorial_window.title("Tutorial")
    tutorial_window.geometry("1000x700")
    tutorial_window.iconbitmap("recursos/icone2.ico")
    imagem = Image.open("recursos/tutorial1.png")
    imagem_redimensionada = imagem.resize((1000, 700))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    label = tk.Label(tutorial_window, image=imagem_tk)
    label.image = imagem_tk 
    label.pack()

    botao_voltar = tk.Button(tutorial_window, text="Voltar ao Menu", command=tutorial_window.destroy,
                             bg="#080B21", fg="white", font=fonte_botoes)
    botao_voltar.place(x=690, y=545)

def mostrar_objetivo():
    objetivo_window = tk.Toplevel(root)
    objetivo_window.title("Objetivos")
    objetivo_window.geometry("1000x700")
    objetivo_window.iconbitmap("recursos/icone2.ico")

    imagem2 = Image.open("recursos/objetivo.png")
    imagem_redimensionada2 = imagem2.resize((1000, 700))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada2)

    label = tk.Label(objetivo_window, image=imagem_tk)
    label.image = imagem_tk 
    label.pack()

    botao_voltar = tk.Button(objetivo_window, text="Voltar ao Menu", command=objetivo_window.destroy,
                             bg="#080B21", fg="white", font=fonte_botoes)
    botao_voltar.place(x= 380, y=500)
    
def mostrar_historico():
    historico_window = tk.Toplevel(root)
    historico_window.title("Histórico de Jogadores")
    historico_window.geometry("600x400")
    historico_window.iconbitmap("recursos/icone2.ico")

    try:
        with open("log.dat", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        conteudo = "Nenhum histórico encontrado ainda."

    texto = tk.Text(historico_window, wrap="word", font=("Bahnschrift", 12))
    texto.insert("1.0", conteudo)
    texto.config(state="disabled")
    texto.pack(expand=True, fill="both", padx=10, pady=10)
    botao_voltar = tk.Button(historico_window, text="Fechar", command=historico_window.destroy,
                             bg="#080B21", fg="white", font=fonte_botoes)
    botao_voltar.pack(pady=10)

def sair_jogo():
    root.destroy()
    pygame.quit()
    quit()

def menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("recursos/musicaFundo.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)
    caminho_fonte = os.path.abspath("fonte.ttf")
    ctypes.windll.gdi32.AddFontResourceW(caminho_fonte)
    global root
    root = tk.Tk()
    root.title("Bem-Vindos a Jornada de Luz")
    root.iconbitmap("recursos/icone2.ico")
    
    global fonte_botoes
    fonte_titulo = font.Font(family="Bahnschrift", size=60, weight="bold")
    fonte_botoes = font.Font(family="Bahnschrift", size=25, weight="bold")

    largura = 1000
    altura = 700
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    posX = (largura_tela // 2) - (largura // 2) - 8
    posY = (altura_tela // 2) - (altura // 2) - 30

    root.geometry(f"{largura}x{altura}+{posX}+{posY}")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.after(10, lambda: root.attributes("-topmost", False))

    imagem_fundo = tk.PhotoImage(file="recursos/telaInicial.png")
    label_fundo = tk.Label(root, image=imagem_fundo)
    label_fundo.image = imagem_fundo
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
    imagem_original = Image.open("recursos/telaInicial.png")
    imagem_redimensionada = imagem_original.resize((1000, 700))
    imagem_fundo = ImageTk.PhotoImage(imagem_redimensionada)

    label_fundo = tk.Label(root, image=imagem_fundo)
    label_fundo.image = imagem_fundo 
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    botao_jogar = tk.Button(root, text="Jogar", command=iniciar_jogo, width=20, height=1, bg="#080B21", fg="white", font=fonte_botoes)
    botao_jogar.place(x=500, y=220)

    botao_tutorial = tk.Button(root, text="Tutorial", command=mostrar_tutorial, width=20, height=1, bg="#080B21", fg="white", font=fonte_botoes)
    botao_tutorial.place(x=500, y=300)

    botao_objetivo = tk.Button(root, text="Objetivos", command=mostrar_objetivo, width=20, height=1, bg="#080B21", fg="white", font=fonte_botoes)
    botao_objetivo.place(x=500, y=385)

    botao_historico = tk.Button(root, text="Histórico", command=mostrar_historico, width=20, height=1, bg="#080B21", fg="white", font=fonte_botoes)
    botao_historico.place(x=500, y=470)

    botao_sair = tk.Button(root, text="Sair", command=sair_jogo, width=20, height=2, bg="#080B21", fg="white", font=fonte_botoes)
    botao_sair.place(x=500, y=550)

    root.mainloop()

def salvar_historico(nome_jogador, pontos):
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{nome_jogador} | Pontos: {pontos} | Data e Hora: {data_hora}\n"

    with open("log.dat", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)

if __name__ == "__main__":
    menu()