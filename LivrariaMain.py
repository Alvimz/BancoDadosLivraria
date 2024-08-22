import LivrariaMini 

Executa = LivrariaMini.Banco_de_dados()
Executa.BancoExiste()
Executa.criarTabelas()

while True:
    print('Selecione o que deseja fazer!')
    print('1 - Cadastrar cliente!')
    print('2 - Cadastrar Livro!')
    print('3 - Cadastro transação!')
    print('4 - Sair')
    acao = int(input(">"))
    if acao == 1:
        Executa.InserirCliente()
    elif acao == 2:
        Executa.NovoLivro()
    elif acao == 3:
        Executa.ComprarLivro()
    elif acao == 4:
        break
    else:
        print("Opção inválida!")
        
    