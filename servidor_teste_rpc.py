from interface_servidor import InterfaceServidor
from interface_cliente import InterfaceCliente
import Pyro4
import sys


if len(sys.argv) != 2:
    print("python <endereço ip>")
    sys.exit()

endereco_ip = str(sys.argv[1])


# definindo classe que vou registrar no servidor de nomes
@Pyro4.expose
class Servidor(InterfaceCliente, InterfaceServidor):
    jogador_1 = None
    jogador_2 = None

    def teste(self) -> str:
        return "deu bom implementar a função do cliente ieeeeeei"

    def conectar_novo_cliente(self, nome: str) -> str:
        return f"Cliente {nome} conectado"

    def desconectar_cliente(self, nome: str) -> str:
        return f"Cliente {nome} desconectado"


# Registrando minha classe Servidor no servidor de nomes
daemon = Pyro4.Daemon()
servidor_de_nomes = Pyro4.locateNS()
uri = daemon.register(Servidor)
servidor_de_nomes.register("mancala.servidor", uri)

print("pronto, servidor registrado no servidor de nomes")
daemon.requestLoop()
