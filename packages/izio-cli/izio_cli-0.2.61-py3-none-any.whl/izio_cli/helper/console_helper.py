import os
import subprocess

from rich.table import Table


def create_table(data_dict) -> Table:
    table = Table()

    # Adicionando cabeçalhos
    for header in data_dict.keys():
        table.add_column(header)

    # Encontrando o número de linhas (baseado no item mais longo)
    num_rows = max(len(values) for values in data_dict.values())

    # Adicionando linhas
    for i in range(num_rows):
        row = [
            f"{"[green]:heavy_check_mark:" if data_dict[key][i] == "Ok" else f"[red]{data_dict[key][i]}"}" if key == "status" else f"[bold blink dark_green]{data_dict[key][i]}" if i < len(
                data_dict[key]) else "" for key in data_dict
        ]
        table.add_row(*row)

    return table


def run_command(command, path=os.getcwd(), silent=False):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=path,
            shell=True,
        )
        if not silent:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error: {e.stderr}")


def update_gradle(root, bundleId, appName, project="loyalty2_0"):
    # remove strings file with os if exists
    # if os.path.exists(
    #         f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res{os.sep}values{os.sep}strings.xml"):
    #     os.remove(
    #         f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res{os.sep}values{os.sep}strings.xml")

    build_gradle_path = f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}build.gradle"

    with open(build_gradle_path, "r") as file:
        data = file.read()

        # Atualizar o applicationId e app_name diretamente na seção defaultConfig
        if 'applicationId' in data:
            actual_bundle_id = data.split('applicationId "')[1].split('"')[0]
            data = data.replace(f'applicationId "{actual_bundle_id}"', f'applicationId "{bundleId}"')

        if 'namespace' in data:
            actual_namespace = data.split('namespace "')[1].split('"')[0]
            data = data.replace(f'namespace "{actual_namespace}"', f'namespace "{bundleId}"')

        if 'resValue "string", "app_name"' in data:
            actual_app_name = data.split('resValue "string", "app_name", "')[1].split('"')[0]
            data = data.replace(f'resValue "string", "app_name", "{actual_app_name}"',
                                f'resValue "string", "app_name", "{appName.replace('"', "")}"')
        # Adicionar o novo manifestPlaceholder para o pacote dinamicamente
        if 'manifestPlaceholders' in data:
            # Extrair o bloco de manifestPlaceholders existente
            placeholders_start = data.index('manifestPlaceholders')
            placeholders_end = data.index("}", placeholders_start)
            existing_placeholders = data[placeholders_start:placeholders_end]


            # Verificar se o placeholder já existe, e substituir ou adicionar se necessário
            if 'appPackage' in existing_placeholders:
                # Substituir o valor existente
                data = data.replace(
                    re.search(r'appPackage: "(.*?)"', existing_placeholders).group(0),
                    f'appPackage: "{bundleId}"'
                )
            else:
                # Adicionar o novo placeholder ao final do bloco existente
                new_placeholder = f'appPackage: "{bundleId}"'
                updated_placeholders = existing_placeholders.rstrip()[:-1] + f", {new_placeholder} }}"
                data = data.replace(existing_placeholders, updated_placeholders)
        else:
            # Se não houver placeholders existentes, adicionar o bloco completo
            new_placeholder_block = f"manifestPlaceholders = [\n" \
                                    f"    HOST_DEEP_LINK: dartEnvironmentVariables.HOST_DEEP_LINK,\n" \
                                    f"    appPackage: \"{bundleId}\"\n" \
                                    f"]"
            # Adicionar a nova definição dentro do defaultConfig
            data = data.replace("defaultConfig {", f"defaultConfig {{\n    {new_placeholder_block}")

    with open(build_gradle_path, "w") as w_file:
        w_file.write(data)
