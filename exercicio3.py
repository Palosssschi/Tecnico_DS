
saldo = 1000
preco = 990

print("Selecione o Método de Pagamento: \n")
print("1- Pix\n")
print("2- Débito\n")
print("3- Crédito\n")
print("4- Dinheiro\n")

case_pag = int(input("Digite aqui:"))

match case_pag:
    case 1:
        print("\nPix selecinado")
        metodo_pag = "pix"
    case 2:
        print("\nDébito selecinado")
        metodo_pag = "débito"
    case 3:
        print("\nCrédito selecinado")
        metodo_pag = "crédito"
    case 4:
        print("\nDinheiro selecinado")
        metodo_pag = "dinheiro"
    case _:
        print("\nMetodo invalido")
        metodo_pag = "pagamento invalido"

if (preco > saldo):
    print("Voce não pode pagar isso")
else:
    print("\n\nNota fiscal\n")
    print("R$", preco," esse preço foi pago em ", metodo_pag)
