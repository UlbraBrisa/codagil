import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ContaAgil - Simulador Fator R e Comparador PJ x CLT")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.option_add("*Font", "Arial 12")

        # Estilo para abas
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        style.configure('TLabel', font=('Arial', 12))

        # Abas
        self.notebook = ttk.Notebook(root)

        self.tab_fator_r = ttk.Frame(self.notebook)
        self.tab_comparador = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_fator_r, text="Fator R")
        self.notebook.add(self.tab_comparador, text="CLT x PJ")
        self.notebook.pack(expand=1, fill="both")

        # Ativar o piscar da aba selecionada
        self.notebook.bind("<<NotebookTabChanged>>", self.atualizar_estilo_abas)

        self.criar_aba_fator_r()
        self.criar_aba_comparador()

    def atualizar_estilo_abas(self, event=None):
        tabs = self.notebook.tabs()
        for tab_id in tabs:
            tab_text = self.notebook.tab(tab_id, "text")
            if tab_id == self.notebook.select():
                self.notebook.tab(tab_id, padding=(10, 5, 10, 5))
                self.notebook.tk.call("ttk::style", "configure", f"TNotebook.Tab.selected.{tab_text}",
                                      "-background", "#007BFF",
                                      "-foreground", "white",
                                      "-font", "Arial 12 bold")
                self.notebook.tk.call("ttk::style", "map", f"TNotebook.Tab.selected.{tab_text}",
                                      "-background", [("selected", "#007BFF")],
                                      "-relief", [("pressed", "sunken")])
                self.notebook.tab(tab_id, style=f"TNotebook.Tab.selected.{tab_text}")
                self.piscar_aba(tab_id, tab_text)
            else:
                self.notebook.tab(tab_id, padding=(10, 5, 10, 5))
                self.notebook.tk.call("ttk::style", "configure", f"TNotebook.Tab.inactive.{tab_text}",
                                      "-background", "#d4edda",
                                      "-foreground", "black",
                                      "-font", "Arial 12")
                self.notebook.tab(tab_id, style=f"TNotebook.Tab.inactive.{tab_text}")

    def piscar_aba(self, tab_id, tab_name):
        current_style = self.notebook.tab(tab_id, "style")
        if "selected" in current_style:
            new_bg = "#007BFF" if "on" in current_style else "#66b3ff"
            self.notebook.tk.call("ttk::style", "configure", f"TNotebook.Tab.selected.{tab_name}",
                                  "-background", new_bg)
        self.root.after(800, lambda: self.piscar_aba(tab_id, tab_name))

    def criar_aba_fator_r(self):
        frame = ttk.LabelFrame(self.tab_fator_r, text="Simulador de Fator R", padding=10)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Receita Bruta dos Últimos 12 Meses (R$)").pack(anchor="w")
        self.receita_bruta = ttk.Entry(frame, width=40)
        self.receita_bruta.pack(pady=5)

        ttk.Label(frame, text="Folha de Pagamento dos Últimos 12 Meses (R$)").pack(anchor="w")
        self.folha_pagamento = ttk.Entry(frame, width=40)
        self.folha_pagamento.pack(pady=5)

        ttk.Button(frame, text="Calcular Fator R", command=self.calcular_fator_r).pack(pady=10)

        self.resultado_fator_r = tk.Text(frame, height=8, wrap="word", state="disabled", bg="#f0f0f0")
        self.resultado_fator_r.pack(fill="x", pady=5)

    def calcular_fator_r(self):
        try:
            receita = float(self.receita_bruta.get())
            folha = float(self.folha_pagamento.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos.")
            return

        if receita <= 0 or folha <= 0:
            messagebox.showerror("Erro", "Valores devem ser maiores que zero.")
            return

        fator_r = (folha / receita) * 100
        percentual = round(fator_r, 2)
        enquadramento = "Anexo III" if fator_r >= 28 else "Anexo V"
        aliquota_atual = "15,5%" if fator_r >= 28 else "6%"
        economia = "Nenhuma economia" if fator_r >= 28 else "Redução de 9,5%"

        texto = (
            f"Fator R: {percentual}%\n"
            f"Enquadramento Tributário: {enquadramento}\n"
            f"Alíquota Aplicável: {aliquota_atual}\n"
            f"Economia Tributária: {economia}"
        )

        self.resultado_fator_r.config(state="normal")
        self.resultado_fator_r.delete(1.0, "end")
        self.resultado_fator_r.insert("end", texto)
        self.resultado_fator_r.config(state="disabled")

    def criar_aba_comparador(self):
        frame = ttk.LabelFrame(self.tab_comparador, text="Dados do Colaborador", padding=10)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Salário Mensal Bruto (CLT):").grid(row=0, column=0, sticky="w")
        self.salario_clt = ttk.Entry(frame, width=30)
        self.salario_clt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Vale-refeição/alimentação (mensal):").grid(row=1, column=0, sticky="w")
        self.vale_refeicao = ttk.Entry(frame, width=30)
        self.vale_refeicao.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Vale-transporte (mensal):").grid(row=2, column=0, sticky="w")
        self.vale_transporte = ttk.Entry(frame, width=30)
        self.vale_transporte.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Plano de saúde (mensal):").grid(row=3, column=0, sticky="w")
        self.plano_saude = ttk.Entry(frame, width=30)
        self.plano_saude.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Outros benefícios (adicional anual):").grid(row=4, column=0, sticky="w")
        self.outros_beneficios = ttk.Entry(frame, width=30)
        self.outros_beneficios.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Taxa de imposto para PJ (%):").grid(row=5, column=0, sticky="w")
        self.taxa_imposto_pj = ttk.Entry(frame, width=30)
        self.taxa_imposto_pj.insert(0, "16")
        self.taxa_imposto_pj.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Regime Tributário do PJ:").grid(row=6, column=0, sticky="w")
        self.regime_pj = ttk.Combobox(frame, values=["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"], width=28)
        self.regime_pj.set("Simples Nacional")
        self.regime_pj.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Custo com Contabilidade (mensal):").grid(row=7, column=0, sticky="w")
        self.custo_contabilidade = ttk.Entry(frame, width=30)
        self.custo_contabilidade.insert(0, "500")
        self.custo_contabilidade.grid(row=7, column=1, padx=5, pady=5)

        self.contribui_inss_pj_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Contribuir com INSS como PJ?", variable=self.contribui_inss_pj_var).grid(
            row=8, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Percentual de aumento sugerido para PJ (%):").grid(row=9, column=0, sticky="w")
        self.percentual_aumento_pj = ttk.Entry(frame, width=30)
        self.percentual_aumento_pj.insert(0, "30")
        self.percentual_aumento_pj.grid(row=9, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Calcular", command=self.calcular_cpl_clt).grid(row=10, columnspan=2, pady=10)

        self.resultado_text = tk.Text(self.tab_comparador, height=20, wrap="word", state="disabled", bg="#f0f0f0")
        self.resultado_text.pack(padx=10, pady=10, fill="both", expand=True)

    def calcular_cpl_clt(self):
        try:
            salario_clt_bruto = float(self.salario_clt.get())
        except ValueError:
            messagebox.showerror("Erro", "Salário CLT inválido.")
            return

        vale_refeicao = float(self.vale_refeicao.get() or 0)
        vale_transporte = float(self.vale_transporte.get() or 0)
        plano_saude = float(self.plano_saude.get() or 0)
        outros_beneficios = float(self.outros_beneficios.get() or 0)
        taxa_imposto_pj = float(self.taxa_imposto_pj.get() or 16) / 100
        regime_pj = self.regime_pj.get()
        custo_contabilidade = float(self.custo_contabilidade.get() or 500)
        contribui_inss_pj = self.contribui_inss_pj_var.get()
        percentual_aumento_pj = float(self.percentual_aumento_pj.get() or 30) / 100

        # Cálculo do INSS CLT
        if salario_clt_bruto <= 1302.00:
            inss_clt = salario_clt_bruto * 0.075
        elif salario_clt_bruto <= 2571.29:
            inss_clt = salario_clt_bruto * 0.09 - 19.53
        elif salario_clt_bruto <= 3856.94:
            inss_clt = salario_clt_bruto * 0.12 - 96.67
        elif salario_clt_bruto <= 7507.49:
            inss_clt = salario_clt_bruto * 0.14 - 174.08
        else:
            inss_clt = 7507.49 * 0.14 - 174.08

        # IRRF
        salario_base_irrf = salario_clt_bruto - inss_clt
        if salario_base_irrf <= 1903.98:
            irrf_clt = 0
        elif salario_base_irrf <= 2826.65:
            irrf_clt = salario_base_irrf * 0.075 - 142.80
        elif salario_base_irrf <= 3751.05:
            irrf_clt = salario_base_irrf * 0.15 - 354.80
        elif salario_base_irrf <= 4664.68:
            irrf_clt = salario_base_irrf * 0.225 - 636.13
        else:
            irrf_clt = salario_base_irrf * 0.275 - 869.36

        # Benefícios
        desconto_vale_transporte = vale_transporte * 0.06
        desconto_vale_refeicao = vale_refeicao * 0.20
        salario_liquido_clt = salario_clt_bruto - inss_clt - irrf_clt - desconto_vale_transporte - desconto_vale_refeicao
        total_beneficios_mensal = salario_liquido_clt + (outros_beneficios + vale_refeicao + vale_transporte + plano_saude) / 12

        # Cálculo PJ
        salario_pj_bruto = salario_clt_bruto * (1 + percentual_aumento_pj)
        impostos_pj = salario_pj_bruto * taxa_imposto_pj
        inss_pj = salario_pj_bruto * 0.11 if contribui_inss_pj else 0
        salario_liquido_pj = salario_pj_bruto - impostos_pj - inss_pj - custo_contabilidade

        resultado = (
            "=== Resultados ===\n\n"
            "--- CLT ---\n"
            f"Salário Bruto: R$ {salario_clt_bruto:.2f}\n"
            f"INSS: R$ {inss_clt:.2f}\n"
            f"IRRF: R$ {irrf_clt:.2f}\n"
            f"Vale Transporte: R$ {vale_transporte:.2f} (Desconto: R$ {desconto_vale_transporte:.2f})\n"
            f"Vale Refeição: R$ {vale_refeicao:.2f} (Desconto: R$ {desconto_vale_refeicao:.2f})\n"
            f"Plano de Saúde: R$ {plano_saude:.2f}\n"
            f"Outros Benefícios: R$ {outros_beneficios:.2f}\n"
            f"Salário Líquido Mensal (sem benefícios): R$ {salario_liquido_clt:.2f}\n"
            f"Total CLT + Benefícios: R$ {total_beneficios_mensal:.2f}\n\n"
            "--- PJ ---\n"
            f"Salário Bruto PJ ({percentual_aumento_pj*100:.0f}% maior): R$ {salario_pj_bruto:.2f}\n"
            f"Impostos PJ ({taxa_imposto_pj*100:.0f}%): R$ {impostos_pj:.2f}\n"
            f"{'INSS PJ: R$ ' + f'{inss_pj:.2f}' if contribui_inss_pj else ''}\n"
            f"Custo com Contabilidade: R$ {custo_contabilidade:.2f}\n"
            f"Salário Líquido PJ: R$ {salario_liquido_pj:.2f}\n\n"
            "--- Comparativo Final ---\n"
            f"Salário Líquido CLT + Benefícios: R$ {total_beneficios_mensal:.2f}\n"
            f"Salário Líquido PJ: R$ {salario_liquido_pj:.2f}\n\n"
        )

        vantagem = ""
        if total_beneficios_mensal > salario_liquido_pj:
            vantagem = "👉 A opção CLT é mais vantajosa neste cenário."
        elif salario_liquido_pj > total_beneficios_mensal:
            vantagem = "👉 A opção PJ é mais vantajosa neste cenário."
        else:
            vantagem = "👉 Ambos regimes são equivalentes neste cenário."

        resultado += f"{vantagem}"

        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, "end")
        self.resultado_text.insert("end", resultado)
        self.resultado_text.config(state="disabled")


# Executar app
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
