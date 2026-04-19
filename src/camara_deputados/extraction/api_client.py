import requests
import pandas as pd

import time
import requests
import pandas as pd


class CamaraAPIClient:

    BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

    def __init__(self, verbose=True):
        self.headers = {'accept': 'application/json'}
        self.verbose = verbose

    def get(self, endpoint: str) -> pd.DataFrame:
        url = f"{self.BASE_URL}/{endpoint}"

        start_time = time.time()

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            dados = response.json().get('dados', [])
            df = pd.json_normalize(dados)

            elapsed = time.time() - start_time

            if self.verbose:
                print(f"🌐 GET {endpoint}")
                print(f"⏱ Tempo: {elapsed:.2f}s | 📦 Registros: {len(df)}")

            return df

        except requests.exceptions.HTTPError as e:
            if self.verbose:
                print(f"❌ HTTP error em {endpoint}: {e}")
            return pd.DataFrame()

        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"⚠️ Erro de conexão em {endpoint}: {e}")
            return pd.DataFrame()