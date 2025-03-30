import pygame
import math

class Mascote:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.estado = "normal"  # normal, feliz, triste
        self.tempo_estado = 0
        self.duracao_estado = 1000  # 1 segundo
        self.tamanho = 60
        self.angulo = 0
        self.velocidade_rotacao = 2
        
        # Cores com alto contraste
        self.COR_NORMAL = (0, 0, 0)  # Preto
        self.COR_FELIZ = (0, 100, 0)  # Verde escuro
        self.COR_TRISTE = (139, 0, 0)  # Vermelho escuro
        self.COR_FUNDO = (255, 255, 255)  # Branco
        self.COR_CORPO = (255, 255, 0)  # Amarelo
        self.COR_OLHOS = (0, 0, 0)  # Preto
        self.COR_LAGRIMA = (0, 191, 255)  # Azul claro
    
    def atualizar(self):
        """Atualiza o estado e animação do mascote"""
        # Atualizar rotação
        self.angulo = (self.angulo + self.velocidade_rotacao) % 360
        
        # Atualizar estado temporário
        if self.estado != "normal":
            self.tempo_estado += 16  # aproximadamente 60 FPS
            if self.tempo_estado >= self.duracao_estado:
                self.estado = "normal"
                self.tempo_estado = 0
    
    def desenhar(self, tela):
        """Desenha o mascote na tela"""
        # Desenhar corpo (círculo)
        pygame.draw.circle(tela, self.COR_CORPO, (self.x, self.y), self.tamanho)
        
        # Desenhar olhos e expressão baseado no estado
        if self.estado == "feliz":
            # Olhos felizes (arcos para cima)
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x - 25, self.y - 20, 20, 20),
                          math.pi, 2 * math.pi, 2)
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x + 5, self.y - 20, 20, 20),
                          math.pi, 2 * math.pi, 2)
            
            # Sorriso
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x - 20, self.y - 10, 40, 30),
                          0, math.pi, 2)
        
        elif self.estado == "triste":
            # Olhos tristes (arcos para baixo)
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x - 25, self.y - 20, 20, 20),
                          0, math.pi, 2)
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x + 5, self.y - 20, 20, 20),
                          0, math.pi, 2)
            
            # Lágrimas
            pygame.draw.rect(tela, self.COR_LAGRIMA,
                           (self.x - 20, self.y, 4, 10))
            pygame.draw.rect(tela, self.COR_LAGRIMA,
                           (self.x + 15, self.y, 4, 10))
            
            # Boca triste
            pygame.draw.arc(tela, self.COR_OLHOS,
                          (self.x - 20, self.y, 40, 30),
                          math.pi, 2 * math.pi, 2)
        
        else:  # normal
            # Olhos normais (círculos)
            pygame.draw.circle(tela, self.COR_OLHOS,
                             (self.x - 15, self.y - 10), 5)
            pygame.draw.circle(tela, self.COR_OLHOS,
                             (self.x + 15, self.y - 10), 5)
            
            # Boca neutra
            pygame.draw.line(tela, self.COR_OLHOS,
                           (self.x - 10, self.y + 10),
                           (self.x + 10, self.y + 10), 2)
    
    def set_estado(self, estado):
        """Define o estado do mascote"""
        if estado in ["normal", "feliz", "triste"]:
            self.estado = estado
            self.tempo_estado = 0 