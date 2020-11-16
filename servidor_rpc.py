from interface_cliente import InterfaceCliente
from interface_servidor import InterfaceServidor
from typing import Optional, List
from cliente_rpc import Cliente
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(InterfaceCliente, InterfaceServidor):
    def __init__(self):
        self.primeiro_jogador_conectado: bool = False
        self.jogadores: List[Cliente] = []

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

    def mostrar_tela_do_jogador(self, nome: str):
        jogador = self.selecionar_jogador(nome=nome)
        if jogador:
            print("cheguei aqui")
            jogador.mostrar_tela_do_jogador(nome)

    def enviar_mensagem_de_chat(self, mensagem: str):
        pass

    def receber_mensagem_de_chat(self, mensagem: str):
        pass

    # Funções exclusivas do servidor, para gerir os clientes
    def selecionar_jogador(self, nome) -> Optional[Cliente]:
        jogador: Optional[Cliente] = next(
            (i for i in self.jogadores if i.nome == nome),
            None,
        )
        return jogador

    def criar_novo_cliente(self, nome: str, primeiro_jogador: bool) -> Cliente:
        return Cliente(nome=nome, sou_primeiro_jogador=primeiro_jogador)

    def definir_se_eh_o_primeiro_jogador(self, nome: str) -> str:
        jogador = self.selecionar_jogador(nome=nome)
        mensagem = ""
        if jogador is None and len(self.jogadores) < 2:
            if not self.primeiro_jogador_conectado:
                novo_jogador = self.criar_novo_cliente(nome=nome, primeiro_jogador=True)
                self.jogadores.append(novo_jogador)
                self.primeiro_jogador_conectado = True
                mensagem = "Sou o primeiro jogador"
            else:
                novo_jogador = self.criar_novo_cliente(
                    nome=nome, primeiro_jogador=False
                )
                self.jogadores.append(novo_jogador)
                mensagem = "Sou o segundo jogador"

        return mensagem

    def conectar_novo_cliente(self, nome: str) -> str:
        mensagem = self.definir_se_eh_o_primeiro_jogador(nome)

        if not mensagem:
            return "O número máximo de jogadores na partida já foi alcançado"

        return f"{mensagem}. Cliente {nome} criado e conectado no servidor de nomes"

    def desconectar_cliente(self, nome: str) -> str:
        jogador = self.selecionar_jogador(nome)

        if jogador:
            self.jogadores.remove(jogador)
            return f"Cliente {nome} desconectado"
        else:
            return f"Cliente {nome} não encontrado"


# Registrando minha classe Servidor no servidor de nomes
daemon = Pyro4.Daemon()
servidor_de_nomes = Pyro4.locateNS()
uri = daemon.register(Servidor)
servidor_de_nomes.register("mancala.servidor", uri)

print("pronto, servidor registrado no servidor de nomes")
daemon.requestLoop()
