import tkinter as tk
from tkinter import ttk

# Função a ser chamada quando uma opção for selecionada
def on_option_select():
    selected_option = option_var.get()
    if selected_option == "Cloud":
        show_cloud_screen()

# Função para mostrar a tela de Cloud
def show_cloud_screen():
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    # Cria um novo rótulo para a tela de Cloud
    cloud_label = tk.Label(root, text="Bem-vindo à tela de Cloud", font=("Helvetica", 22), fg="black", bg="white")
    cloud_label.pack(pady=20)
    
    # Cria um botão para voltar à tela anterior
    back_button = tk.Button(root, text="Voltar", command=show_main_screen, bg="gray", fg="white")
    back_button.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

# Função para mostrar a tela principal
def show_main_screen():
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    # Cria um rótulo com fonte e cor personalizadas
    label = tk.Label(root, text="Escolha seu projeto", font=("Helvetica", 16), fg="black", bg="white")
    label.pack(pady=20)

    # Cria botões de rádio para as opções com o novo estilo
    options = ["Cloud", "Hardware"]
    for option in options:
        radio_button = ttk.Radiobutton(root, text=option, variable=option_var, value=option, command=on_option_select, style="TRadiobutton")
        radio_button.pack(anchor=tk.W, padx=20, pady=45)

# Cria a janela principal
root = tk.Tk()
root.title("Escolha seu projeto")
root.geometry("800x600")  # Define o tamanho da janela
root.configure(bg="white")  # Define a cor de fundo da janela

# Cria uma variável para armazenar a opção selecionada
option_var = tk.StringVar()

# Cria um estilo para os botões de rádio
style = ttk.Style()
style.configure("TRadiobutton", font=("Helvetica", 16), background="white", foreground="black")

# Mostra a tela principal ao iniciar a aplicação
show_main_screen()

# Executa a aplicação
root.mainloop()