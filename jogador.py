import Pyro4
import pygame
import sys
from cliente_rpc import Cliente
import threading

sys.excepthook = Pyro4.util.excepthook


class DaemonThread(threading.Thread):
    def __init__(self, chatter):
        threading.Thread.__init__(self)
        self.chatter = chatter
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.chatter)
            daemon.requestLoop(lambda: not self.chatter.conexao_encerrada)


if __name__ == "__main__":
    meu_nome_usuario = input("Digite seu nome de usuário: ")
    cliente_rpc = Cliente(nome=meu_nome_usuario, sou_primeiro_jogador=True)
    daemonThread = DaemonThread(cliente_rpc)
    daemonThread.start()

    print("INFO: Para desistir da partida, digite 'sair do jogo' ou 'desconectar'")
    servidor = Pyro4.Proxy("PYRONAME:mancala.servidor")
    resposta = servidor.conectar_novo_cliente(meu_nome_usuario, cliente_rpc)
    servidor.mostrar_tela_do_jogador(meu_nome_usuario)
    mostrar_tela_jogo = True

    while mostrar_tela_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrar_tela_jogo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                print("identifiquei o clique")
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
