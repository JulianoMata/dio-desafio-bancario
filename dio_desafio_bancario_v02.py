import time # Módulo para trabalhar com tempo
import textwrap # Módulo para facilitar a formatação de texto

class Cliente:   
    def __init__(self, cpf, nome, data_nascimento, celular, email, endereco):   # Método construtor
        self.cpf = cpf 
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.celular = celular
        self.email = email
        self.endereco = endereco

class Conta:
    def __init__(self, numero_conta, agencia='0001'):  # Método construtor
        self.numero_conta = numero_conta 
        self.agencia = agencia 
        self.saldo = 0.0 
        self.extrato = []
        self.saques_dia = 0

    def depositar(self, saldo, valor, extrato): 
        if valor <= 0:
            print('O valor do depósito deve ser maior que zero.')
            return saldo, extrato

        saldo += valor
        extrato.append(f'Depósito:'.ljust(15) + f'R$ {valor:.2f}')
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso.')
        return saldo, extrato

    def sacar(self, *, saldo, valor, extrato, limite=500, limite_saques=3):  
        if valor <= 0:
            print('O valor do saque deve ser maior que zero.')
            return saldo, extrato

        if self.saques_dia >= limite_saques:
            print('Limite diário de saques atingido.') 
            return saldo, extrato  

        if valor > limite:
            print(f'O valor excede o limite de saque permitido de R$ {limite:.2f}.')  
            return saldo, extrato  

        if valor > saldo:
            print('Saldo insuficiente.')
            return saldo, extrato

        saldo -= valor
        extrato.append(f'Saque:'.ljust(15) + f'R$ {valor:.2f}')
        self.saques_dia += 1
        print(f'Saque de R$ {valor:.2f} realizado com sucesso.')
        return saldo, extrato

class Banco:
    def __init__(self): # Método construtor
        self.clientes = {} # Dicionário vazio
        self.contas = {} # Dicionário vazio 
        self.numero_conta = 1001  # Número da conta

    def criar_cliente(self): 
        cpf = input('Digite o CPF (somente números): ')
        while len(cpf) != 11 or not cpf.isdigit():
            print('O CPF deve conter 11 dígitos numéricos.')
            cpf = input('Digite o CPF (somente números): ')

        if cpf in self.clientes:
            print('Já existe um cliente cadastrado com esse CPF.')
            return

        nome = input('Digite o nome do cliente: ').upper()
        data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ')
        while not self.validar_data_nascimento(data_nascimento): # Enquanto a data de nascimento for inválida
            print('Data de nascimento inválida. O formato deve ser dd/mm/aaaa.')
            data_nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ')

        celular = input('Digite o número de celular: ') or 'Não informado'
        email = input('Digite o e-mail: ') or 'Não informado'

        logradouro = input('Digite o logradouro: ')
        while True:
            numero = input('Digite o número: ')
            if numero.isdigit(): # Verifica se o valor é um número
                break
            else:
                print('Número inválido. Deve ser um número inteiro.')
        bairro = input('Digite o bairro: ')
        cidade = input('Digite a cidade: ')
        uf = input('Digite a UF (sigla do estado): ')

        endereco = f'{logradouro}, {numero} - {bairro} - {cidade}/{uf}'
        self.clientes[cpf] = Cliente(cpf, nome, self.formatar_data(data_nascimento), celular, email, endereco)
        print(f'Cliente {nome} criado com sucesso.')

    def criar_conta(self):
        cpf = input('Digite o CPF do cliente: ')
        if cpf not in self.clientes: # Se o CPF não estiver no dicionário de clientes
            print('Cliente não encontrado. Verifique o CPF e tente novamente.')
            return

        conta = Conta(self.numero_conta)
        self.contas.setdefault(cpf, []).append(conta) # Adiciona a conta ao cliente
        print(f'Conta {self.numero_conta} criada com sucesso para o cliente {self.clientes[cpf].nome}.')
        self.numero_conta += 1

    def escolher_conta(self, cpf):
        contas_cliente = self.contas.get(cpf, []) # Retorna uma lista vazia se o CPF não existir
        if not contas_cliente:
            print(f'Cliente {self.clientes[cpf].nome} não possui contas.')
            return None

        print(f'\nContas do cliente {self.clientes[cpf].nome}:')
        for idx, conta in enumerate(contas_cliente): # Enumera a lista de contas
            print(f'{idx + 1}. Agência: {conta.agencia} - Conta Nº: {conta.numero_conta}')

        while True:
            escolha = input('Escolha o número da conta: ')
            if escolha.isdigit() and 1 <= int(escolha) <= len(contas_cliente): # Verifica se a escolha é um número e se está dentro do intervalo
                return contas_cliente[int(escolha) - 1]
            else:
                print('Escolha inválida. Tente novamente.')

    def solicitar_valor(self, tipo): 
        while True:
            valor = input(f'Digite o valor do {tipo}: R$ ')
            try:
                valor_float = float(valor)
                if valor_float > 0:
                    return valor_float 
                else:
                    print('O valor deve ser maior que zero.')
            except ValueError:  
                print('Valor inválido. Digite um número.')

    def exibir_extrato(self, saldo, *, extrato):
        print('\n=-=-=-=-=-=-=-=-=-=-= EXTRATO =-=-=-=-=-=-=-=-=-=-=')
        if extrato:
            for transacao in extrato:
                print(transacao)
        else:
            print('Nenhuma transação realizada.')
        print(f'Saldo:'.ljust(15) + f'R$ {saldo:.2f}') 
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    def listar_contas(self):
        if self.contas:
            print('\n=-=-=-=-=-=-=-=-=-=-= LISTA DE CONTAS =-=-=-=-=-=-=-=-=-=-=')
            for cpf, contas_cliente in self.contas.items():  
                cliente = self.clientes[cpf]
                cpf_formatado = self.formatar_cpf(cpf)
                for conta in contas_cliente:
                    print(f'\tAgência:'.ljust(15) + f'{conta.agencia}')
                    print(f'\tConta Nº:'.ljust(15) + f'{conta.numero_conta}')
                    print(f'\tCliente:'.ljust(15) + f'{cliente.nome}')
                    print(f'\t'.ljust(15) + f'(CPF: {cpf_formatado})\n')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        else:
            print('\tNenhuma conta cadastrada.')

    def validar_data_nascimento(self, data): 
        try:
            dia, mes, ano = map(int, data.split('/')) # Converte os valores para inteiros
            return 1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2024 # Verifica se a data é válida
        except ValueError: # Se houver erro na conversão
            return False

    def formatar_data(self, data):
        dia, mes, ano = data.split('/') 
        return f'{dia}-{mes}-{ano}' 

    def formatar_cpf(self, cpf):
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}' if cpf else None 

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
            print(textwrap.dedent(menu_texto)) # Remove a indentação do texto
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
                time.sleep(5) # Aguarda 5 segundos
                break
            else:
                print('Opção inválida. Tente novamente.')

    def realizar_deposito(self):
        cpf = input('Digite o CPF do cliente: ')
        if cpf in self.clientes:
            valor = self.solicitar_valor('depósito')
            conta_escolhida = self.escolher_conta(cpf)
            if conta_escolhida:
                conta_escolhida.saldo, conta_escolhida.extrato = conta_escolhida.depositar(
                    conta_escolhida.saldo, valor, conta_escolhida.extrato) 
        else:
            print('Cliente não encontrado.')

    def realizar_saque(self):
        cpf = input('Digite o CPF do cliente: ')
        if cpf in self.clientes:
            valor = self.solicitar_valor('saque')
            conta_escolhida = self.escolher_conta(cpf)
            if conta_escolhida:
                conta_escolhida.saldo, conta_escolhida.extrato = conta_escolhida.sacar(
                    saldo=conta_escolhida.saldo, valor=valor, extrato=conta_escolhida.extrato)
        else:
            print('Cliente não encontrado.')

    def mostrar_extrato(self):
        cpf = input('Digite o CPF do cliente: ')
        if cpf in self.clientes:
            conta_escolhida = self.escolher_conta(cpf)
            if conta_escolhida:
                self.exibir_extrato(conta_escolhida.saldo, extrato=conta_escolhida.extrato)
        else:
            print('Cliente não encontrado.')

if __name__ == '__main__':  # Se o módulo for executado como programa principal
    banco = Banco() # Instancia a classe Banco  
    banco.menu() # Chama o método menu
