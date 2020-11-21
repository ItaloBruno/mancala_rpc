from abc import ABC, abstractmethod


class InterfaceServidor(ABC):
    @abstractmethod
    def conectar_novo_cliente(self, nome_jogador: str, cliente) -> str:
        pass

    @abstractmethod
    def desconectar_cliente(self, nome_jogador: str) -> str:
        pass
