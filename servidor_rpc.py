from interface_cliente import InterfaceCliente
from interface_servidor import InterfaceServidor
from typing import Optional, List, Tuple
from cliente_rpc import Cliente
import Pyro4
import sys

if len(sys.argv) != 2:
    print("uso correto: python servidor_rpc.py <endereço ip>")
    exit()

ENDERECO_IP: str = sys.argv[1]


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(InterfaceCliente, InterfaceServidor):
    def __init__(self):
        self.primeiro_jogador_conectado: bool = False
        self.jogadores: List[Cliente] = []

    def desistir_da_partida(self, nome_jogador: str):
        pass

    def verificar_fim_de_jogo(self, nome_jogador: str):
        pass

    def definir_ganhador(self):
        pass

    def criar_tela_do_jogador(self):
        pass

    def movimentar_pecas_do_tabuleiro(
        self, nome_jogador: str, coordenas_do_clique: Tuple[int]
    ):
        pass

    def sincronizar_pecas_do_tabuleiro(self, nome_jogador: str):
        pass

    def mostrar_tela_do_jogador(self, nome_jogador: str):
        jogador = self.selecionar_jogador(nome=nome_jogador)
        if jogador:
            print("cheguei aqui")
            jogador.mostrar_tela_do_jogador(nome_jogador)

    def enviar_mensagem_de_chat(self, remetente: str, mensagem: str):
        pass

    def receber_mensagem_de_chat(self, destinatario: str, mensagem: str):
        pass

    ########################################################
    # Funções exclusivas do servidor, para gerir os clientes
    ########################################################

    def selecionar_jogador(self, nome) -> Optional[Cliente]:
        jogador: Optional[Cliente] = next(
            (i for i in self.jogadores if i.nome == nome),
            None,
        )
        return jogador
        pass

    def criar_novo_cliente(self, nome: str, primeiro_jogador: bool) -> Cliente:
        return Cliente(nome=nome, sou_primeiro_jogador=primeiro_jogador)

    def definir_se_eh_o_primeiro_jogador(self, nome_jogador: str) -> str:
        jogador = self.selecionar_jogador(nome=nome_jogador)
        mensagem = ""
        if jogador is None and len(self.jogadores) < 2:
            if not self.primeiro_jogador_conectado:
                novo_jogador = self.criar_novo_cliente(
                    nome=nome_jogador, primeiro_jogador=True
                )
                self.jogadores.append(novo_jogador)
                print(self.jogadores)
                novo_jogador.message("servidor", "vai vai vai")
                self.primeiro_jogador_conectado = True
                mensagem = "Sou o primeiro jogador"
            else:
                novo_jogador = self.criar_novo_cliente(
                    nome=nome_jogador, primeiro_jogador=False
                )
                self.jogadores.append(novo_jogador)
                mensagem = "Sou o segundo jogador"

        return mensagem
        pass

    def conectar_novo_cliente(self, nome_jogador: str, cliente) -> str:
        print(cliente)
        mensagem = self.definir_se_eh_o_primeiro_jogador(nome_jogador)

        if not mensagem:
            return "O número máximo de jogadores na partida já foi alcançado"

        self.jogadores[0].message("vai", "mandar msng")
        return f"{mensagem}. Cliente {nome_jogador} criado e conectado no servidor de nomes"

    def desconectar_cliente(self, nome: str) -> str:
        # jogador = self.selecionar_jogador(nome)
        #
        # if jogador:
        #     self.jogadores.remove(jogador)
        #     return f"Cliente {nome} desconectado"
        # else:
        #     return f"Cliente {nome} não encontrado"
        pass

    def teste(self, nome_jogador: str):
        # jogador = self.selecionar_jogador(nome_jogador)
        # indice = self.jogadores.index(jogador)
        # ou = 0
        # if not indice:
        #     ou = 1
        #
        # outro_jogador = self.jogadores[ou]
        jogador_1 = self.jogadores[0]
        jogador_1.message("vai", "vai jogador 1")
        jogador_2 = self.jogadores[1]
        jogador_2.message("vai", "vai jogador 1")
        #
        # jogador.receber_mensagem_de_chat(nome_jogador, "deu cerrto a conexao")
        # outro_jogador.receber_mensagem_de_chat("", "deu cerrto a conexao")


import threading


class DaemonThread(threading.Thread):
    def __init__(self, chat):
        threading.Thread.__init__(self)
        self.chatter = chat
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.chatter)
            daemon.requestLoop()


def registrar_no_servidor_de_nomes(instancia_para_registrar, nome, endereco_ip):
    """
    Registrando a classe/objeto no servidor de nomes, para que eu possa acessá-lo de formata remota.
    """
    print("criando")
    vai = DaemonThread(instancia_para_registrar)
    vai.start()

    # Pyro4.Daemon.serveSimple(
    #     {instancia_para_registrar: f"mancala.{nome}"}, ns=True, host=endereco_ip
    # )
    print("fooooooi")
    # tem que ter uma instânci do servidor no cliente


if __name__ == "__main__":
    Pyro4.Daemon.serveSimple({Servidor: f"mancala.servidor"}, ns=True, host=ENDERECO_IP)


# # Registrando minha classe Servidor no servidor de nomes
# daemon = Pyro4.Daemon()
# servidor_de_nomes = Pyro4.locateNS()
# uri = daemon.register(Servidor)
# servidor_de_nomes.register("mancala.servidor", uri)
#
# print("pronto, servidor registrado no servidor de nomes")
# daemon.requestLoop()
