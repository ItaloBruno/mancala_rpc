from mensagem import Mensagem
import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(object):
    def __init__(self):
        self.canais_de_comunicacao = (
            {}
        )  # registered channels { channel --> (nick, client callback) list }
        self.nomes_jogadores_conectados = []  # all registered nicks on this server

    def pegar_canais_de_comunicacao(self):
        return list(self.canais_de_comunicacao.keys())

    def pegar_nomes_dos_jogadores(self):
        return self.nomes_jogadores_conectados

    def registrar(self, nome_canal, nome_jogador, objeto_jogador):
        if not nome_canal or not nome_jogador:
            raise ValueError("Nome de canal/jogador inválido!!!")

        if nome_jogador in self.nomes_jogadores_conectados:
            raise ValueError("Esse nome de jogador já está sendo usado!!!")

        if nome_canal not in self.canais_de_comunicacao:
            print(f"Criando novo canal {nome_canal}")
            self.canais_de_comunicacao[nome_canal] = []

        sou_o_primeiro_jogador = False
        if not self.nomes_jogadores_conectados:
            sou_o_primeiro_jogador = True

        self.canais_de_comunicacao[nome_canal].append((nome_jogador, objeto_jogador))
        self.nomes_jogadores_conectados.append(nome_jogador)
        print(f"Jogador {nome_jogador} se conectou no canal {nome_canal}")

        mensagem_de_conexao = Mensagem(
            tipo="conexao_estabelecida",
            conteudo=sou_o_primeiro_jogador,
            remetente="servidor",
        )
        self.publicar(
            nome_canal,
            "SERVER",
            mensagem_de_conexao.converter_msg_em_dict_para_enviar(),
        )

        return [
            nome_jogador for (nome_jogador, c) in self.canais_de_comunicacao[nome_canal]
        ]

    def publicar(self, nome_canal, nome_jogador, mensagem):
        if nome_canal not in self.canais_de_comunicacao:
            print(f"CANAL DESCONHECIDO IGNORADO {nome_canal}")
            return
        for (n, c) in self.canais_de_comunicacao[nome_canal][:]:
            try:
                c.receber_mensagem(nome_jogador, mensagem)
            except Pyro4.errors.ConnectionClosedError:
                if (n, c) in self.canais_de_comunicacao[nome_canal]:
                    self.canais_de_comunicacao[nome_canal].remove((n, c))
                    print(f"Ouvinte morto removido {n} - {c} ")

    def desconectar_jogador(self, nome_canal, nome_jogador):
        if nome_canal not in self.canais_de_comunicacao:
            print(f"CANAL DESCONHECIDO IGNORADO {nome_canal}")
            return

        for (n, c) in self.canais_de_comunicacao[nome_canal]:
            if n == nome_jogador:
                self.canais_de_comunicacao[nome_canal].remove((n, c))
                break

        mensagem_de_conexao = Mensagem(
            tipo="desistencia",
            conteudo=f"\n** {nome_jogador} saiu do jogo **",
            remetente=nome_jogador,
        )
        self.publicar(
            nome_canal,
            "SERVER",
            mensagem_de_conexao.converter_msg_em_dict_para_enviar(),
        )

        if len(self.canais_de_comunicacao[nome_canal]) < 1:
            del self.canais_de_comunicacao[nome_canal]
            print(f"Canal {nome_canal} removido")

        self.nomes_jogadores_conectados.remove(nome_jogador)
        print(f"O jogador {nome_jogador} deixou o canal {nome_canal}")


Pyro4.Daemon.serveSimple({Servidor: "mancala.servidor"})
