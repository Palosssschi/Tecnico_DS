class CofreDigital():
    def __init__(self, titular, senha: str , saldo = 0.0):
        self.titular = titular
        self.__senha = senha [:4]
        self.__saldo = saldo

    def depositar(self, valor):
        self.__saldo += valor
        print(f"Seu saldo atual é de {self.__saldo}")

    def sacar(self, valor, senha_digitada):
        if (senha_digitada == self.__senha) :
            self.__saldo -= valor
            print(f"Seu saldo atual é de {self.__saldo}")
        else:
            print("Senha incorreta")
conta_carlos = CofreDigital("Carlos", "8920", 200.0)
conta_carlos.depositar(100.0)
conta_carlos.sacar(300.0, "8920")
