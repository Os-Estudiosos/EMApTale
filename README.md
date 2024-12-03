# Linguagens de Programação - Trabalho A2 - Jogo Pygame

Esse trabalho tem como objetivo criar um jogo utilizando python, mais especificamente a biblioteca de jogos pygame, com o foco principal de colocar em prática os conhecimentos de Programação Orientada a Objetos ensinados pelo professor Rafael de Pinho André.
A ideia principal do jogo se passa na faculdade(especificamente no andar do curso), onde o jogador está com notas muito baixas, e, para recuperá-las, deve ganhar de cada professor batalhando com cada um deles. A mecânica do jogo é baseada no jogo Undertale.

## Clonando o repositório

Vá até o local desejado e execute o comando no terminal do git bash:

```
$ git clone https://github.com/jaopredo/EMApTale.git
```

## Instalação do Projeto

Execute o comando para realizar o download das bibliotecas utilizadas no projeto (recomendamos, antes de instalar o projeto, criar um VIRTUAL ENVIROMENT para melhor organização):

`$ pip install -r ./requirements.txt`

## Como jogar

Para jogar, após dar o git clone e baixar as bibliotecas necessárias no requirements, basta rodar o arquivo **main.py** que localiza-se no fim dos arquivos:

```
$ python main.py
```

## Sobre o jogo:

Nesse jogo, você é um estudante do 2° período de Ciência de Dados e IA da Fundação Getúlio Vargas, e está de recuperação em todas as matérias do período. Por isso, vai lutar contra cada professor, na sala de cada um deles, com o objetivo de vencer a batalha e, com isso, passar de semestre.
O mapa é baseado na vida real, por isso se passa no 5° andar do prédio da faculdade, onde os professores se localizam. Existem várias interações em todo o mapa, que remetem a vida cotidiana do estudante, desde o chão do mapa até os objetos e os coletáveis em todo o mapa que remetem a vivência frequente dos alunos.
Além disso, cada batalha é única e característica, com cada ataque sendo diretamente relacionado a alguma característica do professor ou da matéria dada.

Colocar vídeo/foto

## Estrutura das Pastas

```
|- /classes
    |- battle
        |- menus
            |- hud
    |- bosses
        |- attacks
    |- effects
    |- map
    |- polygon
    |- sprites
    |- text
|- /config
|- /constants
|- /fonts
|- /infos
|- /screens
    |- cutscene
    |- menu
    |- subscreen
|- /sounds
|- /sprites
    |- bosses
    |- cutscene
    |- effects
    |- hud
        |- combat
        |- dialogue
    |- items
    |- npc
    |- player
        |-hearts
    |- tiles
|- /tests
|- /tileset
|- /utils

```

- **Classes:** CCC
  - **battle:** CCC
    - **menus:** CCC
      - **hud:** CCC
  - **bosses:** CCC
    - **attacks:** CCC
  - **effects:** CCC
  - **map:** CCC
  - **polygon:** CCC
  - **sprites:** CCC
  - **text:** CCC
- **Config:** Nessa pasta estão os gerenciadores de combate, de eventos, de texto, de salvamento de progresso, de som e de cutscenes, além de definir o nome do jogo, o caminho base e a quantos frames por segundo o jogo deveria rodar.
- **Constants:** Nesta pasta estão armazenados constantes relacionadas aos turnos dos chefes e do personagem, auxiliando na ordenação de cada turno.
- **Fonts:** Aqui estão as fontes de texto utilizadas nas caixas de diálogo (interações no mapa, durante as batalhas, menu inicial, inventário, menu de pausa, entre outros) presentes no jogo.
- **Infos:** Nesta pasta estão os arquivos .json utilizados para armazenar as informações dos chefes, dos coletáveis e do jogador.
- **Screen:** Pasta com as configurações do game (Além de módulos relacionados a save, mexer nas configurações do jogo, etc.)
  - **cutscene:** CCC
  - **menu:** CCC
  - **subscreen:** CCC
- **Sounds:** Aqui estão todos os sons (trilha sonora e efeitos sonoros) utilizados no projeto.
- **Sprites:** Nesta pasta estão os sprites utilizados nos chefes, nas cutscenes, nos efeitos e na inteface gráfica da batalha. Além disso, há também os sprites do personagem e do mapa
  - **bosses:** imagens pixelada e em preto e branco dos bosses
  - **cutscene:** imagens utilizadas na cutscene do início do jogo
  - **effects:** todo tipo de efeito usado na nas lutas
  - **hud:** imagens básicas do hud de batalha/coisas relacionadas a interação do mapa
    - **combat:** imagens da parte de combate, como os botões de agir, lutar, etc.
    - **dialogue:** imagens de caixa de diálogo usadas tanto na luta como em interações no mapa
  - **items:** pasta com os itens coletáveis do mapa
  - **npc:** imagem de um possível npc do mapa
  - **player:** imagens usadas para desenhar o player no mapa
    - **hearts:** imagens dos corações das batalhas
  - **tiles:** imagens utilizadas no começo do desenvolvimento do jogo
- **Tests:** Aqui estão os testes unitários das funções mais gerais utilizadas, de classes referentes aos ataques dos chefes, classes do inventário e sobre a movimentação do personagem.
- **Tileset:** Aqui estão os sprites de tudo que é usado para criar o mapa, além do arquivo do mapa (.tmx) que é usado para que o pygame leia e entenda a organização dos tiles, colisões, interações, etc.
- **Utils:** Na pasta utils estão algumas funções reutilizáveis em certas partes do código.
- **Report:** Pasta que armazena o relatório do código.

## Relatório

Para melhor entendimento do projeto e andamento do mesmo, foi feito também um relatório de todo o projeto, que está localizado na pasta _Report_ nos arquivos do código.

As **referências** utilizadas(como sprites e aúdios utilizados na criação dos jogos serão devidamente creditados nas referências do relatório).
