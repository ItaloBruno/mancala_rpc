from mensagem import Mensagem, TipoPermitidosDeMensagem
from interface_cliente import InterfaceCliente
from tabuleiro import TelaDoJogo
from typing import Tuple
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Cliente(object):
    def __init__(self, nome: str, sou_primeiro_jogador: bool):
        self.nome: str = nome
        self.sou_primeiro_jogador: bool = sou_primeiro_jogador
        self.tabuleiro: TelaDoJogo = self.criar_tela_do_jogador()
        self.servidor = Pyro4.core.Proxy("PYRONAME:mancala.servidor")

    def desistir_da_partida(self, nome_jogador: str):
        pass

    def verificar_fim_de_jogo(self, nome_jogador: str):
        self.tabuleiro.verficar_se_alguem_ganhou()

    def iniciar_tela_do_jogador(self):
        self.tabuleiro.iniciar_tela_do_jogador()

    def desenhar_tabuleiro(self):
        self.tabuleiro.desenhar_tabuleiro()

    def criar_tela_do_jogador(self) -> TelaDoJogo:
        tabuleiro = TelaDoJogo(
            nome_jogador=self.nome,
            cliente_eh_primeiro_jogador=self.sou_primeiro_jogador,
        )
        return tabuleiro

    def movimentar_pecas_do_tabuleiro(
        self, nome_jogador: str, coordenas_do_clique: Tuple[int]
    ):
        resultado = self.tabuleiro.clicou_em_alguma_das_minhas_casa(coordenas_do_clique)
        if resultado:
            self.sincronizar_pecas_do_tabuleiro(nome_jogador)

    def sincronizar_pecas_do_tabuleiro(self, nome_jogador: str):
        novos_valores_pecas_tabuleiro = (
            self.tabuleiro.pegar_os_valores_das_casas_e_kallah()
        )
        return novos_valores_pecas_tabuleiro

    def mostrar_tela_do_jogador(self, nome_jogador: str):
        self.tabuleiro.mostrar_tela_do_jogador()

    def enviar_mensagem_de_chat(self, remetente: str, mensagem: str):
        mensagem = Mensagem(tipo="chat", conteudo=mensagem, remetente=self.nome)
        return mensagem

    def receber_mensagem_de_chat(self, destinatario: str, mensagem: str):
        # if mensagem.tipo == TipoPermitidosDeMensagem.desistencia.value:
        #     print("Eu venci a partida, ieeeeeeei")
        #     self.desistir_da_partida(self.nome)
        #
        # print(mensagem.conteudo)
        print(mensagem)

    @Pyro4.expose
    @Pyro4.oneway
    def message(self, nick, msg):
        # if nick != self.nick and nick != "Servidor":
        #     self.chat_history += '<font  color=#FF0000>' + nick + ":" + " " + msg + '<br>' + '</font>'
        #     # print(self.chat_history)
        #     # print(self.chat_history)
        # elif nick == "Servidor":
        #     self.chat_history += '<font  color=#437C17>' + '<b>' + nick + ":" + " " + msg + '</b>' + '<br>' + '<br>' + '</font>'
        print(msg)
