import Pyro4
from mensagem import Mensagem


# Chat box administration server.
# Handles logins, logouts, channels and nicknames, and the chatting.
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ChatBox(object):
    def __init__(self):
        self.channels = (
            {}
        )  # registered channels { channel --> (nick, client callback) list }
        self.nicks = []  # all registered nicks on this server

    def getChannels(self):
        return list(self.channels.keys())

    def getNicks(self):
        return self.nicks

    def join(self, channel, nick, callback):
        if not channel or not nick:
            raise ValueError("invalid channel or nick name")
        if nick in self.nicks:
            raise ValueError("this nick is already in use")
        if channel not in self.channels:
            print("CREATING NEW CHANNEL %s" % channel)
            self.channels[channel] = []

        sou_o_primeiro_jogador = False
        if not self.nicks:
            sou_o_primeiro_jogador = True

        self.channels[channel].append((nick, callback))
        self.nicks.append(nick)
        print("%s JOINED %s" % (nick, channel))

        mensagem_de_conexao = Mensagem(
            tipo="conexao_estabelecida",
            conteudo=sou_o_primeiro_jogador,
            remetente="servidor",
        )
        self.publish(
            channel, "SERVER", mensagem_de_conexao.converter_msg_em_dict_para_enviar()
        )

        return [
            nick for (nick, c) in self.channels[channel]
        ]  # return all nicks in this channel

    def leave(self, channel, nick):
        if channel not in self.channels:
            print("IGNORED UNKNOWN CHANNEL %s" % channel)
            return
        for (n, c) in self.channels[channel]:
            if n == nick:
                self.channels[channel].remove((n, c))
                self.nicks.remove(nick)
                break

        mensagem_de_conexao = Mensagem(
            tipo="desistencia", conteudo=f"\n** {nick} saiu do jogo **", remetente=nick
        )
        self.publish(
            channel, "SERVER", mensagem_de_conexao.converter_msg_em_dict_para_enviar()
        )

        if len(self.channels[channel]) < 1:
            del self.channels[channel]
            print("REMOVED CHANNEL %s" % channel)
        self.nicks.remove(nick)
        print("%s LEFT %s" % (nick, channel))

    def publish(self, channel, nick, msg):
        if channel not in self.channels:
            print("IGNORED UNKNOWN CHANNEL %s" % channel)
            return
        for (n, c) in self.channels[channel][:]:  # use a copy of the list
            try:
                c.message(nick, msg)  # oneway call
                # c.receber(nick, msg)
            except Pyro4.errors.ConnectionClosedError:
                # connection dropped, remove the listener if it's still there
                # check for existence because other thread may have killed it already
                if (n, c) in self.channels[channel]:
                    self.channels[channel].remove((n, c))
                    print("Removed dead listener %s %s" % (n, c))


Pyro4.Daemon.serveSimple({ChatBox: "example.chatbox.server"})
