class OrdemDeServico:
    # Atributos de classe
    total_os_criadas = 0
    os_abertas = 0

    def __init__(self, cliente: str, descricao: str):
        # Incrementa os contadores da classe
        OrdemDeServico.total_os_criadas += 1
        OrdemDeServico.os_abertas += 1

        # Atributos da instância
        self.id_os = OrdemDeServico.total_os_criadas
        self.cliente = cliente
        self.descricao = descricao
        self.status = "Aberta"

    def finalizar_os(self):
        """Altera o status para 'Concluída' e decrementa o contador de OS abertas."""
        if self.status == "Aberta":
            self.status = "Concluída"
            OrdemDeServico.os_abertas -= 1
            print(f"-> OS #{self.id_os} ({self.cliente}) foi finalizada com sucesso!")
        else:
            print(f"-> OS #{self.id_os} já está concluída.")

    @classmethod
    def verificar_os_abertas(cls):
        """Método de classe para consultar a quantidade atual de ordens abertas."""
        print(f"Ordens de Serviço Abertas: {cls.os_abertas}")
        return cls.os_abertas


# --- Execução e Testes ---

# 1. Instanciando 3 ordens de serviço
os1 = OrdemDeServico("Carlos Silva", "Troca de tela do celular")
os2 = OrdemDeServico("Ana Souza", "Manutenção preventiva em notebook")
os3 = OrdemDeServico("Empresa XYZ", "Configuração de rede e servidor")

print(f"OS 1 criada com ID: {os1.id_os}")
print(f"OS 2 criada com ID: {os2.id_os}")
print(f"OS 3 criada com ID: {os3.id_os}")
print("-" * 40)

# Verificando total de abertas antes de concluir alguma
OrdemDeServico.verificar_os_abertas()
print("-" * 40)

# 2. Concluindo uma ordem de serviço (por exemplo, a os2)
os2.finalizar_os()
print("-" * 40)

# 3. Verificando quantas ordens continuam abertas
OrdemDeServico.verificar_os_abertas()