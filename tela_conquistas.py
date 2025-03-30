import pygame
import math

class TelaConquistas:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.LARGURA = largura
        self.ALTURA = altura
        
        # Cores
        self.COR_FUNDO = (230, 243, 255)
        self.COR_TEXTO = (44, 62, 80)
        self.COR_TITULO = (231, 76, 60)
        self.COR_ESTRELA = (255, 215, 0)
        self.COR_ESTRELA_VAZIA = (189, 195, 199)
        self.COR_DESBLOQUEADO = (46, 204, 113)
        self.COR_BLOQUEADO = (189, 195, 199)
        
        # Fontes
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_texto = pygame.font.Font(None, 36)
        self.fonte_info = pygame.font.Font(None, 24)
        
        # Configurações de animação
        self.angulo_estrela = 0
        self.velocidade_rotacao = 3
        self.tamanho_estrela = 30
        
        # Estado
        self.mostrando_certificado = False
        self.tempo_certificado = 0
        self.duracao_certificado = 5000  # 5 segundos

    def desenhar_estrela(self, x, y, tamanho, angulo, cor):
        """Desenha uma estrela na posição especificada"""
        pontos = []
        for i in range(5):
            angulo_atual = angulo + i * 72
            raio = tamanho if i % 2 == 0 else tamanho * 0.4
            px = x + raio * math.cos(math.radians(angulo_atual))
            py = y + raio * math.sin(math.radians(angulo_atual))
            pontos.append((px, py))
        pygame.draw.polygon(self.tela, cor, pontos)

    def desenhar_conquistas(self, conquistas, estrelas_nivel):
        """Desenha a tela de conquistas"""
        self.tela.fill(self.COR_FUNDO)
        
        # Título
        titulo = self.fonte_titulo.render("Suas Conquistas!", True, self.COR_TITULO)
        titulo_rect = titulo.get_rect(center=(self.LARGURA/2, 50))
        self.tela.blit(titulo, titulo_rect)
        
        # Estrelas por nível
        y = 150
        for nivel in range(1, 6):
            nivel_texto = self.fonte_texto.render(f"Nível {nivel}", True, self.COR_TEXTO)
            self.tela.blit(nivel_texto, (50, y))
            
            # Desenhar estrelas
            for i in range(3):
                x = 200 + i * 60
                cor = self.COR_ESTRELA if i < estrelas_nivel[nivel] else self.COR_ESTRELA_VAZIA
                self.desenhar_estrela(x, y + 20, self.tamanho_estrela, self.angulo_estrela, cor)
            
            y += 80
        
        # Conquistas desbloqueadas
        y = 150
        for categoria, items in conquistas.items():
            categoria_texto = self.fonte_texto.render(categoria.title(), True, self.COR_TEXTO)
            self.tela.blit(categoria_texto, (400, y))
            
            y += 40
            for item, info in items.items():
                cor = self.COR_DESBLOQUEADO if info['desbloqueado'] else self.COR_BLOQUEADO
                item_texto = self.fonte_info.render(info['nome'], True, cor)
                self.tela.blit(item_texto, (420, y))
                y += 30
        
        # Atualizar ângulo da estrela
        self.angulo_estrela = (self.angulo_estrela + self.velocidade_rotacao) % 360

    def desenhar_certificado(self, certificado):
        """Desenha o certificado de conclusão"""
        self.tela.fill(self.COR_FUNDO)
        
        # Borda do certificado
        pygame.draw.rect(self.tela, self.COR_TEXTO, (50, 50, self.LARGURA-100, self.ALTURA-100), 3)
        
        # Título
        titulo = self.fonte_titulo.render("Certificado de Conclusão", True, self.COR_TITULO)
        titulo_rect = titulo.get_rect(center=(self.LARGURA/2, 100))
        self.tela.blit(titulo, titulo_rect)
        
        # Nome do jogador
        nome_texto = self.fonte_texto.render(f"Parabéns, {certificado['nome']}!", True, self.COR_TEXTO)
        nome_rect = nome_texto.get_rect(center=(self.LARGURA/2, 200))
        self.tela.blit(nome_texto, nome_rect)
        
        # Data
        data_texto = self.fonte_info.render(f"Data: {certificado['data']}", True, self.COR_TEXTO)
        data_rect = data_texto.get_rect(center=(self.LARGURA/2, 250))
        self.tela.blit(data_texto, data_rect)
        
        # Total de estrelas
        estrelas_texto = self.fonte_texto.render(f"Total de Estrelas: {certificado['total_estrelas']}", True, self.COR_ESTRELA)
        estrelas_rect = estrelas_texto.get_rect(center=(self.LARGURA/2, 300))
        self.tela.blit(estrelas_texto, estrelas_rect)
        
        # Estrelas por nível
        y = 400
        for nivel, estrelas in certificado['estrelas_por_nivel'].items():
            nivel_texto = self.fonte_info.render(f"Nível {nivel}: {estrelas} estrelas", True, self.COR_TEXTO)
            self.tela.blit(nivel_texto, (100, y))
            y += 30
        
        # Conquistas desbloqueadas
        y = 400
        for categoria, items in certificado['conquistas_desbloqueadas'].items():
            if items:
                categoria_texto = self.fonte_info.render(f"{categoria.title()}: {', '.join(items)}", True, self.COR_DESBLOQUEADO)
                self.tela.blit(categoria_texto, (400, y))
                y += 30

    def mostrar_certificado(self, certificado):
        """Inicia a exibição do certificado"""
        self.mostrando_certificado = True
        self.tempo_certificado = pygame.time.get_ticks()
        self.certificado = certificado

    def atualizar(self):
        """Atualiza o estado da tela"""
        if self.mostrando_certificado:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_certificado >= self.duracao_certificado:
                self.mostrando_certificado = False
                return True
        return False 