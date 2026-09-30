nome = "Alberto"
usuario_antigo = True
admin = True

mensagem = "Olá adm!" if admin == True or usuario_antigo == True else "Olá usuario!"
mensagem2 = f"Olá {nome}!" if admin == True and usuario_antigo == True else "Olá usuario!"

print(mensagem2)

test  = 2
print("abacate" if test >= 2 else "Goiaba")