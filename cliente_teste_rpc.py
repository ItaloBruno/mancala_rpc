import Pyro4
from time import sleep

nome = input("Qual seu nome?\n").strip()

servidor = Pyro4.Proxy("PYRONAME:mancala.servidor")

print(servidor.conectar_novo_cliente(nome + " 1"))
print(servidor.conectar_novo_cliente(nome + " 2"))
print(servidor.conectar_novo_cliente(nome + " 3"))
print(servidor.conectar_novo_cliente(nome + " 4"))

print(servidor.enviar_mensagem_de_chat(nome + " 1"))
print(servidor.desconectar_cliente(nome=nome + " 1"))
