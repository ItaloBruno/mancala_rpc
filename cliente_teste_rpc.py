import Pyro4
import sys

sys.excepthook = Pyro4.util.excepthook

nome = input("Qual seu nome?\n").strip()

servidor = Pyro4.Proxy("PYRONAME:mancala.servidor")

print(servidor.conectar_novo_cliente(nome + "1"))
print(servidor.conectar_novo_cliente(nome + "2"))

# print(servidor.teste(nome + "1"))
