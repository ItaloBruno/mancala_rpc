from abc import ABC, abstractmethod
from tabuleiro import TelaDoJogo
from typing import Tuple


class InterfaceCliente(ABC):
    @abstractmethod
    def desistir_da_partida(self, nome_jogador: str):
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self, nome_jogador: str):
        pass

    @abstractmethod
    def criar_tela_do_jogador(self) -> TelaDoJogo:
        pass

    @abstractmethod
    def movimentar_pecas_do_tabuleiro(
        self, nome_jogador: str, coordenas_do_clique: Tuple[int]
    ):
        pass

    @abstractmethod
    def sincronizar_pecas_do_tabuleiro(self, nome_jogador: str):
        pass

    @abstractmethod
    def mostrar_tela_do_jogador(self, nome_jogador: str):
        pass

    @abstractmethod
    def enviar_mensagem_de_chat(self, remetente: str, mensagem: str):
        pass

    @abstractmethod
    def receber_mensagem_de_chat(self, destinatario: str, mensagem: str):
        pass
