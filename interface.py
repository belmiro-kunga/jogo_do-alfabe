import pygame

class Interface:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_grande = pygame.font.Font(None, 48)
        
        # Cores com alto contraste
        self.COR_FUNDO = (255, 255, 255)  # Fundo branco
        self.COR_TEXTO = (0, 0, 0)  # Texto preto
        self.COR_PONTUACAO = (0, 0, 139)  # Azul escuro
        self.COR_VIDAS = (139, 0, 0)  # Vermelho escuro
        self.COR_NIVEL = (0, 100, 0)  # Verde escuro
        self.COR_MODO = (128, 0, 128)  # Roxo escuro
        self.COR_SELECIONADO = (0, 0, 139)  # Azul escuro para seleção
    
    def desenhar_hud(self, pontuacao, vidas, nivel, modo_facil=False):
        """Desenha o HUD (Heads-Up Display) do jogo"""
        # Fundo branco para o HUD
        pygame.draw.rect(self.tela, self.COR_FUNDO, (5, 5, 200, 160))
        
        # Desenhar pontuação
        texto_pontuacao = self.fonte.render(f"Pontuação: {pontuacao}", True, self.COR_PONTUACAO)
        self.tela.blit(texto_pontuacao, (10, 10))
        
        # Desenhar vidas
        texto_vidas = self.fonte.render(f"Vidas: {vidas}", True, self.COR_VIDAS)
        self.tela.blit(texto_vidas, (10, 50))
        
        # Desenhar nível
        texto_nivel = self.fonte.render(f"Nível: {nivel}", True, self.COR_NIVEL)
        self.tela.blit(texto_nivel, (10, 90))
        
        # Desenhar modo de jogo
        modo = "Modo Fácil" if modo_facil else "Modo Normal"
        texto_modo = self.fonte.render(modo, True, self.COR_MODO)
        self.tela.blit(texto_modo, (10, 130))
    
    def desenhar_mensagem(self, mensagem, cor, posicao=None):
        """Desenha uma mensagem na tela"""
        # Fundo branco para a mensagem
        texto = self.fonte_grande.render(mensagem, True, cor)
        rect = texto.get_rect()
        if posicao is None:
            rect.center = (self.tela.get_width()/2, self.tela.get_height()/2)
        else:
            rect.center = posicao
        
        # Adicionar padding ao fundo
        padding = 20
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto, rect)
    
    def desenhar_instrucoes(self, nivel):
        """Desenha as instruções do nível atual"""
        instrucoes = {
            1: "Digite a letra que aparece na tela",
            2: "Digite as sílabas que aparecem na tela",
            3: "Digite as palavras que aparecem na tela"
        }
        
        texto = self.fonte.render(instrucoes[nivel], True, self.COR_TEXTO)
        rect = texto.get_rect(center=(self.tela.get_width()/2, 30))
        
        # Fundo branco para as instruções
        padding = 10
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto, rect)
    
    def desenhar_feedback(self, mensagem, cor, posicao=None):
        """Desenha uma mensagem de feedback"""
        if posicao is None:
            posicao = (self.tela.get_width()/2, self.tela.get_height() - 50)
        self.desenhar_mensagem(mensagem, cor, posicao)
    
    def desenhar_tela_pausa(self):
        """Desenha a tela de pausa"""
        # Fundo branco com transparência
        superficie = pygame.Surface(self.tela.get_size())
        superficie.fill(self.COR_FUNDO)
        superficie.set_alpha(200)
        self.tela.blit(superficie, (0, 0))
        
        # Desenhar mensagem de pausa
        self.desenhar_mensagem("JOGO PAUSADO", self.COR_TEXTO)
        
        # Desenhar instruções
        texto = self.fonte.render("Pressione ESC para continuar", True, self.COR_TEXTO)
        rect = texto.get_rect(center=(self.tela.get_width()/2, self.tela.get_height()/2 + 50))
        
        # Fundo branco para as instruções
        padding = 10
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto, rect)
    
    def desenhar_tela_fim_jogo(self, pontuacao, total_estrelas):
        """Desenha a tela de fim de jogo"""
        # Fundo branco com transparência
        superficie = pygame.Surface(self.tela.get_size())
        superficie.fill(self.COR_FUNDO)
        superficie.set_alpha(230)
        self.tela.blit(superficie, (0, 0))
        
        # Desenhar mensagem de fim de jogo
        self.desenhar_mensagem("FIM DE JOGO!", self.COR_TEXTO, (self.tela.get_width()/2, 200))
        
        # Desenhar pontuação final
        texto_pontuacao = self.fonte_grande.render(f"Pontuação Final: {pontuacao}", True, self.COR_PONTUACAO)
        rect = texto_pontuacao.get_rect(center=(self.tela.get_width()/2, 300))
        
        # Fundo branco para a pontuação
        padding = 10
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto_pontuacao, rect)
        
        # Desenhar total de estrelas
        texto_estrelas = self.fonte_grande.render(f"Total de Estrelas: {total_estrelas}", True, self.COR_NIVEL)
        rect = texto_estrelas.get_rect(center=(self.tela.get_width()/2, 350))
        
        # Fundo branco para as estrelas
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto_estrelas, rect)
        
        # Desenhar instruções
        texto = self.fonte.render("Pressione ESC para voltar ao menu", True, self.COR_TEXTO)
        rect = texto.get_rect(center=(self.tela.get_width()/2, 450))
        
        # Fundo branco para as instruções
        fundo_rect = pygame.Rect(rect.x - padding, rect.y - padding, 
                               rect.width + padding * 2, rect.height + padding * 2)
        pygame.draw.rect(self.tela, self.COR_FUNDO, fundo_rect)
        
        self.tela.blit(texto, rect) 