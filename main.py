import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.basicos import limpar_tela
from recursos.basicos import aguarde
from recursos.basicos import inicializarBancoDeDados
from recursos.basicos import escreverDados
import json

pygame.init()
pygame.mixer.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho )
pygame.display.set_caption("A Jornada de Luz")
icone = pygame.image.load("recursos/icone.jpeg")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
amarelo = (217, 211, 100)
tela_inicial = pygame.image.load("recursos/telaInicial.jpeg")
tela_inicial = pygame.transform.scale(tela_inicial, (1000,700))
personagem = pygame.image.load("recursos/personagem (2).png")
personagem = pygame.transform.scale(personagem, (250,250))
tempo_personagem = pygame.time.get_ticks()
travado = False
tempo_travado = 0  #armazenará o momento da colisão.
tela_jogo = pygame.image.load("recursos/telaJogo.jpeg")
tela_jogo = pygame.transform.scale(tela_jogo, (1000,700))
fonteMenu = pygame.font.SysFont("Bahnschirift Light",35)
fonteMorte = pygame.font.SysFont("Bahnschirift Light",120)
orbe = pygame.image.load("recursos/orbe (1).png")
orbe = pygame.transform.scale(orbe, (150,200))
espinho = pygame.image.load("recursos/espinho (1).png")
espinho = pygame.transform.scale(espinho, (150,200))
fumaca = pygame.image.load("recursos/fumaça (1).png")
fumaca = pygame.transform.scale(fumaca, (150,200))
sol = pygame.image.load("recursos/soll.png")
sol = pygame.transform.scale(sol, (200,200))
nuvem = pygame.image.load("recursos/nuvem3.png")
nuvem = pygame.transform.scale(nuvem, (200,200))
som_orbe = pygame.mixer.Sound("recursos/orbeSound.mp3")

posicaoX = 250
posicaoY = 0
movimento = 0
posicao_orbeX = 100
posicao_orbeY = -100
velocidade_orbe = 1
posicao_fumacaX = 400
posicao_fumacaY = -100
velocidade_fumaca = 1
posicao_espinhoX = 500
posicao_espinhoY = 800
velocidade_espinho = 1
posicaoNuvemX = 10
posicaoNuvemY = -80
posicaoSolX = 865
posicaoSolY = -50
direcao_espinho = -1 
travado = False
movimento_espinho = 0
pontos = 0
virar_esquerda = False
pygame.mixer.music.load("recursos/musicaFundo.mp3")
pygame.mixer.music.play(-1)
personagem_original = pygame.transform.scale(personagem, (250, 250))
personagem_atual = personagem_original
escala_sol = 1.0
direcao_escala = 1
escala_minima = 0.95
escala_maxima = 1.05
velocidade_pulsacao = 0.002

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
            elif evento.type == pygame.KEYDOWN:
                if not travado:
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
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if not travado:
                        movimento = 0

        if travado:
            movimento = 0

        posicaoX += movimento
        posicaoX = max(-50, min(posicaoX, 850))

        rect_persona = pygame.Rect(posicaoX, 450,200,300)
        rect_orbe = pygame.Rect(posicao_orbeX, posicao_orbeY, 120, 120)
        rect_fumaca = pygame.Rect(posicao_fumacaX, posicao_fumacaY, 120, 120)
        rect_espinho = pygame.Rect(posicao_espinhoX, posicao_espinhoY, 100,190)

        posicao_orbeY += velocidade_orbe
        if rect_persona.colliderect(rect_orbe):
            posicao_orbeY = -100
            pontos += 1
            som_orbe.play()
            velocidade_orbe += 1
            posicao_orbeX = random.randint(0, 950)
        elif posicao_orbeY > 700:
            posicao_orbeY = -100
            velocidade_orbe += 1
            posicao_orbeX = random.randint(0, 950)

        posicao_fumacaY += velocidade_fumaca
        if rect_persona.colliderect(rect_fumaca):
            posicao_fumacaY = -100
            pontos -= 1
            velocidade_fumaca += 1
            posicao_fumacaX = random.randint(0, 950)
        elif posicao_fumacaY > 700:
            posicao_fumacaY = -100
            velocidade_fumaca += 1
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

jogar()
