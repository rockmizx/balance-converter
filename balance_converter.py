import os
import re

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

def extract_all_damage_values(lines):
    damage_values = {}
    current_func = None
    inside_damage_block = False
    nested_braces = 0
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Damage[DT_'):
            current_func = stripped_line.split(' = ')[0]
            inside_damage_block = '{' in stripped_line or (i + 1 < len(lines) and '{' in lines[i + 1].strip())
            nested_braces = 1 if '{' in stripped_line else 0
        elif inside_damage_block:
            nested_braces += stripped_line.count('{')
            nested_braces -= stripped_line.count('}')
            if 'DAMAGETO_MONSTER' in stripped_line and nested_braces == 1:
                try:
                    value_str = re.search(r'DAMAGETO_MONSTER\s*=\s*(-?\d+\.?\d*)', stripped_line).group(1)
                    value = float(value_str)
                    damage_values[current_func] = value
                except (ValueError, AttributeError):
                    print(f"Valor inválido encontrado para {current_func}. Ignorando...")
            if nested_braces == 0:
                inside_damage_block = False
                current_func = None
    return damage_values

def update_all_damage_values(source_values, lines):
    current_func = None
    inside_damage_block = False
    nested_braces = 0
    changes_log = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Damage[DT_'):
            current_func = stripped_line.split(' = ')[0]
            inside_damage_block = '{' in stripped_line or (i + 1 < len(lines) and '{' in lines[i + 1].strip())
            nested_braces = 1 if '{' in stripped_line else 0
        elif inside_damage_block:
            nested_braces += stripped_line.count('{')
            nested_braces -= stripped_line.count('}')
            if 'DAMAGETO_MONSTER' in stripped_line and nested_braces == 1:
                base_func = current_func.replace('_DUN', '')
                old_value = re.search(r'DAMAGETO_MONSTER\s*=\s*(-?\d+\.?\d*)', stripped_line).group(1)
                if current_func in source_values:
                    lines[i] = re.sub(r'DAMAGETO_MONSTER\s*=\s*(-?\d+\.?\d*)', f'DAMAGETO_MONSTER = {source_values[current_func]}', lines[i])
                    new_value = source_values[current_func]
                    changes_log.append(f"{current_func}: {old_value} --> {new_value}")
                elif base_func in source_values:
                    lines[i] = re.sub(r'DAMAGETO_MONSTER\s*=\s*(-?\d+\.?\d*)', f'DAMAGETO_MONSTER = {source_values[base_func]}', lines[i])
                    new_value = source_values[base_func]
                    changes_log.append(f"{current_func}: {old_value} --> {new_value}")
            if nested_braces == 0:
                inside_damage_block = False
                current_func = None
    return lines, changes_log

def extract_all_attack_properties(lines):
    attack_properties = {}
    current_func = None
    inside_function_block = False
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Player_Action['):
            current_func = stripped_line.split(' = ')[0]
            inside_function_block = 'function' in stripped_line or (i + 1 < len(lines) and 'function' in lines[i + 1].strip())
        elif inside_function_block and 'SetAttackProperty' in stripped_line:
            try:
                params = re.search(r'SetAttackProperty\((.+?)\)', stripped_line).group(1)
                attack_properties[current_func] = params
            except (ValueError, AttributeError):
                print(f"Erro ao extrair propriedades de ataque para {current_func}. Ignorando...")
        elif inside_function_block and 'end' in stripped_line:
            inside_function_block = False
            current_func = None
    return attack_properties

def update_all_attack_properties(source_properties, lines):
    current_func = None
    inside_function_block = False
    changes_log = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Player_Action['):
            current_func = stripped_line.split(' = ')[0]
            inside_function_block = 'function' in stripped_line or (i + 1 < len(lines) and 'function' in lines[i + 1].strip())
        elif inside_function_block and 'SetAttackProperty' in stripped_line:
            if current_func in source_properties:
                old_value = re.search(r'SetAttackProperty\((.+?)\)', stripped_line).group(1)
                new_value = source_properties[current_func]
                lines[i] = re.sub(r'SetAttackProperty\((.+?)\)', f'SetAttackProperty({new_value})', lines[i])
                changes_log.append(f"{current_func}: {old_value} --> {new_value}")
        elif inside_function_block and 'end' in stripped_line:
            inside_function_block = False
            current_func = None
    return lines, changes_log

def extract_all_start_attack_properties(lines):
    start_attack_properties = {}
    current_func = None
    inside_function_block = False
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Player_Action['):
            current_func = stripped_line.split(' = ')[0]
            inside_function_block = 'function' in stripped_line or (i + 1 < len(lines) and 'function' in lines[i + 1].strip())
        elif inside_function_block and 'StartAttack' in stripped_line:
            try:
                params = re.search(r'StartAttack\((.+?)\)', stripped_line).group(1)
                start_attack_properties[current_func] = params
            except (ValueError, AttributeError):
                print(f"Erro ao extrair propriedades de ataque para {current_func}. Ignorando...")
        elif inside_function_block and 'end' in stripped_line:
            inside_function_block = False
            current_func = None
    return start_attack_properties

def update_all_start_attack_properties(source_properties, lines):
    current_func = None
    inside_function_block = False
    changes_log = []
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('Player_Action['):
            current_func = stripped_line.split(' = ')[0]
            inside_function_block = 'function' in stripped_line or (i + 1 < len(lines) and 'function' in lines[i + 1].strip())
        elif inside_function_block and 'StartAttack' in stripped_line:
            if current_func in source_properties:
                old_value = re.search(r'StartAttack\((.+?)\)', stripped_line).group(1)
                new_value = source_properties[current_func]
                lines[i] = re.sub(r'StartAttack\((.+?)\)', f'StartAttack({new_value})', lines[i])
                changes_log.append(f"{current_func}: {old_value} --> {new_value}")
        elif inside_function_block and 'end' in stripped_line:
            inside_function_block = False
            current_func = None
    return lines, changes_log

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def extract_all_functions(directory):
    all_damage_values = {}
    all_attack_properties = {}
    all_start_attack_properties = {}
    files = list_files(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        lines = read_file(file_path)
        all_damage_values.update(extract_all_damage_values(lines))
        all_attack_properties.update(extract_all_attack_properties(lines))
        all_start_attack_properties.update(extract_all_start_attack_properties(lines))
    return all_damage_values, all_attack_properties, all_start_attack_properties

# Solicitar as pastas de origem e destino
source_directory = input("Digite o caminho da pasta de origem: ")
destination_directory = input("Digite o caminho da pasta de destino: ")

# Extrair todas as funções das pastas de origem e destino
source_damage_values, source_attack_properties, source_start_attack_properties = extract_all_functions(source_directory)
destination_files = list_files(destination_directory)

# Processar cada arquivo de destino
for destination_file in destination_files:
    destination_file_path = os.path.join(destination_directory, destination_file)
    
    # Ler conteúdo do arquivo de destino
    try:
        destination_lines = read_file(destination_file_path)

        # Atualizar valores de DAMAGETO_MONSTER
        updated_destination_content, damage_changes_log = update_all_damage_values(source_damage_values, destination_lines)
        # Atualizar propriedades de ataque
        updated_destination_content, attack_changes_log = update_all_attack_properties(source_attack_properties, updated_destination_content)
        # Atualizar propriedades StartAttack
        updated_destination_content, start_attack_changes_log = update_all_start_attack_properties(source_start_attack_properties, updated_destination_content)

        # Escrever conteúdo atualizado de volta no arquivo de destino
        write_file(destination_file_path, updated_destination_content)
        print(f"Arquivo {destination_file} atualizado com sucesso!")

        # Imprimir logs de mudanças
        print("\nLog de mudanças de DAMAGETO_MONSTER:")
        for log in damage_changes_log:
            print(log)
        print("\nLog de mudanças das propriedades de ataque:")
        for log in attack_changes_log:
            print(log)
        print("\nLog de mudanças das propriedades StartAttack:")
        for log in start_attack_changes_log:
            print(log)

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except UnicodeDecodeError as e:
        print(f"Erro de decodificação: {e}")
