import Pyro4


nome = input("Qual seu nome?\n").strip()

servidor = Pyro4.Proxy("PYRONAME:mancala.servidor")

print(servidor.conectar_novo_cliente(nome + " 1"))
print(servidor.conectar_novo_cliente(nome + " 2"))
print(servidor.conectar_novo_cliente(nome + " 3"))

servidor.mostrar_tela_do_jogador(nome + " 1")
print(servidor.desconectar_cliente(nome=nome + " 1"))
