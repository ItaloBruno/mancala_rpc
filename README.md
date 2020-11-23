# Mancala utilizando RMI

Implentação do jogo [mancala](https://www.youtube.com/watch?v=Sog-iKBh6vs) e de um chat para a 
interação entre os jogadores utlizando a tecnologia Pyro4.

## Autor

Italo Bruno Cunha da Silva

## Tecnologias utilizadas

- [Python 3.7.7](https://www.python.org/)
- [Pyro4](https://github.com/irmen/Pyro4)
- [Pygame](https://www.pygame.org/news)


## Executando o projeto 

Antes de tudo, instale as dependências do projeto com o comando abaixo:

`pip install -r requirement.txt`

Pronto, agora vamos lá rodar o jogo e se divertir xD

1.  Você deve subir o servidor de nomes, para que possamos 
    registrar o servidor do jogo e possibilitar o ser acesso remoto. 
    Para isso, abra um terminal e execute o comando abaixo:

    `pyro4-ns`

2.  Agora finalmente podemos executar o servidor do jogo (uhuuuuu \o/). 
    Para isso, crie mais um terminal e execute o camando abaixo:
   
    `python servidor.py`

    Caso você queira ver se o cadastro da instância do servidor foi feita com sucesso, 
    use o comando abaixo para listar todos os objetos registrados no servidor de nomes:

    `pyro4-nsc list`
    
3.  Depois de subir o servidor, agora podemos criar os jogadores que irão participar da partida.
    Como de costume, abra um novo terminal e execute o comando abaixo para cada um dos jogadores:
   
    `python jogador.py`
    
    Quando o código do cliente é executado, será perguntado se você deseja criar um novo canal de comunicação 
    ou utilizar um já existente. Após isso, digite um apelido para o seu jogador e a tela do jogo será iniciada.
    Execute esse comando para cada um dos dois jogadores e se divirta :wink:
    
## Dificuldades encontradas

-   Tive uma certa dificuldade para fazer a comunicação entre o servidor e os clientes conectados nele. 
    Após ver o [exemplo da própria documentação do Pyro4](https://github.com/irmen/Pyro4/tree/master/examples/chatbox), 
    consegui adaptar para que o jogo funcionasse de forma correta.
-   Rodar a controladora do jogo (responsável por capturar os cliques do mouse) e o chat de forma assíncrona.

## Possíveis melhorias

- Controle de turno :x:	
- Reiniciar partida :x:	
- Desconectar os jogadores do servidor de forma correta (quando for solicitado através do chat) :x:	
- Criar um botão na tela do jogador para que eu possa realizar a desistência da partida, 
  colocando uma outra alternativa além do chat :x:	
- Melhorar mensagens mostradas para os jogadores, como: 
    - se sou o primeiro jogador ou não :heavy_check_mark:
    - se tenho direito a +1 jogada :x:
- Criar uma interface gráfica para o chat entre os jogadores :x:	
- Modificar o nome de classes e variáveis para uma melhor compreensão do código :heavy_check_mark:
