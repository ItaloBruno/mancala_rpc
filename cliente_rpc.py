from mensagem import Mensagem, TipoPermitidosDeMensagem
from interface_cliente import InterfaceCliente
from tabuleiro import TelaDoJogo
from typing import Tuple

import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Cliente(InterfaceCliente):
    def __init__(self, nome: str, sou_primeiro_jogador: bool):
        self.nome: str = nome
        self.sou_primeiro_jogador: bool = sou_primeiro_jogador
        self.tabuleiro: TelaDoJogo = self.criar_tela_do_jogador()

    def desistir_da_partida(self):
        pass

    def verificar_fim_de_jogo(self):
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

    def movimentar_pecas_do_tabuleiro(self, coordenas_do_clique: Tuple[int]):
        resultado = self.tabuleiro.clicou_em_alguma_das_minhas_casa(coordenas_do_clique)
        if resultado:
            self.sincronizar_pecas_do_tabuleiro()

    def sincronizar_pecas_do_tabuleiro(self):
        novos_valores_pecas_tabuleiro = (
            self.tabuleiro.pegar_os_valores_das_casas_e_kallah()
        )
        return novos_valores_pecas_tabuleiro

    def mostrar_tela_do_jogador(self, nome: str):
        self.tabuleiro.mostrar_tela_do_jogador()

    def enviar_mensagem_de_chat(self, mensagem: str):
        mensagem = Mensagem(tipo="chat", conteudo=mensagem, remetente=self.nome)
        return mensagem

    def receber_mensagem_de_chat(self, mensagem: Mensagem):
        if mensagem.tipo == TipoPermitidosDeMensagem.desistencia.value:
            print("Eu venci a partida, ieeeeeeei")
            self.desistir_da_partida()

        print(mensagem.conteudo)
