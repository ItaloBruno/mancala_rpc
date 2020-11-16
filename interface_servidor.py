from abc import ABC, abstractmethod


class InterfaceServidor(ABC):
    @abstractmethod
    def conectar_novo_cliente(self, nome: str) -> str:
        pass

    @abstractmethod
    def desconectar_cliente(self, nome: str) -> str:
        pass
