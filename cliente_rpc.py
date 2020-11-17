from mensagem import Mensagem, TipoPermitidosDeMensagem
from interface_cliente import InterfaceCliente
from tabuleiro import TelaDoJogo
from typing import Tuple
import pygame
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Cliente(InterfaceCliente):
    def __init__(self, nome: str, sou_primeiro_jogador: bool):
        self.nome: str = nome
        self.sou_primeiro_jogador: bool = sou_primeiro_jogador
        self.tabuleiro: TelaDoJogo = self.criar_tela_do_jogador()

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

    def receber_mensagem_de_chat(self, destinatario: str, mensagem: Mensagem):
        if mensagem.tipo == TipoPermitidosDeMensagem.desistencia.value:
            print("Eu venci a partida, ieeeeeeei")
            self.desistir_da_partida(self.nome)

        print(mensagem.conteudo)


if __name__ == "__main__":
    meu_nome_usuario = input("Digite seu nome de usuário: ")

    print("INFO: Para desistir da partida, digite 'sair do jogo' ou 'desconectar'")
    servidor = Pyro4.Proxy("PYRONAME:mancala.servidor")
    resposta = servidor.conectar_novo_cliente(meu_nome_usuario)
    mostrar_tela_jogo = True

    while mostrar_tela_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrar_tela_jogo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                # resultado = tela_do_jogador.clicou_em_alguma_das_minhas_casa(
                #     pygame.mouse.get_pos()
                # )
                # time.sleep(0.5)
                # if resultado:
                #     novos_valores_pecas_tabuleiro = (
                #         tela_do_jogador.pegar_os_valores_das_casas_e_kallah()
                #     )
                #
                #     mensagem_movimentacao = Mensagem(
                #         tipo=TipoPermitidosDeMensagem.movimentacao.value,
                #         conteudo=novos_valores_pecas_tabuleiro,
                #         remetente=meu_nome_usuario,
                #     )
                #
                #     cliente.enviar_movimentacao_ao_servidor(mensagem_movimentacao)
                #     resultado = False
                #     continue
                pass
        try:
            # terminou = tela_do_jogador.verficar_se_alguem_ganhou()
            # if terminou:
            #     mostrar_tela_jogo = False
            # tela_do_jogador.desenhar_elementos_na_tela()
            # tela_do_jogador.mostrar_tela_do_jogador()
            pass
        except KeyboardInterrupt:
            # cliente.encerrar_conexao_servidor()
            break
