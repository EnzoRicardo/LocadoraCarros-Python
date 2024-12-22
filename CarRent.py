import customtkinter as ctk
from tkinter import messagebox
import json


ctk.set_appearance_mode("dark")


carros_cadastrados = []
ArquivoDados = "dadosCarro.json"


data = {
    "Carros": [],
    "Alugúeis": []
}

def carregarDados():
    global data
    try:
        with open(ArquivoDados, "r") as arquivo:
            data = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"Carros": [], "Alugúeis": []}
        salvarDados()

def salvarDados():
    with open(ArquivoDados, "w") as arquivo:
        json.dump(data, arquivo, indent=4)

def telaPrincipal():
    root = ctk.CTk()
    root.title("Locar Carros Python")
    root.geometry("400x400")

    title = ctk.CTkLabel(root, text="Aluguel de Carros", font=("Arial", 20))
    title.pack(pady=20)

    btn_gerenciar = ctk.CTkButton(root, text="Gerenciar Carros", width=200, command=gerenciar_carros)
    btn_disponibilidade = ctk.CTkButton(root, text="Checar Disponibilidade", width=200, command=consultar_disponibilidade)
    btn_registrar = ctk.CTkButton(root, text="Registrar Aluguel", width=200, command=registrar_aluguel)
    btn_devolucao = ctk.CTkButton(root, text="Registrar Devolução", width=200, command=devolucao_carro)

    btn_gerenciar.pack(pady=10)
    btn_disponibilidade.pack(pady=10)
    btn_registrar.pack(pady=10)
    btn_devolucao.pack(pady=10)

    root.mainloop()

def gerenciar_carros():
    window = ctk.CTkToplevel()
    window.title("Gerenciamento de Carros")
    window.geometry("400x300")

    ctk.CTkLabel(window, text="Modelo:").grid(row=0, column=0, pady=5, padx=5)
    ctk.CTkLabel(window, text="Marca:").grid(row=1, column=0, pady=5, padx=5)
    ctk.CTkLabel(window, text="Ano:").grid(row=2, column=0, pady=5, padx=5)
    ctk.CTkLabel(window, text="Preço por Dia:").grid(row=3, column=0, pady=5, padx=5)

    global modelo_entry, marca_entry, ano_carro_entry, preco_carro_entry
    modelo_entry = ctk.CTkEntry(window, placeholder_text="Modelo")
    marca_entry = ctk.CTkEntry(window, placeholder_text="Marca")
    ano_carro_entry = ctk.CTkEntry(window, placeholder_text="Ano")
    preco_carro_entry = ctk.CTkEntry(window, placeholder_text="Preço por Dia")

    modelo_entry.grid(row=0, column=1, pady=5, padx=5)
    marca_entry.grid(row=1, column=1, pady=5, padx=5)
    ano_carro_entry.grid(row=2, column=1, pady=5, padx=5)
    preco_carro_entry.grid(row=3, column=1, pady=5, padx=5)

    btn_salvar = ctk.CTkButton(window, text="Salvar", command=salvar_carro)
    btn_salvar.grid(row=4, column=1, pady=20)

def salvar_carro():
    modelo = modelo_entry.get()
    marca = marca_entry.get()
    ano = ano_carro_entry.get()
    preco = preco_carro_entry.get()

    if not modelo or not marca or not ano or not preco:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return
    if not ano.isdigit() or not preco.replace('.', '', 1).isdigit():
        messagebox.showerror("Erro", "Ano e preço devem ser numéricos!")
        return

    carro = {"Modelo": modelo, "Marca": marca, "Ano": int(ano), "Preço": float(preco), "Disponível": True}
    data["Carros"].append(carro)
    salvarDados()  
    carros_cadastrados.append(carro)

    messagebox.showinfo("Info", "Carro salvo com sucesso!")

    modelo_entry.delete(0, "end")
    marca_entry.delete(0, "end")
    ano_carro_entry.delete(0, "end")
    preco_carro_entry.delete(0, "end")

def consultar_disponibilidade():
    window = ctk.CTkToplevel()
    window.title("Consultar Disponibilidade")
    window.geometry("400x300")

    ctk.CTkLabel(window, text="Carros Disponíveis", font=("Arial", 16)).pack(pady=10)

    if not data["Carros"]:
        ctk.CTkLabel(window, text="Nenhum carro disponível no momento.").pack(pady=10)
        return

    for carro in data["Carros"]:
        if carro.get("Disponível", True):
            texto = f"{carro['Modelo']} - {carro['Marca']} - {carro['Ano']} - R${carro['Preço']:.2f}"
            ctk.CTkLabel(window, text=texto).pack(pady=2)

def registrar_aluguel():
    window = ctk.CTkToplevel()
    window.title("Registrar Aluguel")
    window.geometry("500x400")
    ctk.CTkLabel(window, text="Registrar Aluguel", font=("Arial", 16)).pack(pady=10)

    if not carros_cadastrados:
        ctk.CTkLabel(window, text="Nenhum carro disponível para alugar no momento :/").pack(pady=10)
        return

    ctk.CTkLabel(window, text="Selecione o carro:").pack(pady=5)
    carrosOpcoes = [f"{carro['Modelo']} - {carro['Marca']} - {carro['Ano']}" for carro in carros_cadastrados]
    carroVar = ctk.StringVar()
    dropdownCarro = ctk.CTkComboBox(window, values=carrosOpcoes, variable=carroVar)
    dropdownCarro.pack(pady=5)

    ctk.CTkLabel(window, text="Nome completo:").pack(pady=5)
    campoCliente = ctk.CTkEntry(window, placeholder_text="Digite seu nome completo")
    campoCliente.pack(pady=5)

    ctk.CTkLabel(window, text="Dias com o carro:").pack(pady=5)
    campoDias = ctk.CTkEntry(window, placeholder_text="Digite quantos dias deseja")
    campoDias.pack(pady=5)

    def confirmarAluguel():
        carroSelecionado = carroVar.get()
        nomeCliente = campoCliente.get()
        diasAluguel = campoDias.get()

        if not carroSelecionado or not nomeCliente or not diasAluguel:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return
        
        if not diasAluguel.isdigit():
            messagebox.showerror("Erro", "O número de dias deve ser numérico!")
            return

        diasAluguel = int(diasAluguel)
        for carro in carros_cadastrados:
            if carroSelecionado.startswith(carro['Modelo']):
                carro['Disponível'] = False
                carro['Cliente'] = nomeCliente
                carro['Dias'] = diasAluguel
                salvarDados()
                messagebox.showinfo("Sucesso", f"Aluguel registrado para {nomeCliente}!")
                window.destroy()
                return

    ctk.CTkButton(window, text="Confirmar Aluguel", command=confirmarAluguel).pack(pady=10)

def devolucao_carro():
    window = ctk.CTkToplevel()
    window.title("Registrar Devolução")
    window.geometry("400x300")

    ctk.CTkLabel(window, text="Registrar Devolução").pack(pady=20)

    carrosAlugados = [carro for carro in carros_cadastrados if not carro.get("Disponível", True)]

    if not carrosAlugados:
        ctk.CTkLabel(window, text="Nenhum carro alugado no momento").pack(pady=10)
        return

    ctk.CTkLabel(window, text="Selecione o carro:").pack(pady=5)
    carrosOpcoes = [f"{carro['Modelo']} - {carro['Marca']} - {carro['Ano']} ({carro['Cliente']})" for carro in carrosAlugados]
    carroVar = ctk.StringVar()
    dropdownCarro = ctk.CTkComboBox(window, values=carrosOpcoes, variable=carroVar)
    dropdownCarro.pack(pady=5)

    def confirmarDevolucao():
        carroSelecionado = carroVar.get()

        if not carroSelecionado:
            messagebox.showerror("Erro", "Selecione um carro para devolver!")
            return

        for carro in carrosAlugados:
            if carroSelecionado.startswith(carro['Modelo']):
                carro['Disponível'] = True
                carro.pop("Cliente", None)
                carro.pop("Dias", None)
                salvarDados()
                messagebox.showinfo("Sucesso", f"Devolução registrada para o carro {carro['Modelo']}!")
                window.destroy()
                return

    ctk.CTkButton(window, text="Confirmar Devolução", command=confirmarDevolucao).pack(pady=10)


carregarDados()

if __name__ == "__main__":
    telaPrincipal()
