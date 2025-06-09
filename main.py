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
sol = pygame.image.load("recursos/sol.png")
sol = pygame.transform.scale(sol, (200,200))
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
pontos = 0
posicao_espinhoX = 500
posicao_espinhoY = 800
velocidade_espinho = 1
direcao_espinho = -1 
travado = False
movimento_espinho = 0
pygame.mixer.music.load("recursos/musicaFundo.mp3")
pygame.mixer.music.play(-1)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                movimento = -5
            elif evento.key == pygame.K_RIGHT:
                movimento = 5
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                movimento = 0

    posicaoX += movimento
    if posicaoX <= -50:
        posicaoX = -50
    elif posicaoX >= 850:
        posicaoX = 850

    posicao_orbeY += velocidade_orbe
    if posicao_orbeY > 700:
        posicao_orbeY = -100
        pontos += 1
        som_orbe.play()
        velocidade_orbe += 1
        posicao_orbeX = random.randint(0, 950)

    posicao_fumacaY += velocidade_fumaca
    if posicao_fumacaY > 700:
        posicao_fumacaY = -100
        velocidade_fumaca += 1
        posicao_fumacaX = random.randint(0, 950)

    posicao_espinhoY += velocidade_espinho * direcao_espinho
    if posicao_espinhoY <= 550:
        direcao_espinho = 1  
    elif posicao_espinhoY >= 750:
        direcao_espinho = -1  
        posicao_espinhoY = 750
        posicao_espinhoX = random.randint(0, 850)

    tela.fill(branco)
    tela.blit(tela_jogo, (0, 0))
    tela.blit(personagem, (posicaoX, 450))
    tela.blit(orbe, (posicao_orbeX, posicao_orbeY))
    tela.blit(fumaca, (posicao_fumacaX, posicao_fumacaY))
    tela.blit(espinho, (posicao_espinhoX, posicao_espinhoY))
    texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
    tela.blit(texto, (20, 20))
    

    pygame.display.update()
    relogio.tick(60)