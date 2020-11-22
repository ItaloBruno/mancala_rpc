from mensagem import Mensagem, TipoPermitidosDeMensagem
from tabuleiro import TelaDoJogo

import threading
import Pyro4
import pygame
import time
import os


class Jogador(object):
    def __init__(self):
        self.servidor = Pyro4.core.Proxy("PYRONAME:mancala.servidor")
        self.conexao_encerrada = False
        self.historico_de_mensagens = ""
        self.canal_de_comunicacao = ""
        self.nome_jogador = ""
        self.sou_primeiro_jogador = False
        self.tela_do_jogador = None

    @Pyro4.expose
    @Pyro4.oneway
    def receber_mensagem(self, nome_jogador: str, mensagem: dict):
        if nome_jogador != self.nome_jogador:
            mensagem_recebida_do_servidor = Mensagem(
                tipo="chat", conteudo="", remetente=self.nome_jogador
            )
            mensagem_recebida_do_servidor.setar_valores_da_classe(
                json_da_mensagem=mensagem
            )

            if (
                mensagem_recebida_do_servidor.tipo
                == TipoPermitidosDeMensagem.desistencia.value
            ):
                self.historico_de_mensagens += "\nEu venci a partida, ieeeeeeei.\nVocê já pode encerrar a sua partida :D"
            elif (
                mensagem_recebida_do_servidor.tipo
                == TipoPermitidosDeMensagem.conexao_estabelecida.value
            ):
                if mensagem_recebida_do_servidor.conteudo:
                    self.historico_de_mensagens += f"\nsou o primeiro jogador\n** jogador {nome_jogador} conectado **"
                    self.sou_primeiro_jogador = True
                else:
                    self.historico_de_mensagens += f"\nsou o segundo jogador\n** jogador {nome_jogador} conectado **"

            elif (
                mensagem_recebida_do_servidor.tipo
                == TipoPermitidosDeMensagem.movimentacao.value
            ):
                self.tela_do_jogador.sincronizacao_de_valor_de_pecas_do_meu_tabuleiro_com_o_outro_jogador(
                    mensagem_recebida_do_servidor.conteudo
                )

            else:
                self.historico_de_mensagens += mensagem_recebida_do_servidor.conteudo

            os.system("clear")
            print(self.historico_de_mensagens)

    def iniciar_partida(self):
        nomes_jogadores = self.servidor.pegar_nomes_dos_jogadores()
        if nomes_jogadores:
            print(
                "Os seguintes jogadores estão conectados no servidor: {}".format(
                    (", ".join(nomes_jogadores))
                )
            )

        canais = sorted(self.servidor.pegar_canais_de_comunicacao())
        if canais:
            print("Os seguintes canais já existem: {}".format((", ".join(canais))))
            self.canal_de_comunicacao = input(
                "Escolha um dos canais para se conectar ou crie um novo: "
            ).strip()
        else:
            print("O servidor não tem canais ativos")
            self.canal_de_comunicacao = input(
                "Digite um nome para o novo canal: "
            ).strip()

        self.nome_jogador = input("Escolha seu nome: ").strip()
        jogadores_registrados = self.servidor.registrar(
            self.canal_de_comunicacao, self.nome_jogador, self
        )
        self.historico_de_mensagens += f"\nConectado ao canal {self.canal_de_comunicacao} como {self.nome_jogador}"

        self.historico_de_mensagens += "\nPessoas conectadas nesse canal: {}".format(
                (", ".join(jogadores_registrados))
        )

        self.historico_de_mensagens += "\nINFO: Para desistir da partida, digite /sair"

        self.tela_do_jogador = TelaDoJogo(self.nome_jogador, self.sou_primeiro_jogador)
        self.tela_do_jogador.iniciar_tela_do_jogador()
        self.tela_do_jogador.desenhar_tabuleiro()
        self.tela_do_jogador.mostrar_tela_do_jogador()

        thread_controlador = threading.Thread(target=self.controlador_da_partida)
        thread_chat = threading.Thread(target=self.enviar_mensagem_de_chat)

        thread_controlador.start()
        thread_chat.start()

    def controlador_da_partida(self):
        mostrar_tela_jogo = True
        while mostrar_tela_jogo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mostrar_tela_jogo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    resultado = self.tela_do_jogador.clicou_em_alguma_das_minhas_casa(
                        pygame.mouse.get_pos()
                    )
                    time.sleep(0.5)
                    if resultado:
                        novos_valores_pecas_tabuleiro = (
                            self.tela_do_jogador.pegar_os_valores_das_casas_e_kallah()
                        )

                        mensagem_movimentacao = Mensagem(
                            tipo=TipoPermitidosDeMensagem.movimentacao.value,
                            conteudo=novos_valores_pecas_tabuleiro,
                            remetente=self.nome_jogador,
                        )

                        self.servidor.publicar(
                            self.canal_de_comunicacao,
                            self.nome_jogador,
                            mensagem_movimentacao.converter_msg_em_dict_para_enviar(),
                        )
                        resultado = False
                        continue

            terminou = self.tela_do_jogador.verficar_se_alguem_ganhou()
            if terminou:
                mostrar_tela_jogo = False

            self.tela_do_jogador.desenhar_elementos_na_tela()
            self.tela_do_jogador.mostrar_tela_do_jogador()

    def desconectar(self):
        mensagem: Mensagem = Mensagem(
            tipo="desistencia",
            conteudo="Você ganhou a partida",
            remetente=self.nome_jogador,
        )
        self.servidor.publicar(
            self.canal_de_comunicacao,
            self.nome_jogador,
            mensagem.converter_msg_em_dict_para_enviar(),
        )
        self.servidor.desconectar_jogador(self.canal_de_comunicacao, self.nome_jogador)
        self.conexao_encerrada = 1
        self._pyroDaemon.shutdown()

    def enviar_mensagem_de_chat(self):
        try:
            try:
                while not self.conexao_encerrada:
                    pass
                    msg = input(f"{self.nome_jogador}> ").strip()
                    if msg == "/sair":
                        break
                    if msg:
                        self.historico_de_mensagens += f"\n{self.nome_jogador} > {msg}"
                        mensagem: Mensagem = Mensagem(
                            tipo="chat",
                            conteudo=f"\n{self.nome_jogador} > {msg}",
                            remetente=self.nome_jogador,
                        )
                        self.servidor.publicar(
                            self.canal_de_comunicacao,
                            self.nome_jogador,
                            mensagem.converter_msg_em_dict_para_enviar(),
                        )
            except EOFError:
                pass
        finally:
            self.desconectar()


class DaemonThread(threading.Thread):
    def __init__(self, jogador):
        threading.Thread.__init__(self)
        self.jogador = jogador
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.jogador)
            daemon.requestLoop(lambda: not self.jogador.conexao_encerrada)


jogador = Jogador()
daemonthread = DaemonThread(jogador)
daemonthread.start()
jogador.iniciar_partida()
