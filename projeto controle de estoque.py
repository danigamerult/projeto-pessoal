import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

# Dados
produtos = {}  
# estrutura: {codigo: { 'nome': ..., 'preco': float, 'quantidade': int, 'minimo': int }}
movimentacoes = []  
# lista de tuplas: (timestamp, tipo, codigo, nome, quantidade, nota)

# Funções úteis

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

def gravar_movimentacao(tipo, codigo, nome, quantidade, nota=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movimentacoes.append((timestamp, tipo, codigo, nome, quantidade, nota))

def voltar_menu():
    limpar_tela()
    titulo = tk.Label(root, text="📦 Sistema de Controle de Estoque", font=("Helvetica", 20, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=20)

    botoes = [
        ("➕ Cadastrar Produto", cadastrar_produto),
        ("📥 Entrada de Estoque", entrada_estoque),
        ("📤 Saída de Estoque", saida_estoque),
        ("✏️ Ajustar Estoque", ajustar_estoque),
        ("🔍 Buscar Produto", buscar_produto),
        ("📋 Relatórios", mostrar_relatorios),
        ("📦 Listar Produtos", listar_produtos),
        ("🗑️ Deletar Produto", deletar_produto),
        ("❌ Sair", root.quit)
    ]
    for texto, comando in botoes:
        btn = tk.Button(root, text=texto, command=comando,
                        font=("Helvetica", 12, "bold"), bg="#00796b", fg="white", width=25)
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#009688"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#00796b"))

# Funcionalidades

def cadastrar_produto():
    limpar_tela()
    titulo = tk.Label(root, text="➕ Cadastrar Produto", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    # Campos
    label_codigo = tk.Label(root, text="Código do produto:", bg="#004d40", fg="white")
    label_codigo.pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack(pady=5)

    label_nome = tk.Label(root, text="Nome:", bg="#004d40", fg="white")
    label_nome.pack()
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)

    label_preco = tk.Label(root, text="Preço unitário:", bg="#004d40", fg="white")
    label_preco.pack()
    entry_preco = tk.Entry(root)
    entry_preco.pack(pady=5)

    label_quant = tk.Label(root, text="Quantidade inicial:", bg="#004d40", fg="white")
    label_quant.pack()
    entry_quant = tk.Entry(root)
    entry_quant.pack(pady=5)

    label_minimo = tk.Label(root, text="Quantidade mínima:", bg="#004d40", fg="white")
    label_minimo.pack()
    entry_minimo = tk.Entry(root)
    entry_minimo.pack(pady=5)

    def salvar():
        codigo = entry_codigo.get().strip()
        nome = entry_nome.get().strip()
        try:
            preco = float(entry_preco.get())
            quantidade = int(entry_quant.get())
            minimo = int(entry_minimo.get())
        except ValueError:
            messagebox.showwarning("Erro", "Preço deve ser número e quantidades devem ser inteiros.")
            return

        if not codigo or not nome:
            messagebox.showwarning("Erro", "Código e nome são obrigatórios.")
            return
        if codigo in produtos:
            messagebox.showwarning("Erro", "Código já existe.")
            return

        produtos[codigo] = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'minimo': minimo
        }
        gravar_movimentacao("Cadastro", codigo, nome, quantidade, nota="Inicial")
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso.")
        voltar_menu()

    btn_salvar = tk.Button(root, text="Salvar", command=salvar, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold"))
    btn_salvar.pack(pady=10)
    btn_voltar = tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold"))
    btn_voltar.pack(pady=5)

def entrada_estoque():
    limpar_tela()
    titulo = tk.Label(root, text="📥 Entrada de Estoque", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    label_codigo = tk.Label(root, text="Código do produto:", bg="#004d40", fg="white")
    label_codigo.pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack(pady=5)

    label_quant = tk.Label(root, text="Quantidade a adicionar:", bg="#004d40", fg="white")
    label_quant.pack()
    entry_quant = tk.Entry(root)
    entry_quant.pack(pady=5)

    def realizar_entrada():
        codigo = entry_codigo.get().strip()
        try:
            quant = int(entry_quant.get())
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser inteiro.")
            return

        if codigo not in produtos:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return

        produtos[codigo]['quantidade'] += quant
        gravar_movimentacao("Entrada", codigo, produtos[codigo]['nome'], quant, nota="")
        messagebox.showinfo("Sucesso", f"Entrada feita: +{quant} unidades de {produtos[codigo]['nome']}.")
        voltar_menu()

    tk.Button(root, text="Confirmar", command=realizar_entrada, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

def saida_estoque():
    limpar_tela()
    titulo = tk.Label(root, text="📤 Saída de Estoque", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    label_codigo = tk.Label(root, text="Código do produto:", bg="#004d40", fg="white")
    label_codigo.pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack(pady=5)

    label_quant = tk.Label(root, text="Quantidade a remover:", bg="#004d40", fg="white")
    label_quant.pack()
    entry_quant = tk.Entry(root)
    entry_quant.pack(pady=5)

    def realizar_saida():
        codigo = entry_codigo.get().strip()
        try:
            quant = int(entry_quant.get())
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser inteiro.")
            return

        if codigo not in produtos:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return
        if produtos[codigo]['quantidade'] < quant:
            messagebox.showwarning("Erro", "Quantidade insuficiente no estoque.")
            return

        produtos[codigo]['quantidade'] -= quant
        gravar_movimentacao("Saída", codigo, produtos[codigo]['nome'], quant, nota="")
        messagebox.showinfo("Sucesso", f"Saída feita: -{quant} unidades de {produtos[codigo]['nome']}.")
        voltar_menu()

    tk.Button(root, text="Confirmar", command=realizar_saida, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

def ajustar_estoque():
    limpar_tela()
    titulo = tk.Label(root, text="✏️ Ajustar Estoque", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    label_codigo = tk.Label(root, text="Código do produto:", bg="#004d40", fg="white")
    label_codigo.pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack(pady=5)

    label_quant = tk.Label(root, text="Nova quantidade:", bg="#004d40", fg="white")
    label_quant.pack()
    entry_quant = tk.Entry(root)
    entry_quant.pack(pady=5)

    def realizar_ajuste():
        codigo = entry_codigo.get().strip()
        try:
            nova = int(entry_quant.get())
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser inteiro.")
            return

        if codigo not in produtos:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return

        antigo = produtos[codigo]['quantidade']
        produtos[codigo]['quantidade'] = nova
        diferenca = nova - antigo
        gravar_movimentacao("Ajuste", codigo, produtos[codigo]['nome'], diferenca, nota=f"Ajuste de {antigo} → {nova}")
        messagebox.showinfo("Sucesso", f"Estoque do produto {produtos[codigo]['nome']} ajustado de {antigo} para {nova}.")
        voltar_menu()

    tk.Button(root, text="Confirmar", command=realizar_ajuste, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

def buscar_produto():
    limpar_tela()
    titulo = tk.Label(root, text="🔍 Buscar Produto", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    label_busca = tk.Label(root, text="Código ou Nome:", bg="#004d40", fg="white")
    label_busca.pack()
    entry_busca = tk.Entry(root, width=30)
    entry_busca.pack(pady=5)

    def realizar_busca():
        termo = entry_busca.get().strip().lower()
        achados = []
        for codigo, info in produtos.items():
            if termo == codigo.lower() or termo in info['nome'].lower():
                achados.append((codigo, info))
        if not achados:
            messagebox.showinfo("Busca", "Nenhum produto encontrado.")
        else:
            resultado = ""
            for codigo, info in achados:
                resultado += f"Código: {codigo}\nNome: {info['nome']}\nPreço unit: {info['preco']:.2f}\nQuantidade: {info['quantidade']}\nQtd mínima: {info['minimo']}\n\n"
            messagebox.showinfo("Resultados", resultado)

    tk.Button(root, text="Buscar", command=realizar_busca, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

def mostrar_relatorios():
    limpar_tela()
    titulo = tk.Label(root, text="📋 Relatórios", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    # Relatório produtos abaixo do mínimo
    abaixo = [(codigo, info) for codigo, info in produtos.items() if info['quantidade'] < info['minimo']]
    tk.Label(root, text="Produtos abaixo da quantidade mínima:", bg="#004d40", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
    if not abaixo:
        tk.Label(root, text="Nenhum produto abaixo do mínimo.", bg="#004d40", fg="white").pack()
    else:
        for codigo, info in abaixo:
            txt = f"{codigo}: {info['nome']} - Qtd: {info['quantidade']} (mín:{info['minimo']})"
            tk.Label(root, text=txt, bg="#004d40", fg="white").pack()

    # Relatório valor total em estoque
    total_valor = sum(info['preco'] * info['quantidade'] for info in produtos.values())
    tk.Label(root, text=f"\nValor total do estoque: R$ {total_valor:.2f}", bg="#004d40", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

    tk.Button(root, text="Ver Histórico", command=mostrar_historico, bg="#00796b", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

def mostrar_historico():
    # Mostra todas as movimentações
    historico = ""
    for m in movimentacoes:
        ts, tipo, codigo, nome, quant, nota = m
        historico += f"{ts} | {tipo} | {codigo} | {nome} | qtd {quant} | {nota}\n"
    if not historico:
        messagebox.showinfo("Histórico", "Nenhuma movimentação registrada")
    else:
        # mostrar em uma janela pop-up scrollável
        top = tk.Toplevel(root)
        top.title("Histórico de Movimentações")
        top.configure(bg="#eceff1")
        text = tk.Text(top, width=80, height=20)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, historico)
        # desabilitar edição
        text.config(state=tk.DISABLED)
        btn = tk.Button(top, text="Fechar", command=top.destroy, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold"))
        btn.pack(pady=5)

def listar_produtos():
    limpar_tela()
    titulo = tk.Label(root, text="📦 Lista de Produtos", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)
    if not produtos:
        tk.Label(root, text="Nenhum produto cadastrado.", bg="#004d40", fg="white").pack()
    else:
        for codigo, info in produtos.items():
            txt = f"{codigo} | {info['nome']} | Preço: {info['preco']:.2f} | Qtde: {info['quantidade']} | Mín: {info['minimo']}"
            tk.Label(root, text=txt, bg="#004d40", fg="white").pack(anchor="w", padx=20)

    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

def deletar_produto():
    limpar_tela()
    titulo = tk.Label(root, text="🗑️ Deletar Produto", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
    titulo.pack(pady=10)

    label_codigo = tk.Label(root, text="Código do produto:", bg="#004d40", fg="white")
    label_codigo.pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack(pady=5)

    def confirmar_delecao():
        codigo = entry_codigo.get().strip()
        if codigo not in produtos:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return
        nome = produtos[codigo]['nome']
        # confirmar
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar '{nome}'?"):
            del produtos[codigo]
            gravar_movimentacao("Deleção", codigo, nome, 0, nota="Produto removido")
            messagebox.showinfo("Sucesso", f"Produto '{nome}' deletado.")
            voltar_menu()

    tk.Button(root, text="Confirmar", command=confirmar_delecao, bg="#388e3c", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#d32f2f", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

# Janela principal
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("500x600")
root.configure(bg="#004d40")

voltar_menu()
root.mainloop()
