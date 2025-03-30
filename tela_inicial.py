import pygame

class TelaInicial:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.LARGURA = largura
        self.ALTURA = altura
        
        # Fontes
        self.fonte_titulo = pygame.font.Font(None, 48)
        self.fonte_texto = pygame.font.Font(None, 36)
        
        # Cores
        self.COR_FUNDO = (0, 0, 0)
        self.COR_TEXTO = (255, 255, 255)
        self.COR_TITULO = (255, 215, 0)
        self.COR_CURSOR = (255, 255, 255)
        
        # Estado
        self.nome = ""
        self.cursor_visivel = True
        self.tempo_cursor = 0
        self.duracao_cursor = 500  # Piscar a cada 0.5 segundos
        
    def atualizar(self):
        """Atualiza o estado da tela"""
        # Atualizar cursor piscante
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_cursor > self.duracao_cursor:
            self.cursor_visivel = not self.cursor_visivel
            self.tempo_cursor = tempo_atual
    
    def processar_evento(self, evento):
        """Processa eventos de teclado"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and self.nome:
                return True, self.nome  # Nome confirmado
            elif evento.key == pygame.K_BACKSPACE:
                self.nome = self.nome[:-1]
            elif len(self.nome) < 15 and evento.unicode.isalnum():
                self.nome += evento.unicode
        return False, self.nome
    
    def desenhar(self):
        """Desenha a tela inicial"""
        self.tela.fill(self.COR_FUNDO)
        
        # Título
        titulo = self.fonte_titulo.render("Jogo do Alfabeto", True, self.COR_TITULO)
        self.tela.blit(titulo, (self.LARGURA/2 - titulo.get_width()/2, 100))
        
        # Solicitar nome
        texto = self.fonte_texto.render("Digite seu nome!", True, self.COR_TEXTO)
        self.tela.blit(texto, (self.LARGURA/2 - texto.get_width()/2, 200))
        
        # Campo de nome
        nome_texto = self.nome
        if self.cursor_visivel:
            nome_texto += "|"
        nome_surface = self.fonte_texto.render(nome_texto, True, self.COR_TEXTO)
        self.tela.blit(nome_surface, (self.LARGURA/2 - nome_surface.get_width()/2, 250))
        
        # Instruções
        if self.nome:
            instrucao = self.fonte_texto.render("Pressione ENTER para começar!", True, self.COR_TEXTO)
            self.tela.blit(instrucao, (self.LARGURA/2 - instrucao.get_width()/2, 350))
        
        pygame.display.flip() 