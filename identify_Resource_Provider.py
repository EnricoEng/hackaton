import re



def identify_resources_and_providers(terraform_content):
    # Regular expression to find resource blocks
    resource_pattern = r'resource\s+"(\w+)"\s+"(\w+)"'
    resources = re.findall(resource_pattern, terraform_content)
    
    # Regular expression to find provider blocks
    #provider_pattern = r'provider\s+"(\w+)"'
    #providers = re.findall(provider_pattern, terraform_content)

     # Verificar se o resource começa com "google" e atribuir "GCP" ao provider
    for resource_type, _ in resources:
        if resource_type.startswith("google"):
            provider=("GCP")
            #print(f"provider: {provider}")
        elif resource_type.startswith("azure"):
            provider=("Azure")
        
        elif resource_type.startswith("aws"):
            provider=("AWS")

    
    return resources, provider

# Read the content of the terraform file
def readTerraformFile(arquivo):
    with open(arquivo, 'r') as file:
        terraform_content = file.read()
        return terraform_content

# Identify resources and provider
#resources, provider = identify_resources_and_providers(terraform_content) 

# Print the identified resources
def printResources():
    print("Resources:")
    for resource_type, resource_name in resources:
        print(f"Resource Type: {resource_type}, Resource Name: {resource_name}")

# Print the identified provider
def printProviders(): 
    print("\nProviders:")
    print(f"Provider: {provider}")
