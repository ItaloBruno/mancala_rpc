from interface_cliente import InterfaceCliente


class Cliente(InterfaceCliente):
    nome: str = ""

    def __init__(self, nome: str):
        self.nome: str = nome

    def desistir_da_partida(self):
        pass

    def verificar_fim_de_jogo(self):
        pass

    def definir_ganhador(self):
        pass

    def criar_tela_do_jogador(self):
        pass

    def movimentar_pecas_do_tabuleiro(self):
        pass

    def sincronizar_pecas_do_tabuleiro(self):
        pass

    def mostrar_tela_do_jogador(self):
        pass

    def enviar_mensagem_de_chat(self, mensagem: str):
        pass

    def receber_mensagem_de_chat(self, mensagem: str):
        pass

