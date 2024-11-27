import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import requests

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
    



    # Cria um botão para fazer upload de arquivo
    upload_button = tk.Button(root, text="Upload de Arquivo", command=upload_file, bg="gray", fg="white")
    upload_button.pack(pady=20, padx=20)
   
    
    # Cria um botão para chamar uma API
    api_button = tk.Button(root, text="Chamar API", command=call_api, bg="gray", fg="white")
    api_button.pack(pady=20)
    

    # Cria uma caixa de texto para mostrar os outputs dos botões
    global output_text
    output_text = tk.Text(root, height=10, width=40, bg="blue", fg="white")
    output_text.pack(pady=10)


# Função para mostrar a tela principal
def show_main_screen():
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    # Cria um rótulo com fonte e cor personalizadas
    label = tk.Label(root, text="Escolha seu projeto", font=("Helvetica", 22), fg="black", bg="white")
    label.pack(pady=20)

    # Cria botões de rádio para as opções com o novo estilo
    options = ["Cloud", "Hardware"]
    for option in options:
        radio_button = ttk.Radiobutton(root, text=option, variable=option_var, value=option, command=on_option_select, style="TRadiobutton")
        radio_button.pack(anchor=tk.W, padx=20, pady=45)



    # Função para fazer upload de arquivo
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        #print(f"Arquivo selecionado: {file_path}")
        output_text.insert(tk.END, f"Arquivo selecionado: {file_path}\n")

# Função para chamar uma API
def call_api():
    response = requests.get("https://api.exemplo.com/endpoint")
    if response.status_code == 200:
        #print("API chamada com sucesso!")
        #print(response.json())
        output_text.insert(tk.END, "API chamada com sucesso!\n")
        output_text.insert(tk.END, f"{response.json()}\n")
    else:
        output_text.insert(tk.END, "Erro ao chamar a API\n")
        #print("Erro ao chamar a API")



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