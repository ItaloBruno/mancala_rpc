from abc import ABC, abstractmethod


class InterfaceCliente(ABC):
    @abstractmethod
    def desistir_da_partida(self):
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self):
        pass

    @abstractmethod
    def definir_ganhador(self):
        pass

    @abstractmethod
    def criar_tela_do_jogador(self):
        pass

    @abstractmethod
    def movimentar_pecas_do_tabuleiro(self):
        pass

    @abstractmethod
    def sincronizar_pecas_do_tabuleiro(self):
        pass

    @abstractmethod
    def mostrar_tela_do_jogador(self):
        pass

    @abstractmethod
    def enviar_mensagem_de_chat(self, mensagem: str):
        pass

    @abstractmethod
    def receber_mensagem_de_chat(self, mensagem: str):
        pass
