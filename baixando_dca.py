import time
import requests
import csv
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Definir função para baixar os dados
def baixar_dados(url, cidade, ano):
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated from method_whitelist to allowed_methods
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    while True:
        try:
            response = session.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    field_names = list(data['items'][0].keys())
                    nome_cidade = cidade.replace(" ", "_")
                    csv_file_path = f"DCA_anexo_2_{nome_cidade}_{ano}.csv"

                    with open(csv_file_path, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerows(data['items'])

                    print(f"Data has been saved to {csv_file_path} for cidade = {cidade}, ano = {ano}, bimestre = {bimestre}")
                    return True
                else:
                    print(f"No data found in the response. cidade = {cidade} bimestre = {bimestre}")
                    return False
            elif response.status_code == 429:
                print("Received status 429: Too Many Requests. Retrying after a delay...")
                time.sleep(5)  # Wait 5 seconds before retrying
                continue  # Retry the request
            else:
                print(f"Error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504, 429],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    while True:
        try:
            response = session.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    field_names = list(data['items'][0].keys())
                    nome_cidade = cidade.replace(" ", "_")
                    csv_file_path = f"RREO_anexo_2_{nome_cidade}_bim{bimestre}_{ano}.csv"

                    with open(csv_file_path, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerows(data['items'])

                    print(f"Data has been saved to {csv_file_path} for cidade = {cidade}, ano = {ano}, bimestre = {bimestre}")
                    return True
                else:
                    print(f"No data found in the response. cidade = {cidade} bimestre = {bimestre}")
            elif response.status_code == 429:
                print("Received status 429: Too Many Requests. Retrying after a delay...")
                time.sleep(5)  # Wait 5 seconds before retrying
                continue  # Retry the request
            else:
                print(f"Error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False


# Carregar as cidades e a tabela de resultados
cidades = pd.read_csv('~/hello/entes.csv')

# Parâmetros da query para o RREO
an_exercicio = (2016, 2017, 2018, 2019)
co_tipo_demonstrativo = 'Anexo%20I-AB' # Anexo%20I-AB
no_anexo = 'RREO-Anexo%2002'
co_esfera = 'M'

resultados = pd.read_csv('~/hello/tabela_resultados_massivo_gpt.csv')
resultados['ente'] = cidades['ente']
resultados = resultados.set_index('ente')
print(resultados.head(5))

# Loop para baixar os dados
for ano in an_exercicio:
    cidades_baixar = cidades
    for tipo in co_tipo_demonstrativo:
        print(tipo)
        baixar = resultados[resultados[f'ano{ano}'] == 0].index
        cidades_baixar = cidades[cidades['ente'].isin(baixar)]
        for idx, row in cidades_baixar.iterrows():
            id_ente = row['cod_ibge']
            cidade = row['ente']
            url = f'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio={ano}&no_anexo={no_anexo}&id_ente={id_ente}'
            if baixar_dados(url, cidade, ano):
                resultados.loc[resultados.index == cidade, f'ano{ano}'] = 1
                resultados.to_csv('~/hello/tabela_dca_massivo_gpt.csv', index=False)
            
resultados.to_csv('~/hello/tabela_dca_massivo_final_gpt.csv', index=False)
