from models import *
from dao import *
from datetime import datetime


class ControllerCategoria:
    def cadastrarCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        
        for i in x:
            if i.categoria == novaCategoria:
                existe = True
                
        
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso.')
        else:
            print('A categoria que deseja cadastrar já existe')
            
    
    def removerCategoria(self, categoriaRemover):
        x  = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print('A categoria que deseja remover não existe')
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
                
            print('Categoria removida com sucesso')

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')
        
        estoque = DaoEstoque.ler()
        
        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade) if(x.produto.categoria == categoriaRemover) else(x), estoque))
        
        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                           i.produto.categoria + "|" + str(i.quantidade))
                
                arq.writelines('\n')
    

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()            

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if(x.categoria == categoriaAlterar) else(x), x))
                print('A alterção foi efetuada com sucesso.')
                
            else:
                print('A categoria para qual deseja alterar já existe.')  
                 
        else:
            print('A categoria que deseja alterar não existe.')

        
        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')
                
        
        estoque = DaoEstoque.ler()
        
        estoque = list(map(lambda x: Estoque(Produtos(x.nome,x.preco, categoriaAlterada), x.quantidade) if(x.categoria == categoriaAlterada) else(x), estoque))
        
        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                            i.produto.categoria + "|" + str(i.quantidade))
                
                arq.writelines('\n')
    
    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()        

        if len(categorias) == 0:
            print('Categoria vazia.')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')


class ControllerEstoque:
    def cadastrarProduto(self,nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()                 
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso.')
                
            else:
                print('Produto já existe em estoque.')
            
        else:
            print('Categoria inexistente.')
            

    def removerProduto(self, nome):
        x = DaoEstoque.ler()            
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('Produto removido com sucesso.')     
                    
        else:
            print('O produto que deseja remover não existe.')

        
        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                           i.produto.categoria + "|" + str(i.quantidade))
                
                arq.writelines('\n')


    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y  = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == novaCategoria, y))

        if len(h) > 0:
            est = list(filter( lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, x))     
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), x))
                    print('Produto Alterado com sucesso.')
                else:
                    print('Produto já cadastrado.')
            
            else:
                print('O produto que deseja alterar não existe.')
        
        
            with  open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                                i.produto.categoria + "|" + str(i.quantidade))
                    
                    arq.writelines('\n')

        
        else:
            print('A categoria informada não existe.')
        
    
    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()
        
        if len(estoque) ==  0:
            print('Estoque vazio')
        else:
            print("==========Produto==========")
            for i in estoque:
                print(f"Nome: {i.produto.nome}\n"
                      f"Preco: {i.produto.preco}\n"
                      f"Categoria: {i.produto.categoria}\n"
                      f"Quantidade: {i.quantidade}")

            print("--------------------")
        
        
class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False
        
        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= int(quantidadeVendida):
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)
                        
                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)
                        
                        valorDaCompra = int(quantidadeVendida) * int(i.produto.preco)
                        
                        DaoVenda.salvar(vendido)

            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])
            
            
        with open('estoque.txt', 'w') as arq:
            arq.writelines("")
            
        
        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i[0].nome + "|" + i[0].preco + "|" + i[0].categoria + "|" + str(i[1]))
                arq.writelines('\n')        

        if existe == False:
            print('O produto não existe.')
            return None
        
        elif not quantidade:
            print('A quantidade vendidad não contem em estoque.')
            return None

        else:
            print('Venda realizada com sucesso.')
            return valorDaCompra
            
    
    def  relatorioProdutos(self):
        vendas = DaoVenda.ler()
        produtos = []
        for i in vendas:
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            print(tamanho)
            if len(tamanho)> 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)} 
                                if(x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})
            
            
        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esses são os produtos mais vendidos.')
        a  = 1 
        for i in ordenado:
            print(f"==========Produto [{a}]==========")
            print(f"Produto: {i['produto']}\n"
                    f"Quantidade: {i['quantidade']}\n")
            
            a +=1


    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino, '%d/%m/%Y')
        
        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y' ) >= dataInicio1
                                        and datetime.strptime(x.data, "%d/%m/%Y") <= dataTermino1, vendas))
        
        cont = 1
        total = 0
        for i in vendasSelecionadas:
            print(f"========== Venda [{cont}] ==========")
            print(f"Nome: {i.itensVendido.nome}\n"
                  f"Categoria: {i.itensVendido.categoria}\n"
                  f"Data: {i.data}\n"
                  f"Quantidade: {i.quantidadeVendida}\n"
                  f"Cliente: {i.comprador}\n"
                  f"Vendedor: {i.vendedor}\n"
                  )
            
            total += int(i.itensVendido.preco) * int(i.quantidadeVendida)
            cont += 1
            
        print(f"Total vendido: {total}")


class ControllerFornecedor:
    def cadastrarFornecedor(self,nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()

        listCnpj = list(filter(lambda x: x.cnpj == cnpj, x)) 
        listTelefone = list(filter(lambda x: x.cnpj == cnpj, x))

        if len(listCnpj) > 0:
            print('O cnpj já existe')
        
        elif len(listTelefone) > 0:
            print('O Telefone já existe.')
            
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) >=10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
                print('Fornecedor Cadastrado como sucesso.')
                
            else:
                print('Digite um cpf ou um telefine válido.')

        
    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novaCategoria):
        x = DaoFornecedor.ler()

        forn = [i for i in x if i.nome == nomeAlterar]
        
        if len(forn) > 0:
            forn1 = [i for i in x if i.cnpj == novoCnpj]
            if len(forn1) == 0:
                y = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novaCategoria) if(x.nome == nomeAlterar) else(x), y))
                print('Forncedor cadastrado com sucesso.')
            else:
                print('O Forncedor já existe.')
        
            
            with open('fornecedores.txt', 'r') as arq:    
                for i in y:
                    arq.writelines(i.nome + "|" + i.cnpj + "|" + 
                            i.telefone + "|" + i.categoria)
                    
                    arq.writelines('\n')

        else:
            print('O Fornecedor não existe.')
            
 
    def removerForncedor(self, nome):
        x = DaoFornecedor.ler()
        
        y = [i for i in x if x.nome == nome]
        if len(y) > 0:
            for i in range(len(y)):
                if x[i] == nome:
                    del x[i]
                    break
            print('Removido com sucesso.')
        else:
            print('O Forncedor não existe.')
            
        with open('fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + 
                            i.telefone + "|" + i.categoria)
                
                arq.writelines('\n') 
            
    
    def motrarFornecedor(self):
        fornecedores = DaoFornecedor.ler()
        
        if len(fornecedores) == 0:
            print('Não há fornecedor.')
        else:
            n = 1
            for i in fornecedores:
                print(f'==========Fornecedor [{n}]==========')
                print(f'Nome: {i.nome}\n'
                      f'Cnpj: {i.cnpj}\n'
                      f'Telefone: {i.telefone}\n'
                      f'Categoria: {i.categoria}\n')
                print('-------------------------------------')
                n += 1
    
    
class ControllerCliente:
    def cadastrarCliente(self, nome, telefone, cpf, email, endereco ):
        x  = DaoPessoa.ler()

        listCpf = list(filter(lambda x: x.cpf == cpf, x))
        listTelefone = list(filter(lambda x: x.cpf == cpf, x))
       
        if len(listCpf) > 0:
            print('O Cpf já foi cadastrado.')
        elif len(listTelefone) > 0:
            print('O Telefone já foi cadastrado.')
        else:
            if len(cpf) == 14 and len(telefone) <= 11 and len(telefone) >=10:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso.')
            else:
                print('Digite o cpf ou um número válido.')

    
    def alterarCliente(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEndereco):
        x = DaoPessoa.ler()

        y = [i for i in x if i.nome == nomeAlterar]
        
        if len(y) > 0:
            h = [i for i in x if i.nome == novoNome]
            if len(h) == 0:
                cli = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEndereco) if(x.nome == novoNome) else(x),cli))
                print('Cliente alterado com sucesso.')
            
            else:
                print('O Cliente já existe')
                
            with open('clientes.txt', 'w') as arq:
                for i in cli:
                    arq.writelines(cli.nome + "|" + cli.telefone + "|" +
                            cli.cpf + "|" + cli.email + "|" +
                            cli.endereco)
                    
                    arq.writelines('\n')
            
        else:
            print('O Cliente que deseja alterar não existe.')
        
   
    def removerCliente(self, nome):
        x = DaoPessoa.ler()

        cli = [i for i in x if i.nome == nome]
        if len(cli) > 0:
            for i in range(len(cli)):
                del cli[i]
                break
            print('Cliente deletado com sucesso.')
        else:
            print('O Cliente não existe.')
            
        with open('clientes.txt', 'w') as arq:
            for i in cli:
                arq.writelines(cli.nome + "|" + cli.telefone + "|" +
                                cli.cpf + "|" + cli.email + "|" +
                                cli.endereco)
    
    
    def motrarCliente(self):
        clientes = DaoPessoa.ler()
        
        if len(clientes) == 0:
            print('Não possui clientes.')
        else:
            x = 1
            for i in clientes:
                print(f"==========Cliente [{x}]==========")
                print(f"Nome: {i.nome}\n"
                      f"Telefone: {i.telefone}\n"
                      f"Cpf: {i.categoria}\n"
                      f"Endereço: {i.endereco}"
                )

                print("---------------------------")
                x += 1


class ControllerFuncionario:
    def cadastrarFuncionario(self,clt, nome, telefone, cpf, email, endereco):
        x  = DaoFuncionario.ler()

        listClt = list(filter(lambda x: x.clt == clt, x))
        listTelefone = list(filter(lambda x: x.telefone == telefone, x))
       
        if len(listClt) > 0:
            print('O clt já foi cadastrado.')
        elif len(listTelefone) > 0:
            print('O telefone já foi cadastrado.')
        else:
            if len(clt) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFuncionario.salvar(Funcionario(nome, telefone, cpf, email, endereco, clt))
                print('Funcionario cadastrado com sucesso.')
            else:
                print('Digite o clt ou um número válido.')
        
          
    def alterarFuncionario(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco, NovoClt):
        x = DaoFuncionario.ler()

        y = [i for i in x if i.nome == nomeAlterar]
        
        if len(y) > 0:
            h = [i for i in x if i.nome == novoNome]
            if len(h) == 0:
                cli = list(map(lambda x: Funcionario(Pessoa(novoNome, novoTelefone, novoCpf, novoEndereco), NovoClt) if(x.nome == novoNome) else(x),cli))
                print('Funcionario alterado com sucesso.')
            
            else:
                print('O Funcionarios já existe')
                
            with open('funcionarios.txt', 'w') as arq:
                for i in cli:
                    arq.writelines(cli.nome + "|" + cli.telefone + "|" +
                            cli.cpf + "|" + cli.email + "|" +
                            cli.endereco)
                    
                    arq.writelines('\n')
            
        else:
            print('O Funcionario que deseja alterar não existe.')
        
   
    def removerFuncionario(self, nome):
        x = DaoFuncionario.ler()
        
        funcionario = [i for i in x if i.nome == nome]
        if len(funcionario) > 0:
            for i in range(len(funcionario)):
                del funcionario[i]
                break
            print('Cliente deletado com sucesso.')
        else:
            print('O Cliente não existe.')
            
        with open('clientes.txt', 'w') as arq:
            for i in funcionario:
                arq.writelines(funcionario.nome + "|" + funcionario.telefone + "|" +
                                funcionario.cpf + "|" + funcionario.email + "|" +
                                funcionario.endereco)
    
    def motrarFuncionario(self):
        funcionarios = DaoFuncionario.ler()
        
        if len(funcionarios) == 0:
            print('Não possui clientes.')
        else:
            x = 1
            for i in funcionarios:
                print(f"==========Cliente [{x}]==========")
                print(f"Nome: {i.pessoa.nome}\n"
                      f"Telefone: {i.pessoa.telefone}\n"
                      f"Cpf: {i.pessoa.categoria}\n"
                      f"Endereço: {i.pessoa.endereco}"
                      f"Clt: {i.clt}")

                print("---------------------------")
                x += 1

