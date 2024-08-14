import requests
import csv
import pandas as pd

# url pra BH 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2024&nr_periodo=1&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2001&co_esfera=M&id_ente=3106200'
# codigo ibge de Belo Horizonte 3106200

cidades = pd.read_csv('~/hello/entes.csv')


# parametros da query pro rreo
an_exercicio = 2023 #ano do exercicio
#nr_periodo = 6 #bimestre do an_exercicio
co_tipo_demonstrativo = 'RREO' #RREO ou RREO Simplificado, mas simplificado é só pra municipios abaixo de 50k habitantes que fizerem a opção do simplificado
no_anexo = 'RREO-Anexo%2002' #RREO-Anexo x, com x indo de 1 a 14
co_esfera = 'M'#(M)unicipios, (E)stados e DF, (U)nião, (C)onsórcio

resultado = pd.read_csv('~/hello/tabela_resultados.csv')
baixar2023 = resultado.query('ano2023 == 0')

cidades = cidades.merge(baixar2023,how = 'inner',on='ente')[['cod_ibge','ente','capital','regiao','uf','populacao']].drop_duplicates()

# Criar um DataFrame para armazenar os resultados
resultados = pd.DataFrame(index=cidades['ente'], columns=["ano2023"])
resultados = resultados.fillna(0)  # Inicializar todas as células com 0

count = 0
for id_ente in cidades['cod_ibge']:
    count += 1
    nr_periodo = 5
    conseguiu = 0
    print(count)
    while conseguiu == 0 or nr_periodo > 0:
        url = f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio={an_exercicio}&nr_periodo={nr_periodo}&co_tipo_demonstrativo={co_tipo_demonstrativo}&no_anexo={no_anexo}&co_esfera={co_esfera}&id_ente={id_ente}"

        #A estrutura do RREO está definida conforme discriminação a seguir: 
        # Anexo 01 Balanço Orçamentário; 
        # Anexo 02 Demonstrativo da Execução das Despesas por Função/Subfunção; 
        # Anexo 03 Demonstrativo da Receita Corrente Líquida; 
        # Anexo 04 Demonstrativo das Receitas e Despesas Previdenciárias do RPPS; 
        # Anexo 06 Demonstrativo do Resultado Primário; 
        # Anexo 07 Demonstrativo dos Restos à Pagar por Poder e Órgão; 
        # Anexo 09 Demonstrativo das Receitas de Operações de Crédito e Despesas de Capital; 
        # Anexo 10 RPPS Demonstrativo da Projeção Atuarial do Regime Próprio de Previdência dos Servidores; 
        # Anexo 10.1 RPPS Demonstrativo da Projeção Atuarial do Regime Próprio de Previdência dos Servidores; 
        # Anexo 10.2 RGPS Demonstrativo da Projeção Atuarial do Regime Geral de Previdência Social; 
        # Anexo 11 Demonstrativo da Receita de Alienação de Ativos e Aplicação dos Recursos; 
        # Anexo 13 Demonstrativo das Parcerias Públicos-Privadas; Anexo 14 Demonstrativo Simplificado do Relatório Resumido da Execução Orçamentária .

        # Make a GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if 'items' key exists and it's not empty
            if 'items' in data and data['items']:
                # Extract field names from the first item
                field_names = list(data['items'][0].keys())
                nome_cidade = cidades.query(f'cod_ibge == {id_ente}')['ente'].values[0]
                nome_cidade_sem_espacos = nome_cidade.replace(" ", "_")
                # Define the path to the CSV file
                csv_file_path = f"RREO_anexo_2_{nome_cidade_sem_espacos}_bim{nr_periodo}_{ano}.csv"

                # Write data to CSV file
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)

                    # Write the header
                    writer.writeheader()

                    # Write all data rows
                    writer.writerows(data['items'])

                print("Data has been saved to", csv_file_path)
                resultados.loc[nome_cidade, an_exercicio] = 1
                conseguiu = 1
                
            else:
                nr_periodo -= 1
                # nome_cidade = cidades.query(f'cod_ibge == {id_ente}')['ente'].values[0]
                # print(f"No data found in the response. cidade = {nome_cidade} ano = {an_exercicio}")
        else:
            print("Error:", response.status_code)
resultados.to_csv('tabela_resultados2023.csv')