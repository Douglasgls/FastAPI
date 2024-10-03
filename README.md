# 🎯 Projeto FastAPI - A Jornada da TODO List!

Bem-vindo(a) à minha aventura, onde criei um sistema de TODO list usando o poderoso FastAPI. Mas não é qualquer lista de tarefas! Essa API tem uma missão importante: proteger suas tarefas do acesso de curiosos com um sistema de login que usa tokens gerados por uma pitada de magia criptográfica fornecida pela lib **argon2**.


## O Que Eu Aprendi Nessa Jornada? 🛤️
Ah, muita coisa! Ao longo desse projeto, mergulhei fundo no mar do back-end e pesquei novos conhecimentos, como:

- A importância da segurança na construção de APIs 🛡️.
- Como criar e executar containers Docker
- Conectar minha aplicação a um banco de dados usando o SQLAlchemy – a verdadeira âncora que sustenta nossa aplicação!


## Implementação do CRUD 🛠️
Como toda boa aplicação TODO list, temos um clássico CRUD (Create, Read, Update, Delete) para dois protagonistas:

- Usuários: Cada um com sua própria área de tarefas!
- Tarefas: Ninguém mexe nas suas! Só o dono pode visualizar e manipular essas informações.


# Conhecendo o FastAPI 🚀
O FastAPI é como aquele amigo que resolve seus problemas rápido, de forma simples, mas com uma robustez impressionante. Ele me ajudou a aprender conceitos essenciais como verbos HTTP, queries, e modelos de uma forma que foi quase mágica. Se você ficou curioso para saber mais sobre essa maravilha, link para a documentação. [Leia mais sobre aqui](https://fastapi.tiangolo.com/)  



# 🧪 Testes: A Ciência Por Trás da Magia
Aqui utilizei o pytest para garantir que tudo está funcionando como deveria. Usei ferramentas incríveis como:

- **FactoryBoy**: Criei usuários como se estivesse fabricando bonequinhos personalizados para os testes!

- **Freezegun**: Manipulei o tempo para garantir que os tokens expiram como esperado no mundo real (quem nunca quis controlar o tempo, né?).

- **TestContainers**: Esse foi um verdadeiro game-changer! Com ele, consegui criar e destruir ambientes de teste com containers reais, como o PostgreSQL. Dessa forma, os testes simularam o comportamento exato do ambiente de produção. Meu código utilizava o PostgresContainer para iniciar uma instância temporária do banco durante os testes. Com uma integração assim, nada escapou!

    ```python
    @pytest.fixture(scope='session')
    def engine():
        with PostgresContainer('postgres:16', driver='psycopg') as postgres:
            _engine = create_engine(postgres.get_connection_url())
            with _engine.begin():
                yield _engine

    @pytest.fixture
    def session(engine):
        table_registry.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
            session.rollback()
        table_registry.metadata.drop_all(engine)
    ```


# 🛠️ Gerenciamento de Tarefas com Taskipy
Quem gosta de digitar comandos gigantes toda hora? Eu não! Por isso, o taskipy é meu salvador. Agora, rodar os testes é tão simples quanto um "task test". Formatar o código? Só rodar "task format" com o Ruff. E para colocar a aplicação no ar? "Task run"!


# 🐳 Docker: A Aventura de Containerizar Tudo!
Para levar esse projeto a um nível mais profissional, dockerizei tanto a aplicação quanto o banco de dados. Usei um Dockerfile para criar a imagem da API e um arquivo Docker Compose para orquestrar tudo. Ah, não pense que foi fácil! Configurar o banco no Docker foi como montar um quebra-cabeça 3D – difícil, mas extremamente gratificante quando tudo funcionou.


# ⏳ Migrations: A Linha do Tempo do Banco de Dados
Com o Alembic e o SQLAlchemy, aprendi a fazer migrações no banco de dados, o que é como uma máquina do tempo para o nosso esquema de tabelas. Um simples "`alembic upgrade head`", e pronto: o banco evolui conforme as necessidades da aplicação.


# 🎩 Poetry: O Gerenciador de Dependências
Uma parte essencial do projeto foi organizar as dependências de forma limpa e eficiente, e para isso, o Poetry foi meu fiel escudeiro. Ele cuida de tudo, desde a instalação de pacotes até a definição de versões, garantindo que meu ambiente de desenvolvimento esteja sempre em harmonia.
