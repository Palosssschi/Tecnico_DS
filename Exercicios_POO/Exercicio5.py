class Produto:
    def __init__(self, nome: str, preco: float, estoque: int):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def reduzir_estoque(self, quantidade: int) -> bool:
        """Reduz a quantidade do produto no estoque caso haja saldo suficiente."""
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return True
        print(f"Estoque insuficiente de '{self.nome}'. Restantes: {self.estoque}")
        return False


class CarrinhoDeCompras:
    def __init__(self):
        self.produtos = []

    def adicionar_ao_carrinho(self, produto: Produto, quantidade: int):
        """Adiciona uma tupla (produto, quantidade) à lista de produtos."""
        if produto.estoque >= quantidade:
            self.produtos.append((produto, quantidade))
            print(f"-> Adicionado: {quantidade}x {produto.nome} ao carrinho.")
        else:
            print(f"-> Não foi possível adicionar {produto.nome}. Estoque disponível: {produto.estoque}")

    def mostrar_carrinho(self):
        """Exibe todos os produtos, quantidades, subtotais e o total do carrinho."""
        if not self.produtos:
            print("\nO carrinho está vazio.")
            return

        print("\n=== ITENS NO CARRINHO ===")
        total = 0.0
        for produto, quantidade in self.produtos:
            subtotal = produto.preco * quantidade
            total += subtotal
            print(f"- {produto.nome} | Qtd: {quantidade} | Preço un.: R$ {produto.preco:.2f} | Subtotal: R$ {subtotal:.2f}")
        
        print(f"Total a pagar: R$ {total:.2f}")
        print("=========================\n")

    def finalizar_compra(self):
        """Efetiva a compra e atualiza o estoque dos produtos adquiridos."""
        if not self.produtos:
            print("Carrinho vazio. Nenhuma compra realizada.")
            return

        print("\nFinalizando compra e atualizando estoques...")
        for produto, quantidade in self.produtos:
            produto.reduzir_estoque(quantidade)
        
        self.produtos.clear()
        print("Compra efetuada com sucesso!")



notebook = Produto("Notebook", 3500.00, 5)
mouse = Produto("Mouse Sem Fio", 80.00, 10)
carrinho = CarrinhoDeCompras()
carrinho.adicionar_ao_carrinho(notebook, 2)
carrinho.adicionar_ao_carrinho(mouse, 1)
carrinho.mostrar_carrinho()
carrinho.finalizar_compra()

print(f"Estoque restante de '{notebook.nome}': {notebook.estoque}")
print(f"Estoque restante de '{mouse.nome}': {mouse.estoque}")