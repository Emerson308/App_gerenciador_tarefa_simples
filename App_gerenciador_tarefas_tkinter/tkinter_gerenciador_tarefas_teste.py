# from tkinter import *
import tkinter as tk
import json
import os
from tkinter import ttk

class App_gerenciador_tarefas():
    def __init__(self, root, dados):
        
        self.janela_principal = root
        self.janela_principal.title("Gerenciador de tarefas")
        self.janela_principal.configure(bg="gray")
        # self.janela_principal.geometry("500x500")

        self.dados = dados
        self.tarefas = self.dados["afazer"]
        self.tarefas_concluidas = self.dados["concluidas"]

        self.label_entrada_tarefas = tk.Label(self.janela_principal, text=" Insira uma nova tarefa:", font=("Arial",24), bg="black",anchor="w", fg="white", height= 2)
        self.label_entrada_tarefas.grid(row=0, column=0, columnspan=6, sticky="wnse",pady=0,padx=3)

        self.text_entrada_tarefas = tk.StringVar()
        self.entry_entrada_tarefas = tk.Entry(self.janela_principal, textvariable= self.text_entrada_tarefas, width=33, font=("Arial",17), bg="lightgray")
        self.entry_entrada_tarefas.bind('<Return>', self.on_enter)
        self.entry_entrada_tarefas.grid(row=1, column=0, sticky="W, E, N, S", padx=5, pady=5, columnspan=5)

        self.button_add_tarefa = tk.Button(self.janela_principal, text="+", command=self.b_add_tarefa, width=5, height=2, bg="lightgray")
        self.button_add_tarefa.grid(row=1, column=5, sticky="W, E, N, S", padx=5, pady=5)

        self.button_tarefas_afazer = tk.Button(self.janela_principal, text=f"A fazer({len(self.tarefas)})", height=2, command=self.b_tarefas_afazer, bg="black", fg="white")
        self.button_tarefas_afazer.grid(row=2, column=0, sticky="W, E, N, S", padx=5, pady=5)

        self.button_tarefas_concluidas = tk.Button(self.janela_principal, text=f"Concluídas({len(self.tarefas_concluidas)})", height=2, command=self.b_tarefas_concluidas, bg="lightgray")
        self.button_tarefas_concluidas.grid(row=2, column=1, sticky="W, E, N, S", padx=5, pady=5)

        self.frame_scrollbars = tk.Frame(root)
        self.frame_scrollbars.grid(row=3, column=0, sticky="nsew", pady=5, padx=5, columnspan=6)
        
        self.canvas = tk.Canvas(self.frame_scrollbars)
        self.frame_tarefas = tk.Frame(self.canvas)
        self.scroll_y = tk.Scrollbar(self.frame_scrollbars, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self.frame_scrollbars, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame_tarefas, anchor="nw")
        
        self.frame_tarefas.bind("<Configure>", self.on_frame_configure)

        self.atualizar_frame_tarefas()

    def on_enter(self, event):
        self.b_add_tarefa()
    
    def salvar_em_json(self):
        salvar_dados(self.dados, ARQUIVO_JSON)

    def on_frame_configure(self, event): 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def b_add_tarefa(self):
        self.button_tarefas_afazer.config(bg="black", fg="white")
        self.button_tarefas_concluidas.config(bg="lightgray", fg="black")
        tarefa = self.text_entrada_tarefas.get()
        if tarefa != "":
            self.tarefas.append(tarefa)
            self.atualizar_frame_tarefas()
            self.button_tarefas_afazer.config(text=f"A fazer({len(self.tarefas)})")
            self.button_tarefas_concluidas.config(text=f"Concluídas({len(self.tarefas_concluidas)})")
        self.text_entrada_tarefas.set('')
        self.salvar_em_json()

    
    def b_tarefas_concluidas(self):
        self.button_tarefas_afazer.config(fg="black", bg="lightgray")
        self.button_tarefas_concluidas.config(fg="white", bg="black")
        self.atualizar_frame_tarefas_concluidas()
        self.salvar_em_json()



    def b_tarefas_afazer(self):
        self.button_tarefas_afazer.config(fg="white", bg="black")
        self.button_tarefas_concluidas.config(fg="black", bg="lightgray")
        self.atualizar_frame_tarefas()
        self.salvar_em_json()

    

    def atualizar_frame_tarefas(self):
        for widget in self.frame_tarefas.winfo_children():
            widget.destroy()
        self.button_tarefas_afazer.config(text=f"A fazer({len(self.tarefas)})")
        self.button_tarefas_concluidas.config(text=f"Concluídas({len(self.tarefas_concluidas)})")
        row = 0
        for tarefa in self.tarefas:
            text_tarefa = tarefa
            if len(tarefa) >= 80:
                text_tarefa = f"{tarefa[0:80]}"+"..."
            var = tk.IntVar()
            checkbutton_tarefa = tk.Checkbutton(self.frame_tarefas, text=text_tarefa, anchor="w", variable=var, command=lambda var=var, task_text=tarefa: self.on_checkbutton_click(var, task_text),width=50, borderwidth=2, relief="solid", bg="lightgray")
            checkbutton_tarefa.grid(pady=3, row=row, column=0, sticky="wens")
            button_editar_tarefa = tk.Button(self.frame_tarefas, text="Editar", command= lambda tarefa=tarefa: self.b_delete(tarefa), anchor="center")
            button_editar_tarefa.grid(pady=3, sticky="enws", row=row, column=1)
            button_deletar_tarefa = tk.Button(self.frame_tarefas, text="Delete", command= lambda tarefa=tarefa: self.b_delete(tarefa), anchor="center")
            button_deletar_tarefa.grid(pady=3, sticky="enws", row=row, column=2)
            row += 1
    

    def atualizar_frame_tarefas_concluidas(self):
        for widget in self.frame_tarefas.winfo_children():
            widget.destroy()
        self.button_tarefas_afazer.config(text=f"A fazer({len(self.tarefas)})")
        self.button_tarefas_concluidas.config(text=f"Concluídas({len(self.tarefas_concluidas)})")
        row = 0
        for tarefa in self.tarefas_concluidas:
            text_tarefa = tarefa
            if len(tarefa) >= 80:
                text_tarefa = f"{tarefa[0:80]}"+"..."
            var = tk.IntVar(value=1)
            checkbutton_tarefa = tk.Checkbutton(self.frame_tarefas, text=text_tarefa, anchor="w", variable=var, command=lambda var=var, task_text=tarefa: self.move_to_afazer(var, task_text) if var.get()==0 else None,bg="gray", font=('TkDefaultFont', 10, 'overstrike'), width=44, borderwidth=2, relief="solid")
            checkbutton_tarefa.grid(pady=3, row=row, column=0, sticky="wens")
            button_editar_tarefa = tk.Button(self.frame_tarefas, text="Editar", command= lambda tarefa=tarefa: self.b_delete(tarefa), anchor="center")
            button_editar_tarefa.grid(pady=3, sticky="enws", row=row, column=1)
            button_deletar_tarefa = tk.Button(self.frame_tarefas, text="Delete", command= lambda tarefa=tarefa: self.b_delete_concluida(tarefa), anchor="center")
            button_deletar_tarefa.grid(pady=3, sticky="enws", row=row, column=2)
            row += 1



    def b_delete(self, tarefa):
        self.tarefas.remove(tarefa)
        self.atualizar_frame_tarefas()
        self.salvar_em_json()

    

    def b_delete_concluida(self, tarefa):
        self.tarefas_concluidas.remove(tarefa)
        self.atualizar_frame_tarefas_concluidas()
        self.salvar_em_json()

    
    def move_to_afazer(self, var, task_text):
        self.tarefas_concluidas.remove(task_text)
        self.tarefas.append(task_text)
        self.atualizar_frame_tarefas_concluidas()
        self.salvar_em_json()

    

    def on_checkbutton_click(self, var, task_text):
        for widget in self.frame_tarefas.winfo_children():
            text_tarefa = task_text
            if len(task_text) >= 80:
                text_tarefa = f"{task_text[0:80]}"+"..."

            if widget.cget('text') == text_tarefa:
                widget.config(bg="gray", font=('TkDefaultFont', 10, 'overstrike'), width=43)
        self.janela_principal.after(1200, lambda: self.check_and_move(var, task_text))
        
    def check_and_move(self, var, task_text):
        if var.get() == 1:  # Verifica se o Checkbutton ainda está ativado
            for widget in self.frame_tarefas.winfo_children():
                text_tarefa = task_text
                if len(task_text) >= 80:
                    text_tarefa = f"{task_text[0:80]}"+"..."

                if widget.cget('text') == text_tarefa:
                    self.janela_principal.after(0000, lambda widget=widget: self.move_checkbutton(widget, task_text))
        else:
            self.atualizar_frame_tarefas()
        
    def move_checkbutton(self, widget, task_text):
        widget.pack_forget()
        self.tarefas.remove(task_text)
        self.tarefas_concluidas.append(task_text)
        self.atualizar_frame_tarefas()
        self.salvar_em_json()



def carregar_dados(ARQUIVO_JSON):
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"afazer" : [], "concluidas" : []}


def salvar_dados(dados, ARQUIVO_JSON):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    ARQUIVO_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerenciador_tarefas.json")

    root = tk.Tk()
    app_gerenciador_tarefas = App_gerenciador_tarefas(root, carregar_dados(ARQUIVO_JSON))
    root.mainloop()