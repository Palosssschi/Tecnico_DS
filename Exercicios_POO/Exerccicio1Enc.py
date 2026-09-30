class Animal:
    def __init__(self, nome, especie):
        self.nome = nome
        self.especie = especie

    def fazerSom(self):
        print(f"{self.nome} esta fazendo barulho")


class Cachorro(Animal):
    def __init__(self, nome, especie):
        super().__init__(nome, especie)

    def fazerSom(self):
        print(f"{self.nome} esta fazendo: AUAU")


class Gato(Animal):
    def __init__(self, nome, especie):
        super().__init__(nome, especie)

    def fazerSom(self):
        print(f"{self.nome} esta fazendo: Miau")


class Vaca(Animal):
    def __init__(self, nome, especie):
        super().__init__(nome, especie)

    def fazerSom(self):
        print(f"{self.nome} esta fazendo: MUMU")


# Instanciação dos objetos
cao = Cachorro("Bob", "canino")
gato = Gato("Claudio", "Felino")
vaca = Vaca("Olinda", "Bovino")

# Testando a execução
cao.fazerSom()
gato.fazerSom()
vaca.fazerSom()