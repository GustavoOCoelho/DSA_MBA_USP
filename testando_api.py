import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2023&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2002&co_esfera=M&id_ente=2603603'

# Create a session with retry strategy
session = requests.Session()
retry = Retry(
    total=5,
    read=5,
    connect=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504)
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

try:
    response = session.get(url, timeout=10)  # Set timeout to 10 seconds
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    data = response.json()
    print(data)
except requests.exceptions.SSLError as ssl_err:
    print(f"SSL error occurred: {ssl_err}")
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")