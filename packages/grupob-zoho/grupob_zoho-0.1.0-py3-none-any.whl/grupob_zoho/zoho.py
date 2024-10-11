# grupob_zoho/zoho.py
import requests
import json
import os
from datetime import datetime, timedelta, timezone

class ZohoCRM:
    BASE_URL = "https://www.zohoapis.com/crm"

    def __init__(self, credential:dict = {"client_id":str,"client_secret":str,"reflesh_token":str},save_cache_token="token_cache.json"):
        """
        Inicializa a classe de manipulação do zoho.

        Parâmetros:
        - credential (dict): Dicionário contendo o 'client_id', 'client_secret' e 'reflesh_token' do credential.
            - client_id (str): O client_id do credential (obrigatório).
            - client_secret (str): O client_secret do credential (obrigatório).
            - reflesh_token (str): O reflesh_token do credential (obrigatório).
        - save_cache_token (str): Caminho onde deve ser salvo o cache do token, padrão "token_cache.json"    
        """
        if not isinstance(credential, dict) or 'client_id' not in credential or 'client_secret' not in credential or 'reflesh_token' not in credential:
            raise ValueError("O dicionário 'credential' deve conter as chaves 'client_id', 'client_secret' e 'reflesh_token'.")
        
        self.token = None  # Armazena o token em cache
        self.token_expiry = None  # Armazena a data de expiração do token
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.reflesh_token = os.getenv('REFLESH_TOKEN')
        self.TOKEN_CACHE_FILE = save_cache_token
        self.load_token_cache()  # Carrega o token do cache

    def load_token_cache(self):
        """Carrega o token e a expiração do arquivo de cache, se existir."""
        if os.path.exists(self.TOKEN_CACHE_FILE):
            with open(self.TOKEN_CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                self.token = cache_data.get('token')
                self.token_expiry = datetime.fromisoformat(cache_data.get('expiry'))

    def save_token_cache(self):
        """Salva o token e a expiração em um arquivo de cache."""
        with open(self.TOKEN_CACHE_FILE, 'w') as f:
            json.dump({
                'token': self.token,
                'expiry': self.token_expiry.isoformat() if self.token_expiry else None
            }, f)

    def gera_headers(self, token=None):
        """Gera os cabeçalhos necessários para as requisições."""
        if token is None:
            token = self.get_token()
        return {
            'Authorization': f'Zoho-oauthtoken {token}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        """Obtém um token de acesso armazenado em cache, se ainda for válido."""
        if self.token and self.token_expiry and datetime.now(timezone.utc) < self.token_expiry:
            return self.token

        # Se não houver token válido, obtenha um novo token
        return self.refresh_token()

    def refresh_token(self):
        """Obtém um novo token de autenticação e o armazena em cache."""
        url = "https://accounts.zoho.com/oauth/v2/token"
        payload = {
            'refresh_token': f'{self.reflesh_token}',
            'client_id': f'{self.client_id}',
            'client_secret': f'{self.client_secret}',
            'grant_type': 'refresh_token'
        }
        response = requests.request("POST", url, data=payload)
        data_dict = json.loads(response.text)

        # Implementar a lógica para obter o token de autenticação (exemplo)
        new_token = data_dict['access_token']
        self.token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)  # Define a validade do token (1 hora)
        self.token = new_token  # Armazena o novo token em cache

        self.save_token_cache()  # Salva o novo token no cache
        return new_token

    def getLeadsModulo(self, criteria, modulo, fields, version='v3'):
        """Obtém leads de um módulo com base em critérios específicos."""
        url = f"{self.BASE_URL}/{version}/{modulo}/search"
        page = 1
        lista = []

        while True:
            params = {
                "fields": fields,
                "criteria": criteria,
                "per_page": 200,
                "page": page
            }
            headers = self.gera_headers()
            response = requests.get(url, headers=headers, params=params)
            if response.text != "":
                parsed = response.json()

                if 'code' in parsed and parsed['code'] == "INVALID_TOKEN":
                    self.refresh_token() #se o token venceu devemos renovar ele, pois ele expirou
                else:
                    print(f"ZOHO::PAGE {page}")
                    lista.extend(parsed['data'])

                    if parsed['info']['more_records'] == False:
                        break
                    page += 1

        return lista

    def getLeadsModuloHistory(self, fields, modulo, id_lead, version='v5'):
        """Obtém o histórico de estágios de um lead específico."""
        url = f"{self.BASE_URL}/{version}/{modulo}/{id_lead}/Stage_History"
        params = {"fields": fields}
        headers = self.gera_headers()

        response = requests.get(url, headers=headers, params=params)
        parsed = response.json()

        if 'code' in parsed and parsed['code'] == "INVALID_TOKEN":
            token = self.refresh_token() #se o token venceu devemos renovar ele, pois ele expirou
            headers = self.gera_headers(token)
            response = requests.get(url, headers=headers, params=params)
            parsed = response.json()
        

        return parsed.get('data', [])                   