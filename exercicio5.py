
try:
    idade = float(input("Digite o ano em que voce nasceu: "))
    subtracao = 2026 - idade
    try:
        try:
            if subtracao >= 18:
                print("Voce é maior de idade")
            try:
                print("Voce tem " + str(subtracao) + " anos")
            except (subtracao > 116):
                print("Voce é um idoso que já morreu")
        except (subtracao < 18):
            print("Voce é menor de idade")
    except (subtracao <= 0):
        print("Voce é uma criança que ainda não nasceu")
except :
    print("Voce tentou passar um dado que não é um numero")