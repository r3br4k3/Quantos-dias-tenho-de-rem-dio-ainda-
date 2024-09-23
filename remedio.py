import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import xml.etree.ElementTree as ET
import os

class MedicamentoApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Medicamentos")
        master.geometry("600x400")
        self.load_medicamentos()

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        # Frame para adicionar medicamentos
        frame_adicionar = ttk.Frame(master, padding="10")
        frame_adicionar.grid(row=0, column=0, sticky="ew")

        # Frame para cálculo de duração
        frame_calcular = ttk.Frame(master, padding="10")
        frame_calcular.grid(row=1, column=0, sticky="ew")

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        frame_adicionar.columnconfigure(1, weight=1)
        frame_calcular.columnconfigure(1, weight=1)

        # Widgets para adicionar medicamentos
        ttk.Label(frame_adicionar, text="Nome do Medicamento:").grid(row=0, column=0, sticky="w")
        self.entry_nome = ttk.Entry(frame_adicionar)
        self.entry_nome.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame_adicionar, text="Comprimidos por Cartela:").grid(row=1, column=0, sticky="w")
        self.entry_comprimidos_cartela = ttk.Entry(frame_adicionar)
        self.entry_comprimidos_cartela.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame_adicionar, text="Cartelas por Caixa:").grid(row=2, column=0, sticky="w")
        self.entry_cartelas_caixa = ttk.Entry(frame_adicionar)
        self.entry_cartelas_caixa.grid(row=2, column=1, sticky="ew")

        ttk.Button(frame_adicionar, text="Salvar Medicamento", command=self.salvar_medicamento).grid(row=3, columnspan=2, sticky="ew")

        # Widgets para calcular duração do medicamento
        ttk.Label(frame_calcular, text="Selecione um Medicamento:").grid(row=0, column=0, sticky="w")
        self.combobox_medicamentos = ttk.Combobox(frame_calcular, values=list(self.medicamentos.keys()), state='readonly')
        self.combobox_medicamentos.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame_calcular, text="Comprimidos por dia:").grid(row=1, column=0, sticky="w")
        self.entry_dose_diaria = ttk.Entry(frame_calcular)
        self.entry_dose_diaria.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame_calcular, text="Número de Caixas:").grid(row=2, column=0, sticky="w")
        self.entry_quantidade_caixas = ttk.Entry(frame_calcular)
        self.entry_quantidade_caixas.grid(row=2, column=1, sticky="ew")

        ttk.Label(frame_calcular, text="Cartelas Avulsas:").grid(row=3, column=0, sticky="w")
        self.entry_cartelas_avulsas = ttk.Entry(frame_calcular)
        self.entry_cartelas_avulsas.grid(row=3, column=1, sticky="ew")

        ttk.Label(frame_calcular, text="Comprimidos Avulsos:").grid(row=4, column=0, sticky="w")
        self.entry_comprimidos_avulsos = ttk.Entry(frame_calcular)
        self.entry_comprimidos_avulsos.grid(row=4, column=1, sticky="ew")

        ttk.Button(frame_calcular, text="Calcular Dias de Medicamento", command=self.calcular_dias).grid(row=5, columnspan=2, sticky="ew")

    def salvar_medicamento(self):
        nome = self.entry_nome.get()
        comprimidos_cartela = int(self.entry_comprimidos_cartela.get())
        cartelas_caixa = int(self.entry_cartelas_caixa.get())

        self.medicamentos[nome] = {
            "comprimidos_cartela": comprimidos_cartela,
            "cartelas_caixa": cartelas_caixa
        }

        self.update_xml()
        messagebox.showinfo("Salvo", f"Medicamento '{nome}' salvo com sucesso!")
        self.combobox_medicamentos['values'] = list(self.medicamentos.keys())
        self.limpar_campos()

    def calcular_dias(self):
        medicamento = self.combobox_medicamentos.get()
        if not medicamento:
            messagebox.showerror("Erro", "Selecione um medicamento primeiro!")
            return

        dados_medicamento = self.medicamentos[medicamento]
        dose_diaria = int(self.entry_dose_diaria.get())
        qtd_caixas = int(self.entry_quantidade_caixas.get())
        cartelas_avulsas = int(self.entry_cartelas_avulsas.get())
        comprimidos_avulsos = int(self.entry_comprimidos_avulsos.get())

        total_comprimidos = (
            qtd_caixas * dados_medicamento["cartelas_caixa"] * dados_medicamento["comprimidos_cartela"] +
            cartelas_avulsas * dados_medicamento["comprimidos_cartela"] +
            comprimidos_avulsos
        )

        dias_de_tratamento = total_comprimidos // dose_diaria
        messagebox.showinfo("Duração", f"Você tem medicamento para {dias_de_tratamento} dias.")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_comprimidos_cartela.delete(0, tk.END)
        self.entry_cartelas_caixa.delete(0, tk.END)

    def update_xml(self):
        root = ET.Element("medicamentos")
        for nome, info in self.medicamentos.items():
            med_elem = ET.SubElement(root, "medicamento", nome=nome)
            ET.SubElement(med_elem, "comprimidos_cartela").text = str(info["comprimidos_cartela"])
            ET.SubElement(med_elem, "cartelas_caixa").text = str(info["cartelas_caixa"])
        tree = ET.ElementTree(root)
        tree.write("medicamentos.xml")

    def load_medicamentos(self):
        self.medicamentos = {}
        if os.path.exists("medicamentos.xml"):
            tree = ET.parse("medicamentos.xml")
            root = tree.getroot()
            for med_elem in root.findall("medicamento"):
                nome = med_elem.get("nome")
                comprimidos_cartela = int(med_elem.find("comprimidos_cartela").text)
                cartelas_caixa = int(med_elem.find("cartelas_caixa").text)
                self.medicamentos[nome] = {
                    "comprimidos_cartela": comprimidos_cartela,
                    "cartelas_caixa": cartelas_caixa
                }

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicamentoApp(root)
    root.mainloop()
