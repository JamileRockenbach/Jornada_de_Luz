import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox, font
import ctypes
from recursos.basicos import limpar_tela, aguarde, inicializarBancoDeDados, escreverDados
import json
from PIL import Image, ImageTk

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
amarelo = (197, 162, 124)

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

som_orbe = pygame.mixer.Sound("recursos/orbeSound.mp3")
fonteMenu = pygame.font.SysFont("Bahnschrift", 25)

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
pygame.mixer.music.load("recursos/musicaFundo.mp3")
pygame.mixer.music.play(-1)

personagem_original = personagem
personagem_atual = personagem_original
escala_sol = 1.0
direcao_escala = 1
escala_minima = 0.95
escala_maxima = 1.05
velocidade_pulsacao = 0.002
posicaoNuvemX, posicaoNuvemY = 10, -80
posicaoSolX, posicaoSolY = 865, -50

def jogar():
    global movimento, posicaoX, posicao_orbeX, posicao_orbeY
    global posicao_fumacaX, posicao_fumacaY, posicao_espinhoX, posicao_espinhoY
    global velocidade_orbe, velocidade_fumaca, direcao_espinho
    global pontos, travado, tempo_travado, personagem_atual
    global virar_esquerda, posicaoNuvemX, escala_sol, direcao_escala

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and not travado:
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
            posicao_fumacaY = -100
            pontos -= 1
            posicao_fumacaX = random.randint(0, 950)
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
        tela.blit(texto, (20, 20))

        pygame.display.update()
        relogio.tick(60)

def iniciar_jogo():
    root.destroy()
    jogar()

def mostrar_tutorial():
    tutorial_window = tk.Toplevel(root)
    tutorial_window.title("Tutorial")
    tutorial_window.geometry("1000x700")

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
    objetivo_window.title("Tutorial")
    objetivo_window.geometry("1000x700")

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
    messagebox.showinfo("Histórico", "Funcionalidade em desenvolvimento.")

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
    root.title("Bem-Vindos a Jornada de Luz!")

    icone_ico_path = os.path.abspath("recursos/icone.png")
    
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
    label_fundo.image = imagem_fundo  # para evitar garbage collection
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

if __name__ == "__main__":
    menu()
