import pygame
import random
import time
import math
import os
from conquistas import GerenciadorConquistas
from tela_conquistas import TelaConquistas
from interface import Interface
from letra import Letra
from mascote import Mascote
from sons import GerenciadorSons
from banco_dados import BancoDados

class Particula:
    def __init__(self, x, y, cor, velocidade_x, velocidade_y, tamanho):
        self.x = x
        self.y = y
        self.cor = cor
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.tamanho = tamanho
        self.vida = 1.0  # Vida da partícula (1.0 a 0.0)
        self.alpha = 255  # Transparência
        
        # Cores com alto contraste
        self.COR_ACERTO = (0, 100, 0)  # Verde escuro
        self.COR_ERRO = (139, 0, 0)  # Vermelho escuro
        self.COR_BONUS = (0, 0, 139)  # Azul escuro

    def atualizar(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.vida -= 0.02  # Velocidade de desvanecimento
        self.alpha = int(255 * self.vida)
        return self.vida > 0

    def desenhar(self, tela):
        superficie = pygame.Surface((self.tamanho * 2, self.tamanho * 2), pygame.SRCALPHA)
        pygame.draw.circle(superficie, (*self.cor, self.alpha), (self.tamanho, self.tamanho), self.tamanho)
        tela.blit(superficie, (self.x - self.tamanho, self.y - self.tamanho))

class FundoTematico:
    def __init__(self, nivel):
        self.nivel = nivel
        self.elementos = []
        self.criar_elementos()
        
        # Cores com alto contraste
        self.COR_NUVEM = (200, 200, 200)  # Cinza claro
        self.COR_TRONCO = (139, 69, 19)  # Marrom escuro
        self.COR_COPA = (0, 100, 0)  # Verde escuro
        self.COR_PREDIO = (128, 128, 128)  # Cinza escuro
        self.COR_JANELA = (0, 0, 0)  # Preto

    def criar_elementos(self):
        if self.nivel == 1:  # Céu com nuvens
            for _ in range(5):
                self.elementos.append({
                    'tipo': 'nuvem',
                    'x': random.randint(0, 800),
                    'y': random.randint(0, 300),
                    'velocidade': random.uniform(0.5, 1.5)
                })
        elif self.nivel == 2:  # Floresta
            for _ in range(3):
                self.elementos.append({
                    'tipo': 'arvore',
                    'x': random.randint(0, 800),
                    'y': 500
                })
        elif self.nivel == 3:  # Cidade
            for _ in range(4):
                self.elementos.append({
                    'tipo': 'predio',
                    'x': random.randint(0, 800),
                    'y': 500
                })

    def atualizar(self):
        if self.nivel == 1:  # Movimento das nuvens
            for elemento in self.elementos:
                elemento['x'] += elemento['velocidade']
                if elemento['x'] > 800:
                    elemento['x'] = -100
                    elemento['y'] = random.randint(0, 300)

    def desenhar(self, tela):
        if self.nivel == 1:
            for elemento in self.elementos:
                if elemento['tipo'] == 'nuvem':
                    pygame.draw.circle(tela, self.COR_NUVEM, (int(elemento['x']), int(elemento['y'])), 30)
                    pygame.draw.circle(tela, self.COR_NUVEM, (int(elemento['x'] + 20), int(elemento['y'])), 30)
                    pygame.draw.circle(tela, self.COR_NUVEM, (int(elemento['x'] + 40), int(elemento['y'])), 30)
        elif self.nivel == 2:
            for elemento in self.elementos:
                if elemento['tipo'] == 'arvore':
                    # Tronco
                    pygame.draw.rect(tela, self.COR_TRONCO, (elemento['x'], elemento['y'], 20, 100))
                    # Copa
                    pygame.draw.circle(tela, self.COR_COPA, (elemento['x'] + 10, elemento['y']), 40)
        elif self.nivel == 3:
            for elemento in self.elementos:
                if elemento['tipo'] == 'predio':
                    altura = random.randint(100, 200)
                    pygame.draw.rect(tela, self.COR_PREDIO, (elemento['x'], elemento['y'] - altura, 40, altura))
                    # Janelas
                    for i in range(3):
                        for j in range(4):
                            pygame.draw.rect(tela, self.COR_JANELA, 
                                          (elemento['x'] + 5 + j * 10, 
                                           elemento['y'] - altura + 20 + i * 30, 
                                           8, 20))

class JogoAlfabeto:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jogo do Alfabeto")
        
        # Cores com alto contraste
        self.COR_FUNDO = (255, 255, 255)  # Fundo branco
        self.COR_TEXTO = (0, 0, 0)  # Texto preto
        self.COR_ACERTO = (0, 100, 0)  # Verde escuro
        self.COR_ERRO = (139, 0, 0)  # Vermelho escuro
        self.COR_SELECIONADO = (0, 0, 139)  # Azul escuro para opção selecionada
        
        # Estado do jogo
        self.rodando = True
        self.pausado = False
        self.nivel = 1
        self.pontuacao = 0
        self.vidas = 3
        self.letras = []
        self.tempo_ultima_letra = time.time()
        self.intervalo_letras = 3.0  # segundos
        
        # Modo de jogo
        self.modo_facil = False
        
        # Componentes do jogo
        self.interface = Interface(self.tela)
        self.sons = GerenciadorSons()
        self.mascote = Mascote(700, 500)
        self.banco_dados = BancoDados()
        
        # Relógio para controle de FPS
        self.clock = pygame.time.Clock()
        
        # Nome do jogador
        self.nome_jogador = ""
        self.obtendo_nome = True
        self.selecionando_dificuldade = False
        
        # Estado do jogo
        self.jogo_terminado = False
        self.mostrando_resultados = False
        self.mostrando_ranking = False
    
    def obter_nome_jogador(self):
        """Obtém o nome do jogador e a dificuldade"""
        fonte = pygame.font.Font(None, 36)
        fonte_titulo = pygame.font.Font(None, 48)
        
        while self.obtendo_nome and self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if not self.selecionando_dificuldade and self.nome_jogador:
                            self.selecionando_dificuldade = True
                        elif self.selecionando_dificuldade:
                            self.obtendo_nome = False
                    elif evento.key == pygame.K_BACKSPACE:
                        if not self.selecionando_dificuldade:
                            self.nome_jogador = self.nome_jogador[:-1]
                    elif evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        self.modo_facil = not self.modo_facil
                    elif len(self.nome_jogador) < 20 and evento.unicode.isalnum() and not self.selecionando_dificuldade:
                        self.nome_jogador += evento.unicode
            
            self.tela.fill(self.COR_FUNDO)
            
            if not self.selecionando_dificuldade:
                # Tela de nome
                texto = fonte.render("Digite seu nome:", True, self.COR_TEXTO)
                nome = fonte.render(self.nome_jogador, True, self.COR_TEXTO)
                self.tela.blit(texto, (300, 250))
                self.tela.blit(nome, (300, 300))
                
                if self.nome_jogador:
                    texto_enter = fonte.render("Pressione ENTER para continuar", True, self.COR_TEXTO)
                    self.tela.blit(texto_enter, (300, 350))
            else:
                # Tela de seleção de dificuldade
                titulo = fonte_titulo.render("Selecione a Dificuldade", True, self.COR_TEXTO)
                self.tela.blit(titulo, (250, 200))
                
                modo_normal = fonte.render("Modo Normal", True, self.COR_SELECIONADO if not self.modo_facil else self.COR_TEXTO)
                modo_facil = fonte.render("Modo Fácil (Velocidade mais lenta)", True, self.COR_SELECIONADO if self.modo_facil else self.COR_TEXTO)
                
                self.tela.blit(modo_normal, (300, 300))
                self.tela.blit(modo_facil, (300, 350))
                
                texto_enter = fonte.render("Pressione ENTER para começar", True, self.COR_TEXTO)
                self.tela.blit(texto_enter, (300, 450))
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def criar_letra(self):
        """Cria uma nova letra em posição aleatória"""
        x = random.randint(100, self.largura - 100)
        # Velocidade base reduzida no modo fácil
        velocidade_base = 1.5 if self.modo_facil else 2.0
        velocidade = velocidade_base + self.nivel * 0.5
        return Letra(x, -50, velocidade, self.nivel)
    
    def atualizar(self):
        """Atualiza o estado do jogo"""
        # Criar novas letras
        tempo_atual = time.time()
        # Intervalo maior entre letras no modo fácil
        intervalo_base = 4.0 if self.modo_facil else 3.0
        if tempo_atual - self.tempo_ultima_letra > intervalo_base:
            self.letras.append(self.criar_letra())
            self.tempo_ultima_letra = tempo_atual
        
        # Atualizar letras
        for letra in self.letras[:]:
            letra.atualizar()
            if letra.y > self.altura:
                self.letras.remove(letra)
                self.vidas -= 1
                self.mascote.set_estado("triste")
                self.sons.tocar_efeito("erro")
                if self.vidas <= 0:
                    self.fim_jogo()
        
        # Atualizar mascote
        self.mascote.atualizar()
    
    def processar_eventos(self):
        """Processa eventos do jogo"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.mostrando_resultados or self.mostrando_ranking:
                        self.rodando = False
                    else:
                        self.pausado = not self.pausado
                elif evento.key == pygame.K_r and self.mostrando_resultados:
                    self.reiniciar_jogo()
                elif evento.key == pygame.K_TAB:
                    if self.mostrando_resultados:
                        self.mostrando_ranking = True
                    elif self.mostrando_ranking:
                        self.mostrando_ranking = False
                else:
                    self.processar_tecla(evento.unicode)
    
    def processar_tecla(self, tecla):
        """Processa tecla pressionada"""
        for letra in self.letras[:]:
            acertou, completa = letra.verificar_tecla(tecla)
            if acertou:
                if completa:
                    self.pontuacao += letra.valor * 10
                    self.letras.remove(letra)
                    self.mascote.set_estado("feliz")
                    self.sons.tocar_efeito("acerto")
                    if self.pontuacao >= self.nivel * 100:
                        self.proximo_nivel()
                else:
                    self.sons.tocar_efeito("digitou")
                break
    
    def proximo_nivel(self):
        """Avança para o próximo nível"""
        self.nivel += 1
        self.letras.clear()
        self.intervalo_letras = max(1.0, self.intervalo_letras - 0.5)
        self.sons.tocar_efeito("nivel")
        self.sons.tocar_musica_nivel(self.nivel)  # Troca a música para o novo nível
        
        # Mostrar mensagem de novo nível
        self.interface.desenhar_mensagem(f"Nível {self.nivel}!", self.COR_TEXTO)
        pygame.display.flip()
        time.sleep(2)  # Pausa de 2 segundos para mostrar a mensagem
    
    def fim_jogo(self):
        """Finaliza o jogo"""
        self.jogo_terminado = True
        self.mostrando_resultados = True
        self.sons.parar_musica()
        self.sons.tocar_efeito("tente_novamente")
        
        # Salva os dados da partida no banco de dados
        self.banco_dados.salvar_partida(self.nome_jogador, self.pontuacao, self.nivel, self.modo_facil)
    
    def reiniciar_jogo(self):
        """Reinicia o jogo"""
        self.nivel = 1
        self.pontuacao = 0
        self.vidas = 3
        self.letras.clear()
        self.tempo_ultima_letra = time.time()
        self.intervalo_letras = 3.0
        self.jogo_terminado = False
        self.mostrando_resultados = False
        self.sons.tocar_musica_nivel(1)
    
    def desenhar(self):
        """Desenha os elementos do jogo"""
        self.tela.fill(self.COR_FUNDO)
        
        # Desenhar interface
        self.interface.desenhar_hud(self.pontuacao, self.vidas, self.nivel, self.modo_facil)
        
        # Desenhar letras
        for letra in self.letras:
            letra.desenhar(self.tela)
        
        # Desenhar mascote
        self.mascote.desenhar(self.tela)
        
        # Desenhar mensagem de pausa
        if self.pausado:
            fonte = pygame.font.Font(None, 74)
            texto = fonte.render("PAUSADO", True, self.COR_TEXTO)
            rect = texto.get_rect(center=(self.largura/2, self.altura/2))
            self.tela.blit(texto, rect)
        
        # Desenhar tela de fim de jogo
        if self.mostrando_resultados:
            self.interface.desenhar_tela_fim_jogo(self.pontuacao, self.nivel)
            
            # Desenhar opções de reiniciar, ranking ou sair
            fonte = pygame.font.Font(None, 36)
            texto_reiniciar = fonte.render("Pressione R para jogar novamente", True, self.COR_TEXTO)
            texto_ranking = fonte.render("Pressione TAB para ver o ranking", True, self.COR_TEXTO)
            texto_sair = fonte.render("Pressione ESC para sair", True, self.COR_TEXTO)
            
            rect_reiniciar = texto_reiniciar.get_rect(center=(self.largura/2, 500))
            rect_ranking = texto_ranking.get_rect(center=(self.largura/2, 550))
            rect_sair = texto_sair.get_rect(center=(self.largura/2, 600))
            
            self.tela.blit(texto_reiniciar, rect_reiniciar)
            self.tela.blit(texto_ranking, rect_ranking)
            self.tela.blit(texto_sair, rect_sair)
        
        # Desenhar tela de ranking
        if self.mostrando_ranking:
            self.desenhar_ranking()
        
        pygame.display.flip()
    
    def desenhar_ranking(self):
        """Desenha a tela de ranking"""
        fonte_titulo = pygame.font.Font(None, 48)
        fonte = pygame.font.Font(None, 36)
        
        # Título
        titulo = fonte_titulo.render("Ranking dos Jogadores", True, self.COR_TEXTO)
        rect_titulo = titulo.get_rect(center=(self.largura/2, 50))
        self.tela.blit(titulo, rect_titulo)
        
        # Obter ranking
        ranking = self.banco_dados.obter_ranking()
        
        # Desenhar cada posição do ranking
        y = 150
        for i, (nome, pontuacao, nivel, partidas) in enumerate(ranking, 1):
            texto = fonte.render(f"{i}. {nome} - {pontuacao} pontos (Nível {nivel}) - {partidas} partidas", 
                               True, self.COR_TEXTO)
            rect = texto.get_rect(center=(self.largura/2, y))
            self.tela.blit(texto, rect)
            y += 40
        
        # Opções
        texto_voltar = fonte.render("Pressione TAB para voltar", True, self.COR_TEXTO)
        texto_sair = fonte.render("Pressione ESC para sair", True, self.COR_TEXTO)
        
        rect_voltar = texto_voltar.get_rect(center=(self.largura/2, 550))
        rect_sair = texto_sair.get_rect(center=(self.largura/2, 600))
        
        self.tela.blit(texto_voltar, rect_voltar)
        self.tela.blit(texto_sair, rect_sair)
    
    def executar(self):
        """Executa o loop principal do jogo"""
        self.obter_nome_jogador()
        self.sons.tocar_musica_nivel(1)  # Começa com a música do nível 1
        
        while self.rodando:
            self.processar_eventos()
            
            if not self.pausado and not self.mostrando_resultados and not self.mostrando_ranking:
                self.atualizar()
            
            self.desenhar()
            self.clock.tick(60)
        
        # Fecha o banco de dados antes de encerrar
        self.banco_dados.fechar()
        pygame.quit()

if __name__ == "__main__":
    jogo = JogoAlfabeto()
    jogo.executar() 