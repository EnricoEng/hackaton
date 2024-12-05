import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
import hashlib  # Usado para simular a verificação de hash de firmware BIOS
import identify_Resource_Provider

import time

# Função para ser chamada quando uma opção for selecionada
def on_option_select():
    selected_option = option_var.get()
    if selected_option == "Cloud":
        show_cloud_screen()
        show_firmware_screen()

# Função para mostrar a tela Cloud
def show_cloud_screen():
    # Limpar a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    # Criar um novo label para a tela Cloud com um estilo moderno
    cloud_label = tk.Label(root, text="Welcome to the Cloud Screen", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    cloud_label.pack(pady=10)
    
    # Botão de voltar
    back_button = ttk.Button(root, text="Back", style="TButton", command=show_main_screen)
    back_button.place(x=20, y=20)  # Posicionar o botão 10 pixels da esquerda e 10 pixels de cima


    # Criar o frame para os botões
    button_frame = tk.Frame(root, bg=root.cget("bg"))  # Define a cor de fundo para coincidir com a janela principal
    button_frame.pack(pady=10)

    # Botão para upload de arquivo
    global upload_button  # Torna o botão global para acesso em outras funções
    upload_button = tk.Button(button_frame, text="Upload File", command=upload_file, bg="#27ae60", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#2ecc71", activeforeground="white")
    upload_button.pack(side=tk.LEFT, padx=5)

    # Botão para chamar a API (desabilitado inicialmente)
    global api_button  # Torna o botão global
    api_button = tk.Button(button_frame, text="Generate Test Scenarios", command=call_api, state="disabled", bg="#3498db", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#2b6b96", activeforeground="white")
    api_button.pack(side=tk.LEFT, padx=5)

    # Botão para chamar a API Rag (desabilitado inicialmente)
    global api_rag_button  # Torna o botão global
    api_rag_button = tk.Button(button_frame, text="Generate Test Scenarios using RAG", command=call_api_rag, state="disabled", bg="#3498db", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#2b6b96", activeforeground="white")
    api_rag_button.pack(side=tk.LEFT, padx=5)

    # Aumentar o tamanho da caixa de texto para exibir os resultados dos botões
    global output_text
    output_text = tk.Text(root, height=30, width=150, bg="#2c3e50", fg="white", font=("Courier New", 12), relief="flat", bd=0, padx=10, pady=0)
    output_text.pack(pady=10, padx=20)

    # Botão para download do output
    download_button = tk.Button(root, text="Download Output", command=download_output, bg="#3498db", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#2980b9", activeforeground="white")
    download_button.pack(pady=10)

# Função para chamar a API Rag
def call_api_rag():
    for resource_type in resources:    
        url = "http://127.0.0.1:5000/generate_scenario_v2"
        headers = {"Content-Type": "application/json"}
        data = {"provider": provider, "resource": "Compute Engine"}
    
        response = requests.post(url, headers=headers, data=json.dumps(data))
    
        if response.status_code == 200:
            output_text.insert(tk.END, "API called successfully! (Response is not JSON)\n")
            output_text.insert(tk.END, f"{response.text}\n")
        else:
            output_text.insert(tk.END, f"Error calling the API: {response.status_code}\n")
            output_text.insert(tk.END, f"{response.text}\n")

# Função para mostrar a tela de Firmware
def show_firmware_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text="Firmware Screen", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    label.pack(pady=30)

    # Adicionar opções de verificação de integridade do BIOS
    integrity_button = tk.Button(root, text="EDK II C Coding Standards Specification", command=verify_firmware_integrity, bg="#f39c12", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#f1c40f")
    integrity_button.pack(pady=30, padx=20)

    # Botão de voltar
    back_button = ttk.Button(root, text="Back", style="TButton", command=show_main_screen)
    back_button.place(x=20, y=20)  # Posicionar o botão 10 pixels da esquerda e 10 pixels de cima

# Função para verificar a integridade do firmware BIOS
def verify_firmware_integrity():
    # Simulação de verificação de hash (usando um hash pré-definido para comparação)
    file_path = filedialog.askopenfilename(title="Select BIOS Firmware File")
    if file_path:
        predefined_hash = "d2d2d2f4e5a5646f2d2e1e6f59a8be77"  # Exemplo de hash
        file_hash = calculate_file_hash(file_path)
        output_text.insert(tk.END, f"Verifying integrity of: {file_path}\n")
        if file_hash == predefined_hash:
            output_text.insert(tk.END, "Firmware integrity verified successfully! (Hash matches)\n")
        else:
            output_text.insert(tk.END, "Integrity check failed. (Hash does not match)\n")

# Função para calcular o hash de um arquivo
def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Função para mostrar a tela principal
def show_main_screen():
    # Limpar a tela atual
    for widget in root.winfo_children():
        widget.destroy()

    # Criar um label com estilo moderno
    label = tk.Label(root, text="Choose Your Project", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    label.pack(pady=30)

    # Definir o estilo para os botões
    style = ttk.Style()
    style.configure("TButton",
                    font=("Arial", 14, "bold"),
                    foreground="#fff",
                    background="#3498db",
                    relief="flat",
                    padding=10)
    style.map("TButton",
              background=[('active', '#2980b9'), ('pressed', '#1f4e79')])  # Efeito ao passar o mouse

    # Criar botões de seleção com o novo estilo
    options = ["Cloud", "Firmware"]
    for option in options:
        button = ttk.Button(root, text=option, style="TButton", command=lambda opt=option: on_option_select(opt))
        button.pack(pady=15, padx=10)

# Função chamada quando um botão é selecionado
def on_option_select(option):
    if option == "Cloud":
        show_cloud_screen()  # Exibe a tela "Cloud"
    elif option == "Firmware":
        show_firmware_screen()  # Exibe a tela "Firmware"

# Função para upload de arquivo
def upload_file():
    global provider
    global resources

    file_path = filedialog.askopenfilename()
    if file_path:
        output_text.insert(tk.END, f"Selected file: {file_path}\n")

        terraform_content = identify_Resource_Provider.readTerraformFile(file_path)
        resources, provider = identify_Resource_Provider.identify_resources_and_providers(terraform_content) 
        
        output_text.insert(tk.END, "Resources:\n")
        for resource_type, resource_name in resources:
            output_text.insert(tk.END, f"Resource Type: {resource_type}, Resource Name: {resource_name}\n")

        output_text.insert(tk.END, f"Provider: {provider}\n")

                # Muda a cor do botão para cinza após a seleção do arquivo
        upload_button.config(bg="gray", activebackground="gray")

        # Habilita os botões "Generate" após a seleção do arquivo
        api_button.config(state="normal")
        api_rag_button.config(state="normal")

# Função para chamar a API
def call_api():
    for resource_type in resources:    
        url = "http://127.0.0.1:5000/generate_scenario"
        headers = {"Content-Type": "application/json"}
        data = {"provider": provider, "resource": resource_type}
    
        response = requests.post(url, headers=headers, data=json.dumps(data))
    
        if response.status_code == 200:
            output_text.insert(tk.END, "API called successfully! (Response is not JSON)\n")
            output_text.insert(tk.END, f"{response.text}\n")
        else:
            output_text.insert(tk.END, f"Error calling the API: {response.status_code}\n")
            output_text.insert(tk.END, f"{response.text}\n")

# Função para download do conteúdo da Text widget
def download_output():
    # Obter o conteúdo da Text widget
    output_content = output_text.get(1.0, tk.END)

    # Perguntar onde salvar o arquivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_content)
        output_text.insert(tk.END, f"Output saved to {file_path}\n")

# Criar a janela principal
root = tk.Tk()
root.title("The Wall CyberSec Solutions")
root.geometry("1290x800")  # Definir tamanho inicial da janela
root.configure(bg="#ecf0f1")  # Cor de fundo moderna e clara

# Tornar a janela responsiva configurando os pesos das linhas e colunas
root.grid_rowconfigure(0, weight=1, minsize=50)  # A linha 0 expande, com tamanho mínimo
root.grid_rowconfigure(1, weight=1, minsize=50)  # A linha 1 expande
root.grid_columnconfigure(0, weight=1, minsize=200)  # A coluna 0 expande, com tamanho mínimo

# Criar a variável para armazenar a opção selecionada
option_var = tk.StringVar()

# Estilo para os botões de rádio
style = ttk.Style()
style.configure("TRadiobutton", font=("Arial", 16), background="#ecf0f1", foreground="#2c3e50", padding=10)

# Exibir a tela principal ao iniciar o app
show_main_screen()

# Rodar o aplicativo
root.mainloop()
