#!/usr/bin/env python3

"""
Marco Toledo,
  @Ocramoi

Junho de 2021
"""

import os
import signal
import logging
import tweepy
import csv
from time import sleep

# Variáveis de ambiente (informações de autenticação)
from dotenv import load_dotenv
load_dotenv()

# Configuração para logging
logging.basicConfig(filename="log",
                    format='%(asctime)s - %(name)s\
                    - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger()

# Número mínimo de timeout entre requisições,
# considerando o limite de 15 requisições a cada
# 15 minutos e as distribuindo uniformimente (1 por minuto)
MAX_REQ_TIMEOUT = (15*60)/15

# Informações de ambiente para autenticação do bot
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")


# Loga recebimento de sinal no console
def trataSinal(SIG_NUM: int, frame: None) -> None:
    logger.info("Sinal de terminamento ({}) recebido".format(SIG_NUM))
    exit(0)


signal.signal(signal.SIGINT, trataSinal)
signal.signal(signal.SIGTERM, trataSinal)


# Confere por novos 'amigos' (contas seguidas) a partir do usuário dado
# e tweeta de acordo com o [formato]
def conferenciaRegistro(api: tweepy.API, registro: str, formato: str) -> int:
    # Estabelesce nome de arquivo local para controle de seguidores
    nomeArq = "Data/{}".format(
        registro["Usuário"]
    )

    # Busca última página de seguidores (máx. 20) e trata erro de API
    try:
        seguindo = api.friends(screen_name=registro["Usuário"])
    except Exception as e:
        logger.error(e)
        return 1

    # Se arquivo ainda não criado apenas salva amigos atuais
    if not os.path.exists(nomeArq):
        with open(nomeArq, "a+") as ultRegistro:
            for amigo in seguindo:
                ultRegistro.write(amigo.screen_name)
                ultRegistro.write("\n")
        return 0

    # Lê amigos salvos
    ultimo = []
    with open(nomeArq, "r+") as ultRegistro:
        ultimo = ultRegistro.read().splitlines()
        ultRegistro.truncate(0)

    # Tweeta cada amigo que não consta na última conferência
    for amigo in seguindo:
        if amigo.screen_name == ultimo[0]:
            break
        api.update_status(formato.format(
            registro["Usuário"],
            amigo.screen_name
        ))
        # Printa tweet escrito (USO EM DEBUGAÇÃO!)
        # print(formato.format(
        #     registro["Usuário"],
        #     amigo.screen_name
        # ))

    # Escreve nova lista de amigos para arquivo
    with open(nomeArq, "a+") as ultRegistro:
        for amigo in seguindo:
            ultRegistro.write(amigo.screen_name)
            ultRegistro.write("\n")

    return 0


def main():
    # Configuração do handler da API
    print("Inicializando autenticador e abrindo API...")
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Confere autorização
    if not api.verify_credentials():
        logger.error("Erro na verificação das credenciais")
        exit(1)
    logger.info("Credenciais verificadas")

    # Lê lista de usuários e formato de tweet
    print("Configurando ambiente...")
    with open("formato.txt", "r") as arqFormato:
        formato = arqFormato.read().strip()

    listaUsers = []
    try:
        with open("Usuarios.csv", "r") as arq:
            usuariosConf = csv.DictReader(arq, delimiter=",")
            for linha in usuariosConf:
                listaUsers.append(linha)
    except FileNotFoundError:
        logger.warning("Arquivo não existe")
        exit(1)
    except Exception:
        logging.warning("Erro no arquivo")
        exit(1)

    # Loop de conferência registro a registro
    print("Entrando no loop funcional...")
    while True:
        for registro in listaUsers:
            if conferenciaRegistro(api, registro, formato):
                print("Erro na execução da conferência do usuário @{},\
                caso o erro persista, confira o perfil!".format(
                    registro["Usuário"]
                ))
            sleep(MAX_REQ_TIMEOUT)


if __name__ == "__main__":
    main()
