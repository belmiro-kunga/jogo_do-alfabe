import pygame

class Feedback:
    def __init__(self, mensagem, cor):
        self.mensagem = mensagem
        self.cor = cor
        self.tempo_inicio = pygame.time.get_ticks()
        self.duracao = 2000  # 2 segundos
        self.fonte = pygame.font.Font(None, 48)
    
    def desenhar(self, tela):
        """Desenha a mensagem de feedback na tela"""
        # Calcular transparência baseada no tempo
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = tempo_atual - self.tempo_inicio
        
        if tempo_passado < self.duracao:
            # Calcular alpha (255 = opaco, 0 = transparente)
            alpha = 255 * (1 - tempo_passado / self.duracao)
            
            # Criar superfície com o texto
            texto = self.fonte.render(self.mensagem, True, self.cor)
            
            # Criar superfície para o fundo
            fundo = pygame.Surface((texto.get_width() + 20, texto.get_height() + 20))
            fundo.fill((0, 0, 0))
            fundo.set_alpha(int(alpha * 0.5))
            
            # Desenhar fundo
            tela.blit(fundo, (tela.get_width()/2 - fundo.get_width()/2,
                            tela.get_height()/2 - fundo.get_height()/2))
            
            # Desenhar texto
            texto.set_alpha(int(alpha))
            tela.blit(texto, (tela.get_width()/2 - texto.get_width()/2,
                            tela.get_height()/2 - texto.get_height()/2))
        else:
            return False  # Feedback terminou
        
        return True  # Feedback ainda está ativo 