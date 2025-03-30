import pygame
import random
import os

class Letra:
    def __init__(self, x, y, velocidade, nivel):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.nivel = nivel
        self.valor = self.gerar_valor()
        self.estado = "normal"
        self.letras_digitadas = []
        self.imagem = None
        
        # Configurações visuais
        self.tamanho = 48  # Aumentei o tamanho da fonte para melhor legibilidade
        self.fonte = pygame.font.Font(None, self.tamanho)
        
        # Cores com alto contraste
        self.COR_NORMAL = (0, 0, 0)  # Preto
        self.COR_ACERTO = (0, 100, 0)  # Verde escuro
        self.COR_ERRO = (139, 0, 0)  # Vermelho escuro
        self.COR_FUNDO = (255, 255, 255)  # Branco
        
        # Gerar conteúdo baseado no nível
        if nivel == 1:
            # Letras simples
            self.texto = chr(random.randint(65, 90))  # A-Z
        elif nivel == 2:
            # Sílabas simples
            silabas = ['BA', 'BE', 'BI', 'BO', 'BU',
                      'CA', 'CE', 'CI', 'CO', 'CU',
                      'DA', 'DE', 'DI', 'DO', 'DU',
                      'FA', 'FE', 'FI', 'FO', 'FU']
            self.texto = random.choice(silabas)
        else:
            # Palavras com imagens
            palavras = {
                'SOL': 'imagens/sol.png',
                'LUA': 'imagens/lua.png',
                'BOI': 'imagens/boi.png',
                'PÃO': 'imagens/pao.png',
                'UVA': 'imagens/uva.png'
            }
            self.texto = random.choice(list(palavras.keys()))
            # Carregar imagem se existir
            caminho_imagem = palavras[self.texto]
            if os.path.exists(caminho_imagem):
                self.imagem = pygame.image.load(caminho_imagem)
                self.imagem = pygame.transform.scale(self.imagem, (40, 40))
    
    def atualizar(self):
        """Atualiza a posição da letra"""
        self.y += self.velocidade
    
    def desenhar(self, tela):
        """Desenha a letra/sílaba/palavra na tela"""
        # Fundo branco para a letra
        texto_surface = self.fonte.render(self.texto, True, self.COR_NORMAL)
        rect = texto_surface.get_rect()
        rect.center = (self.x, self.y)
        
        # Adicionar padding ao fundo
        padding = 10
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(tela, self.COR_FUNDO, fundo_rect)
        
        tela.blit(texto_surface, rect)
        
        # Desenhar imagem se existir
        if self.imagem:
            imagem_rect = self.imagem.get_rect()
            imagem_rect.center = (self.x + texto_surface.get_width()/2 + 30, self.y)
            tela.blit(self.imagem, imagem_rect)
        
        # Desenhar letras já digitadas
        if self.letras_digitadas:
            digitadas = ''.join(self.letras_digitadas)
            digitadas_surface = self.fonte.render(digitadas, True, self.COR_ACERTO)
            digitadas_rect = digitadas_surface.get_rect()
            digitadas_rect.center = (self.x, self.y + 40)
            
            # Fundo branco para as letras digitadas
            padding = 10
            fundo_rect = pygame.Rect(digitadas_rect.x - padding, digitadas_rect.y - padding, 
                                   digitadas_rect.width + padding * 2, digitadas_rect.height + padding * 2)
            pygame.draw.rect(tela, self.COR_FUNDO, fundo_rect)
            
            tela.blit(digitadas_surface, digitadas_rect)
    
    def verificar_tecla(self, tecla):
        """Verifica se a tecla pressionada está correta"""
        tecla = tecla.upper()
        proximo_indice = len(self.letras_digitadas)
        
        if proximo_indice < len(self.texto) and tecla == self.texto[proximo_indice]:
            self.letras_digitadas.append(tecla)
            return True, len(self.letras_digitadas) == len(self.texto)
        
        return False, False
    
    def esta_completa(self):
        """Verifica se todas as letras foram digitadas"""
        return len(self.letras_digitadas) == len(self.texto)

    def gerar_valor(self):
        if self.nivel == 1:
            return 1
        elif self.nivel == 2:
            return 2
        else:
            return 3 