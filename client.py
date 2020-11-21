import sys
import threading
import Pyro4
import os
from mensagem import Mensagem, TipoPermitidosDeMensagem
from tabuleiro import TelaDoJogo


class Jogador(object):
    def __init__(self):
        self.servidor = Pyro4.core.Proxy("PYRONAME:example.chatbox.server")
        self.conexao_encerrada = 0
        self.historico_de_mensagens = ""
        self.canal_de_comunicacao = ""
        self.nome_jogador = ""
        self.sou_primeiro_jogador = False
        self.tela_do_jogador = None

    @Pyro4.expose
    @Pyro4.oneway
    def message(self, nome_jogador, mensagem: dict):
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
        nicks = self.servidor.getNicks()
        if nicks:
            print("The following people are on the server: %s" % (", ".join(nicks)))
        channels = sorted(self.servidor.getChannels())
        if channels:
            print("The following channels already exist: %s" % (", ".join(channels)))
            self.canal_de_comunicacao = input(
                "Choose a channel or create a new one: "
            ).strip()
        else:
            print("The server has no active channels.")
            self.canal_de_comunicacao = input("Name for new channel: ").strip()

        self.nome_jogador = input("Choose a nickname: ").strip()
        people = self.servidor.join(self.canal_de_comunicacao, self.nome_jogador, self)
        print(
            "Joined channel %s as %s" % (self.canal_de_comunicacao, self.nome_jogador)
        )
        print("People on this channel: %s" % (", ".join(people)))
        print("INFO: Para desistir da partida, digite /sair")

        tela_do_jogador = TelaDoJogo(self.nome_jogador, self.sou_primeiro_jogador)
        tela_do_jogador.iniciar_tela_do_jogador()
        tela_do_jogador.desenhar_tabuleiro()
        tela_do_jogador.mostrar_tela_do_jogador()

        # TODO: Implementar a parte do chat assíncrono (não bloqueante)
        # TODO: Pegar os eventos do mouse e fazer a atualização das telas
        try:
            try:
                while not self.conexao_encerrada:
                    line = input(f"{self.nome_jogador}> ").strip()
                    if line == "/quit":
                        break
                    if line:
                        self.historico_de_mensagens += f"\n{self.nome_jogador} > {line}"
                        mensagem: Mensagem = Mensagem(
                            tipo="chat",
                            conteudo=self.historico_de_mensagens,
                            remetente=self.nome_jogador,
                        )
                        self.servidor.publish(
                            self.canal_de_comunicacao,
                            self.nome_jogador,
                            mensagem.converter_msg_em_dict_para_enviar(),
                        )
            except EOFError:
                pass
        finally:
            mensagem: Mensagem = Mensagem(
                tipo="desistencia",
                conteudo="Você ganhou a partida",
                remetente=self.nome_jogador,
            )
            self.servidor.publish(
                self.canal_de_comunicacao,
                self.nome_jogador,
                mensagem.converter_msg_em_dict_para_enviar(),
            )
            self.servidor.leave(self.canal_de_comunicacao, self.nome_jogador)
            self.conexao_encerrada = 1
            self._pyroDaemon.shutdown()


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
print("Saída executada com sucesso.")
