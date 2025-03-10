import os

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.readlines()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def reformat_damage_blocks(lines):
    reformatted_lines = []
    for line in lines:
        if line.strip().startswith('Damage[DT') and line.strip().endswith('= {'):
            parts = line.split('=')
            reformatted_lines.append(parts[0].strip() + ' =\n')
            reformatted_lines.append('{\n')
        else:
            reformatted_lines.append(line)
    return reformatted_lines

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Solicitar ao usuário para selecionar a pasta de origem
source_directory = input("Digite o caminho da pasta de origem: ")

# Listar arquivos no diretório de origem
source_files = list_files(source_directory)

print("Arquivos disponíveis na pasta de origem:")
for i, file in enumerate(source_files):
    print(f"{i + 1}. {file}")

# Processar cada arquivo na pasta de origem
for source_file in source_files:
    source_file_path = os.path.join(source_directory, source_file)
    
    # Ler conteúdo do arquivo de origem
    try:
        source_lines = read_file(source_file_path)
        
        # Reformatar os blocos de dano
        reformatted_content = reformat_damage_blocks(source_lines)
        
        # Escrever o conteúdo reformatado no arquivo de origem
        write_file(source_file_path, reformatted_content)
        
        print(f"Arquivo {source_file} reformado com sucesso!")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except UnicodeDecodeError as e:
        print(f"Erro de decodificação: {e}")
