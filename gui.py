import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
import hashlib  # Usado para simular a verificação de hash de arquivo de BIOS
import identify_Resource_Provider

# Função a ser chamada quando uma opção for selecionada
def on_option_select():
    selected_option = option_var.get()
    if selected_option == "Cloud":
        show_cloud_screen()
    elif selected_option == "Hardware":
        show_hardware_screen()

# Função para mostrar a tela de Cloud
def show_cloud_screen():
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    # Cria um novo rótulo para a tela de Cloud com um estilo mais moderno
    cloud_label = tk.Label(root, text="Bem-vindo à tela de Cloud", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    cloud_label.pack(pady=30)
    
    # Cria um botão para voltar à tela anterior com um estilo diferenciado
    back_button = tk.Button(root, text="Voltar", command=show_main_screen, bg="#2980b9", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#3498db")
    back_button.pack(side=tk.LEFT, anchor=tk.SW, padx=20, pady=20)

    # Cria um botão para fazer upload de arquivo com estilo melhorado
    upload_button = tk.Button(root, text="Upload de Arquivo", command=upload_file, bg="#27ae60", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#2ecc71")
    upload_button.pack(pady=30, padx=20) 
    
    # Cria um botão para chamar uma API com estilo diferenciado
    api_button = tk.Button(root, text="Chamar API", command=call_api, bg="#e74c3c", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#c0392b")
    api_button.pack(pady=30)
    
    # Aumenta o tamanho da caixa de texto para mostrar os outputs dos botões
    global output_text
    output_text = tk.Text(root, height=20, width=80, bg="#2c3e50", fg="white", font=("Courier New", 12), relief="flat", bd=0, padx=10, pady=10)
    output_text.pack(pady=10, padx=20)

# Função para mostrar a tela de "Hardware"
def show_hardware_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text="Tela de Hardware", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    label.pack(pady=30)

    # Adiciona opções de verificação de integridade de BIOS
    integrity_button = tk.Button(root, text="Verificar Integridade do Firmware (BIOS)", command=verify_firmware_integrity, bg="#f39c12", fg="white", font=("Arial", 14, "bold"), relief="flat", bd=0, padx=15, pady=8, activebackground="#f1c40f")
    integrity_button.pack(pady=30, padx=20)

    # Botão para voltar
    back_button = ttk.Button(root, text="Voltar", style="TButton", command=show_main_screen)
    back_button.pack(pady=20)

# Função para simular a verificação de integridade de BIOS
def verify_firmware_integrity():
    # Abrir um arquivo para simular a verificação de hash
    file_path = filedialog.askopenfilename(title="Selecione o arquivo de firmware BIOS")
    if file_path:
        # Simulando a verificação de hash (usaremos um hash pré-definido para comparar)
        predefined_hash = "d2d2d2f4e5a5646f2d2e1e6f59a8be77"  # Exemplo de hash fictício
        
        # Calcular o hash do arquivo selecionado
        file_hash = calculate_file_hash(file_path)

        output_text.insert(tk.END, f"Verificando integridade de: {file_path}\n")
        if file_hash == predefined_hash:
            output_text.insert(tk.END, "A integridade do firmware foi verificada com sucesso! (Hash corresponde)\n")
        else:
            output_text.insert(tk.END, "Falha na verificação de integridade. (Hash não corresponde)\n")

# Função para calcular o hash de um arquivo
def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Função para mostrar a tela principal
def show_main_screen():
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()

    # Cria um rótulo com um estilo mais moderno
    label = tk.Label(root, text="Escolha seu projeto", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#ecf0f1")
    label.pack(pady=30)

    # Define o estilo para os botões
    style = ttk.Style()
    style.configure("TButton",
                    font=("Arial", 14, "bold"),
                    foreground="#fff",
                    background="#3498db",
                    relief="flat",
                    padding=10)
    style.map("TButton",
              background=[('active', '#2980b9'), ('pressed', '#1f4e79')])  # Efeito ao passar o mouse

    # Cria os botões de seleção com o novo estilo
    options = ["Cloud", "Hardware"]
    for option in options:
        button = ttk.Button(root, text=option, style="TButton", command=lambda opt=option: on_option_select(opt))
        button.pack(pady=15, padx=10)

# Função que será chamada quando um botão for selecionado
def on_option_select(option):
    if option == "Cloud":
        show_cloud_screen()  # Exibe a tela de "Cloud"
    elif option == "Hardware":
        show_hardware_screen()  # Exibe a tela de "Hardware"

Provider = ""
resourceType = ""

# Função para fazer upload de arquivo
def upload_file():
    global Provider  # Use the global variable 'Provider'

    file_path = filedialog.askopenfilename()
    if file_path:
        output_text.insert(tk.END, f"Arquivo selecionado: {file_path}\n")

        terraform_content = identify_Resource_Provider.readTerraformFile(file_path)
        resources, provider = identify_Resource_Provider.identify_resources_and_providers(terraform_content) 
        
        output_text.insert(tk.END, "Resources:\n")
        for resource_type, resource_name in resources:
            output_text.insert(tk.END, f"Resource Type: {resource_type}, Resource Name: {resource_name}\n")
            resourceType = resource_type

        output_text.insert(tk.END, f"Provider: {provider}\n")
        Provider = provider

# Função para chamar uma API
def call_api():
    url = "http://127.0.0.1:5000/generate_scenario"
    headers = {"Content-Type": "application/json"}
    data = {"provider": Provider, "service": "S3 Bucket"}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    
    if response.status_code == 200:
        output_text.insert(tk.END, "API chamada com sucesso!\n")
        output_text.insert(tk.END, f"{response.text}\n")
    else:
        output_text.insert(tk.END, f"Erro ao chamar a API: {response.status_code}\n")
        output_text.insert(tk.END, f"{response.text}\n")

# Cria a janela principal
root = tk.Tk()
root.title("The Wall CyberSec Solutions")
root.geometry("1290x800")  # Define o tamanho inicial da janela
root.configure(bg="#ecf0f1")  # Cor de fundo suave e moderna

# Tornar a janela responsiva configurando o peso das linhas e colunas
root.grid_rowconfigure(0, weight=1, minsize=50)  # A linha 0 vai se expandir, com um tamanho mínimo
root.grid_rowconfigure(1, weight=1, minsize=50)  # A linha 1 vai se expandir
root.grid_columnconfigure(0, weight=1, minsize=200)  # A coluna 0 vai se expandir, com um tamanho mínimo

# Cria uma variável para armazenar a opção selecionada
option_var = tk.StringVar()

# Estilo para botões de rádio
style = ttk.Style()
style.configure("TRadiobutton", font=("Arial", 16), background="#ecf0f1", foreground="#2c3e50", padding=10)

# Mostra a tela principal ao iniciar a aplicação
show_main_screen()

# Executa a aplicação
root.mainloop()
