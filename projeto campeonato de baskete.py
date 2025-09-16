import tkinter as tk
from tkinter import messagebox

# Dados
times = {}
partidas = []

# Funções principais
def cadastrar_time():
    limpar_tela()
    titulo = tk.Label(root, text="Cadastrar Time", font=("Helvetica", 16, "bold"), bg="#1e3c72", fg="white")
    titulo.pack(pady=10)

    label_nome = tk.Label(root, text="Nome do time:", bg="#1e3c72", fg="white")
    label_nome.pack()
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)

    def salvar():
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome não pode ser vazio!")
        elif nome in times:
            messagebox.showinfo("Atenção", "Esse time já está cadastrado.")
        else:
            times[nome] = {"pontos": 0, "vitorias": 0}
            messagebox.showinfo("Sucesso", f"Time '{nome}' cadastrado!")
            voltar_menu()

    tk.Button(root, text="Salvar", command=salvar, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#f44336", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)


def cadastrar_partida():
    limpar_tela()
    if len(times) < 2:
        messagebox.showwarning("Aviso", "Cadastre pelo menos 2 times antes.")
        voltar_menu()
        return

    tk.Label(root, text="Cadastrar Partida", font=("Helvetica", 16, "bold"), bg="#1e3c72", fg="white").pack(pady=10)

    tk.Label(root, text="Time 1:", bg="#1e3c72", fg="white").pack()
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)

    tk.Label(root, text="Time 2:", bg="#1e3c72", fg="white").pack()
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)

    tk.Label(root, text="Pontos Time 1:", bg="#1e3c72", fg="white").pack()
    pontos1 = tk.Entry(root)
    pontos1.pack(pady=5)

    tk.Label(root, text="Pontos Time 2:", bg="#1e3c72", fg="white").pack()
    pontos2 = tk.Entry(root)
    pontos2.pack(pady=5)

    def salvar_partida():
        t1 = entry1.get().strip()
        t2 = entry2.get().strip()
        try:
            p1 = int(pontos1.get())
            p2 = int(pontos2.get())
        except:
            messagebox.showwarning("Erro", "Pontos devem ser números inteiros.")
            return

        if t1 not in times or t2 not in times:
            messagebox.showwarning("Erro", "Um ou ambos os times não estão cadastrados.")
            return
        if t1 == t2:
            messagebox.showwarning("Erro", "Times devem ser diferentes.")
            return

        partidas.append((t1, p1, t2, p2))

        if p1 > p2:
            times[t1]['pontos'] += 3
            times[t1]['vitorias'] += 1
        elif p2 > p1:
            times[t2]['pontos'] += 3
            times[t2]['vitorias'] += 1
        else:
            times[t1]['pontos'] += 1
            times[t2]['pontos'] += 1

        messagebox.showinfo("Sucesso", f"Partida registrada: {t1} {p1} x {p2} {t2}")
        voltar_menu()

    tk.Button(root, text="Salvar", command=salvar_partida, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Voltar", command=voltar_menu, bg="#f44336", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)


def mostrar_tabela():
    limpar_tela()
    tk.Label(root, text="📊 Tabela de Pontuação", font=("Helvetica", 16, "bold"), bg="#1e3c72", fg="white").pack(pady=10)

    if not times:
        tk.Label(root, text="Nenhum time cadastrado.", bg="#1e3c72", fg="white").pack()
    else:
        sorted_times = sorted(times.items(), key=lambda x: (-x[1]['pontos'], -x[1]['vitorias']))
        for nome, stats in sorted_times:
            texto = f"{nome} - Pontos: {stats['pontos']} | Vitórias: {stats['vitorias']}"
            tk.Label(root, text=texto, bg="#1e3c72", fg="white").pack()

    tk.Button(root, text="Voltar", command=voltar_menu, bg="#f44336", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)


def mostrar_time_vitorioso():
    limpar_tela()
    tk.Label(root, text="🏆 Time Vitorioso", font=("Helvetica", 16, "bold"), bg="#1e3c72", fg="white").pack(pady=10)

    if not times:
        tk.Label(root, text="Nenhum time cadastrado.", bg="#1e3c72", fg="white").pack()
    else:
        vencedor = max(times.items(), key=lambda x: (x[1]['pontos'], x[1]['vitorias']))
        texto = f"🏆 {vencedor[0]} - Pontos: {vencedor[1]['pontos']}, Vitórias: {vencedor[1]['vitorias']}"
        tk.Label(root, text=texto, bg="#1e3c72", fg="white", font=("Helvetica", 14, "bold")).pack()

    tk.Button(root, text="Voltar", command=voltar_menu, bg="#f44336", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)


def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()


def voltar_menu():
    limpar_tela()
    titulo = tk.Label(root, text="🏀 Campeonato de Basquete 🏀", font=("Helvetica", 20, "bold"), bg="#1e3c72", fg="white")
    titulo.pack(pady=20)

    botoes = [
        ("📝 Cadastrar Time", cadastrar_time),
        ("🏟️  Cadastrar Partida", cadastrar_partida),
        ("📊 Tabela de Pontuação", mostrar_tabela),
        ("🏆 Time Vitorioso", mostrar_time_vitorioso),
        ("❌ Sair", root.quit)
    ]

    for texto, comando in botoes:
        btn = tk.Button(
            root,
            text=texto,
            command=comando,
            font=("Helvetica", 12, "bold"),
            bg="#ff9800",
            fg="white",
            width=25
        )
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#ffc107"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ff9800"))


# Janela principal
root = tk.Tk()
root.title("Campeonato de Basquete")
root.geometry("400x500")
root.configure(bg="#1e3c72")

# Inicia o menu
voltar_menu()
root.mainloop()
