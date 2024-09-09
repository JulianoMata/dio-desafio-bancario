import time  # Importa o módulo time para usar a função sleep

class Banco:
    def __init__(self):
        # Inicializa o saldo, as listas de depósitos e saques, e a contagem de saques diários
        self.saldo = 0.0
        self.depositos = []
        self.saques = []
        self.saques_diarios = 0

    def depositar(self, valor):
        # Verifica se o valor do depósito é positivo
        if valor > 0:
            # Adiciona o valor ao saldo e armazena o depósito
            self.saldo += valor
            self.depositos.append(valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito deve ser positivo.")

    def sacar(self, valor):
        # Verifica se o limite de saques diários foi atingido
        if self.saques_diarios >= 3:
            print("Limite de 3 saques diários atingido.")
        # Verifica se o valor do saque é superior ao limite permitido
        elif valor > 500:
            print("O limite máximo por saque é de R$ 500.00.")
        # Verifica se há saldo suficiente para realizar o saque
        elif valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
        # Verifica se o valor do saque é positivo
        elif valor > 0:
            # Deduz o valor do saldo, armazena o saque e incrementa a contagem de saques diários
            self.saldo -= valor
            self.saques.append(valor)
            self.saques_diarios += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de saque deve ser positivo.")

    def extrato(self):
        # Define as sequências de escape ANSI para cor verde e reset
        verde = "\033[92m"
        reset = "\033[0m"

        # Imprime o cabeçalho do extrato na cor verde
        print(f"{verde}\n=-=-=-=-=-=-=-=-=-=-= EXTRATO =-=-=-=-=-=-=-=-=-=-=")
        
        # Verifica se não há depósitos e saques
        if not self.depositos and not self.saques:
            print("Não há movimentações na conta.")
        else:
            # Imprime todos os depósitos
            print("Depósitos:")
            for deposito in self.depositos:
                print(f"R$ {deposito:.2f}")
            # Imprime todos os saques
            print("\nSaques:")
            for saque in self.saques:
                print(f"R$ {saque:.2f}")
                
        # Imprime o saldo atual e o rodapé do extrato
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={reset}")

def menu():
    banco = Banco()  # Cria uma instância da classe Banco

    while True:
        # Exibe o menu de opções para o usuário
        print("\nEscolha uma operação:")
        print("1. Depósito")
        print("2. Saque")
        print("3. Extrato")
        print("4. Sair")
        opcao = input("Digite o número da operação desejada: ")

        # Processa a escolha do usuário
        if opcao == "1":
            valor = float(input("Digite o valor do depósito: "))
            banco.depositar(valor)
        elif opcao == "2":
            valor = float(input("Digite o valor do saque: "))
            banco.sacar(valor)
        elif opcao == "3":
            banco.extrato()
        elif opcao == "4":
            print("Saindo...")
            time.sleep(5)  # Pausa de 5 segundos antes de sair
            break
        else:
            print("Opção inválida. Tente novamente.")

# Ponto de entrada do programa
if __name__ == "__main__":
    menu()
