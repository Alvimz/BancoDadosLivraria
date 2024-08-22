import os
import sqlite3


class Banco_de_dados:
    def __init__(self) -> None:
        self.conexao = sqlite3.connect("bdLivraria.db")
        self.cursor = None

    def BancoExiste(self):
        banco = not os.path.exists("bdLivraria.db")

        if banco:
            print("Banco criado com sucesso!")
        else:
            print("Banco acessado com sucesso!")
        return self.conexao

    def criarTabelas(self):
        self.cursor = self.conexao.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(150) NOT NULL UNIQUE,
                qnt INT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(255) NOT NULL,
                telefone INT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trans(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INT NOT NULL UNIQUE,
                id_livro INT UNIQUE,
                qnt_comprados int NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                FOREIGN KEY (id_livro) REFERENCES livros(id)
            );
        """)

        self.cursor.close()

    def InserirCliente(self):
        self.cursor = self.conexao.cursor()
        while True:
            nome = input("Insira o nome do cliente: ")
            if not nome:
                print("Obrigatório ter um nome!")
            else:
                break
        while True:
            telefone = int(input("Insira o telefone: "))
            if not telefone:
                print("Obrigatório um número de telefone!")
            else:
                self.cursor.execute(
                    """
                                    INSERT INTO clientes (nome,telefone) values
                                    (?,?);
                                    
                                    """,
                    (
                        nome,
                        telefone,
                    ),
                )
                self.conexao.commit()
                print("Cliente Cadastrado!")
                self.cursor.close()
                break

    def NovoLivro(self):
        self.cursor = self.conexao.cursor()
        while True:
            titulo = input("Insira o titulo: ")
            if not titulo:
                print("É necessário inserir um titulo!")
            else:
                break

        while True:
            qnt_estoq = int(input("Insira a qnt no estoque: "))
            if qnt_estoq <= 0:
                print("Insira um valor válido!")
            else:
                self.cursor.execute(
                    """
                                    INSERT INTO livros (titulo,qnt) values
                                    (?,?);""",
                    (titulo, qnt_estoq),
                )
                self.conexao.commit()
                print("Livro Cadastrado!")
                self.cursor.close()
                break

    def listar_livros(self):
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SELECT * FROM livros")
        livros = self.cursor.fetchall()
        for livro in livros:
            print(f"ID: {livro[0]} , Título: {livro[1]} , Quantidade: {livro[2]}")

    def VerificaClienteBD(self):
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SELECT * FROM clientes where id >= 1")
        vazio = self.cursor.fetchall()
        if not vazio:
            print("Cadastre pelo menos um cliente!")
            return False
        else:
            self.cursor.close()
            return True

    def VerificaLivroVazio(self):
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SELECT * FROM livros where id >= 1")
        vazio = self.cursor.fetchall()
        if not vazio:
            print("Insira pelo menos um livro!")
            return False
        else:
            return True

    # verifica se o campo foi preenchido!
    def VerificaCompradorVazio(self):
        Comprador = int(input("Insira o id do comprador: "))
        if Comprador == "":
            print("O campo precisa ser preenchido!")
            return False
        else:
            return Comprador

    # verifica se o comprador existe no BD!
    def VerificaCompradorExisteBD(self, Comprador):
        self.cursor = self.conexao.cursor()

        self.cursor.execute("SELECT id from clientes where id = ?", (Comprador,))
        existe = self.cursor.fetchone()
        if existe == None:
            print("Cliente não localizado!")
        else:
            self.cursor.close()
            return True

    # verifica o id do livro e realiza a remoção do bd na qnt certa , segundo a transação do cliente!
    def EstoqueLivroRetirar(self):
        self.cursor = self.conexao.cursor()
        Banco_de_dados.listar_livros(self)

        Livro = int(input("Digite o id do livro: "))
        self.cursor.execute("SELECT * FROM livros where id = ?", (Livro,))
        LivroExiste = self.cursor.fetchone()
        if not LivroExiste:
            return False
        else:
            QntLivro = int(input("Digite agora qnt que deseja comprar: "))
            if QntLivro == 0:
                print("Precisa compra mais que um!")
            else:
                self.cursor.execute("SELECT qnt FROM livros where id = ?", (Livro,))
                QntReal = (
                    self.cursor.fetchone()
                )  # retorna em uma tupla o valor "qnt" do id do livro solicitado

                if QntLivro > QntReal[0]:
                    print("Não temos essa quantidade!")
                else:
                    QntLivroNovo = QntReal[0] - QntLivro

                    self.cursor.execute(
                        "UPDATE livros SET qnt = ? where id = ?",
                        (QntLivroNovo, Livro),
                    )
                    self.conexao.commit()
                    print("Livro comprado com sucesso!")
                    transacao = (Livro, QntLivro)
                    self.cursor.close()
                    return transacao

    def ComprarLivro(self):
        self.cursor = self.conexao.cursor()  # conexão com bd
        LivroBD = self.VerificaLivroVazio()
        CompradorVazio = self.VerificaClienteBD()
        if LivroBD and CompradorVazio:
            comprador = Banco_de_dados.VerificaCompradorVazio(self)
            compradorBD = Banco_de_dados.VerificaCompradorExisteBD(self, comprador)
            if comprador and compradorBD:
                Banco_de_dados.EstoqueLivroRetirar(self)

        else:
            return


