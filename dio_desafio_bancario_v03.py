import time # Importa o módulo time
import textwrap # Importa o módulo textwrap
from datetime import datetime # Importa a classe datetime

# Classe que representa um Endereço
class Endereco:
    def __init__(self, logradouro, numero, bairro, cidade, uf): # Construtor
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro 
        self.cidade = cidade
        self.uf = uf

    def __str__(self): # Método para representação em string
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.uf}' # Retorna o endereço formatado

# Classe que representa um Cliente
class Cliente:
    def __init__(self, cpf, nome, data_nascimento, celular, email, endereco: Endereco): # Construtor 
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.celular = celular
        self.email = email
        self.endereco = endereco

# Classe que representa uma Agência
class Agencia:
    def __init__(self, numero='0001'): # Construtor
        self.numero = numero # Número da agência

    def __str__(self): # Método para representação em string
        return self.numero

# Classe que representa uma Transação (para uso no extrato)
class Transacao:
    def __init__(self, tipo, valor): # Construtor
        self.tipo = tipo 
        self.valor = valor
        self.data_hora = datetime.now() # Data e hora da transação

    def __str__(self):
        return f'{self.tipo:<10} R$ {self.valor:>10.2f}   - {self.data_hora.strftime("%d/%m/%Y %H:%M")}' # Retorna a transação formatada

# Classe que representa uma Conta Bancária
class Conta:
    def __init__(self, numero_conta, agencia: Agencia): # Construtor
        self.numero_conta = numero_conta
        self.agencia = agencia
        self.saldo = 0.0
        self.extrato = [] # Lista de transações
        self.saques_dia = 0

    def depositar(self, valor): # Método para depósito
        if valor <= 0:
            print('O valor do depósito deve ser maior que zero.')
            return

        self.saldo += valor # Atualiza o saldo
        transacao = Transacao('Depósito', valor) # Cria uma transação
        self.extrato.append(transacao) # Adiciona a transação ao extrato
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso.') 

    def sacar(self, valor, limite=500, limite_saques=3): # Método para saque
        if valor <= 0:
            print('O valor do saque deve ser maior que zero.')
            return

        if self.saques_dia >= limite_saques:
            print('Limite diário de saques atingido.')
            return

        if valor > limite:
            print(f'O valor excede o limite de saque permitido de R$ {limite:.2f}.')
            return

        if valor > self.saldo:
            print('Saldo insuficiente.')
            return

        self.saldo -= valor # Atualiza o saldo
        transacao = Transacao('Saque', valor) # Cria uma transação
        self.extrato.append(transacao) # Adiciona a transação ao extrato
        self.saques_dia += 1 # Atualiza o contador de saques no dia
        print(f'Saque de R$ {valor:.2f} realizado com sucesso.')

# Classe que representa o Banco
class Banco:
    def __init__(self): # Construtor
        self.clientes = {} # Dicionário de clientes
        self.contas = {} # Dicionário de contas
        self.numero_conta = 1 # Número da primeira conta

    def criar_cliente(self): # Método para criar um cliente
        cpf = input('Digite o CPF (somente números): ') 
        while len(cpf) != 11 or not cpf.isdigit(): # Validação do CPF
            print('O CPF deve conter 11 dígitos numéricos.')
            cpf = input('Digite o CPF (somente números): ')

        if cpf in self.clientes:
            print('Já existe um cliente cadastrado com esse CPF.')
            return

        nome = input('Digite o nome do cliente: ').upper() # Converte o nome para maiúsculas
        while not all(c.isalpha() or c.isspace() for c in nome):  # Permite apenas letras e espaços
            print('Nome inválido. O nome deve conter apenas letras e espaços.')
            nome = input('Digite o nome do cliente: ').upper()

        data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ') 
        while not self.validar_data_nascimento(data_nascimento): # Validação da data de nascimento
            print('Data de nascimento inválida. O formato deve ser dd/mm/aaaa.')
            data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ')

        celular = input('Digite o número de celular: ')
        while len(celular) != 11 or not celular.isdigit(): # Validação do celular
            print('O celular deve conter 11 dígitos numéricos.')
            celular = input('Digite o número de celular: ')

        email = input('Digite o e-mail: ').lower()  # Converte o e-mail para minúsculas
        while '@' not in email:  # Verifica se o e-mail contém '@'
            print('E-mail inválido. Deve conter "@"')
            email = input('Digite o e-mail: ').lower()  # Solicita novamente o e-mail

        logradouro = input('Digite o logradouro: ')
        numero = input('Digite o número: ')
        bairro = input('Digite o bairro: ')
        cidade = input('Digite a cidade: ')
        uf = input('Digite a UF: ')
        while len(uf) != 2 or not uf.isalpha(): # Validação da UF
            print('UF inválida. Deve conter exatamente 2 letras.')
            uf = input('Digite a UF (sigla do estado): ').upper() # Converte a UF para maiúsculas

        endereco = Endereco(logradouro, numero, bairro, cidade, uf) # Cria um objeto Endereco
        self.clientes[cpf] = Cliente(cpf, nome, data_nascimento, celular, email, endereco) # Cria um objeto Cliente
        print(f'Cliente {nome} criado com sucesso.')

    def criar_conta(self): # Método para criar uma conta
        cpf = input('Digite o CPF do cliente: ')
        if cpf not in self.clientes: # Verifica se o cliente existe
            print('Cliente não encontrado. Verifique o CPF e tente novamente.')
            return

        agencia = Agencia()  # Agência fixa
        conta = Conta(self.numero_conta, agencia) # Cria uma conta
        self.contas.setdefault(cpf, []).append(conta) # Adiciona a conta ao dicionário de contas
        print(f'Conta {self.numero_conta} criada com sucesso para o cliente {self.clientes[cpf].nome}.')
        self.numero_conta += 1

    def escolher_conta(self, cpf): # Método para escolher uma conta
        contas_cliente = self.contas.get(cpf, []) # Obtém as contas do cliente
        if not contas_cliente:
            print(f'Cliente {self.clientes[cpf].nome} não possui contas.')
            return None

        print(f'\nContas do cliente {self.clientes[cpf].nome}:') # Exibe as contas do cliente
        for idx, conta in enumerate(contas_cliente): # Enumera as contas
            print(f'{idx + 1}. Agência: {conta.agencia} - Conta Nº: {conta.numero_conta}') # Exibe a agência e o número da conta

        while True:
            escolha = input('Escolha o número da conta: ')
            if escolha.isdigit() and 1 <= int(escolha) <= len(contas_cliente): # Valida a escolha
                return contas_cliente[int(escolha) - 1] # Retorna a conta escolhida
            else:
                print('Escolha inválida. Tente novamente.')

    def exibir_extrato(self, conta): # Método para exibir o extrato
        print('\n=-=-=-=-=-=-=-=-=-=-= EXTRATO =-=-=-=-=-=-=-=-=-=-=')
        if conta.extrato:
            for transacao in conta.extrato:
                print(transacao)
        else:
            print('Nenhuma transação realizada.')
        print(f'Saldo      R$ {conta.saldo:>10.2f}') # Exibe o saldo alinhado à direita 
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    def listar_contas(self): # Método para listar as contas
        if self.contas:
            print('\n=-=-=-=-=-=-=-=-=-=-= LISTA DE CONTAS =-=-=-=-=-=-=-=-=-=-=')
            for cpf, contas_cliente in self.contas.items():
                cliente = self.clientes[cpf]
                cpf_formatado = self.formatar_cpf(cpf) # Formata o CPF
                for conta in contas_cliente:
                    print(f'\tAgência:'.ljust(15) + f'{conta.agencia}')
                    print(f'\tConta Nº:'.ljust(15) + f'{conta.numero_conta}')
                    print(f'\tCliente:'.ljust(15) + f'{cliente.nome}')
                    print(f'\t'.ljust(15) + f'(CPF: {cpf_formatado})\n')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        else:
            print('\tNenhuma conta cadastrada.')

    def validar_data_nascimento(self, data): # Método para validar a data de nascimento
        try:
            dia, mes, ano = map(int, data.split('/')) # Divide a data em dia, mês e ano
            return 1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2024 # Valida dia, mês e ano
        except ValueError: # Trata erro de conversão
            return False

    def formatar_cpf(self, cpf):
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}' if cpf else None # Formata o CPF

    def menu(self): # Método para exibir o menu
        while True:
            menu_texto = '''
            \tEscolha uma operação:
            \t1. Depósito
            \t2. Saque
            \t3. Extrato
            \t4. Criar Cliente
            \t5. Criar Conta
            \t6. Listar Contas
            \t7. Sair
            '''
            print(textwrap.dedent(menu_texto)) # Exibe o menu formatado
            opcao = input('Digite o número da operação desejada: ')

            if opcao == '1':
                self.realizar_deposito()
            elif opcao == '2':
                self.realizar_saque()
            elif opcao == '3':
                self.mostrar_extrato()
            elif opcao == '4':
                self.criar_cliente()
            elif opcao == '5':
                self.criar_conta()
            elif opcao == '6':
                self.listar_contas()
            elif opcao == '7':
                print('Saindo do sistema...')
                time.sleep(2) # Aguarda 2 segundos
                break
            else:
                print('Opção inválida. Tente novamente.')

    def realizar_deposito(self): # Método para realizar um depósito
        cpf = input('Digite o CPF do cliente: ')
        if cpf not in self.clientes: # Verifica se o cliente existe
            print('Cliente não encontrado. Verifique o CPF e tente novamente.')
            return

        conta = self.escolher_conta(cpf) # Escolhe a conta 
        if conta:
            valor = float(input('Digite o valor do depósito: '))
            conta.depositar(valor) # Realiza o depósito

    def realizar_saque(self): # Método para realizar um saque
        cpf = input('Digite o CPF do cliente: ')
        if cpf not in self.clientes: # Verifica se o cliente existe
            print('Cliente não encontrado. Verifique o CPF e tente novamente.')
            return

        conta = self.escolher_conta(cpf) # Escolhe a conta
        if conta:
            valor = float(input('Digite o valor do saque: '))
            conta.sacar(valor) # Realiza o saque

    def mostrar_extrato(self): # Método para mostrar o extrato
        cpf = input('Digite o CPF do cliente: ') 
        if cpf not in self.clientes: # Verifica se o cliente existe
            print('Cliente não encontrado. Verifique o CPF e tente novamente.')
            return

        conta = self.escolher_conta(cpf) # Escolhe a conta
        if conta:
            self.exibir_extrato(conta)  # Exibe o extrato


# Inicializando o sistema
if __name__ == '__main__': # Executa o código se o script for executado diretamente
    banco = Banco() # Cria um objeto Banco
    banco.menu() # Exibe o menu
