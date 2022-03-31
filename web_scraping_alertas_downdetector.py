#!/usr/bin/python3
import requests
import subprocess
from bs4 import BeautifulSoup
import re

resposta = "OK"
servicos = ["alelo","amazon","amazonprimevideo","amazonwebservices","anydesk","apexlegends","bancodobrasil","bancointer","bancoitau","bancopan","bancosantander","banrisul","binance","blizzardbattlenet","bradesco","c6bank","caixaeconomicafederal","callofduty","canva","claro","clear","cloudflare","correios","counterstrike","crunchyroll","dataprev","deadbydaylight","discord","disney","dota2","ea","ecac","embratel","enem","epicgamesstore","esocial","facebook","facebookmessenger","fallguys","fifa","fortnite","freefire","garena","github","globo","globoplay","gmail","google","googledrive","googlemeet","googleplay","gta5","hbo","ifood","instagram","iti","kinghost","leagueoflegends","linkedin","locaweb","mercadobitcoin","mercadolivre","microsoft","microsoftazure","microsoftteams","netflix","notafiscaleletronica","notion","nubank","office365","oi","olx","onedrive","origin","outlook","overwatch","pagseguro","picpay","pinterest","playstationnetwork","pokemongo","pokerstars","rainbowsix","receitafederal","reddit","roblox","rocketleague","runescape","sefaz","sicredi","sky","skype","slack","spotify","steam","superdigital","teamviewer","telegram","terra","tiktok","tim","tinder","trello","tribunalsuperioreleitoral","twitch","twitter","uber","udemy","uol","uplaypc","valorant","waze","whatsapp","xboxlive","xpinvestimentos","youtube","zoom"]

for servico in servicos:
    subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k downdetector.status.{} -o {}".format(servico,1), shell=False)
    subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k downdetector.hora.data.{} -o '{}'".format(servico,resposta), shell=False)


page_request = requests.get('https://t.me/s/alertasdowndetector')
soup = BeautifulSoup(page_request.text, 'html.parser')

for texto in soup.find_all("div", {"class": "tgme_widget_message_text"}):
    conteudo = (texto.text)
    lista = conteudo.split('"')
    if "🟩 INCIDENTE RESOLVIDO 🟩" in conteudo:
        hora_mensagem = (re.search('\d[0-9]:\d[0-9]:\d[0-9]',conteudo).group(0))
        data_mensagem = (re.search('\d[0-9]\/\d[0-9]\/\d[0-9]\d[0-9]',conteudo).group(0))
        hora_data = str(hora_mensagem + " " + data_mensagem)
        item_zabbix_hora_data = "downdetector.hora.data." + lista[1].replace(" ","").lower()
        subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k {} -o 'UP {}'".format(item_zabbix_hora_data,hora_data), shell=False)
        
        item_zabbix = "downdetector.status." + lista[1].replace(" ","").replace("-","").replace(".","").replace("+","").replace("á","a").replace("ã","a").replace("â","a").replace("à","a").replace("é","e").replace("ê","e").replace("Á","a").replace("Ã","a").replace("Â","a").replace("À","a").replace("É","e").replace("Ê","e").replace("í","i").replace("ó","o").replace("õ","o").replace("ô","o").replace("ú","u").replace("ç","c").replace("Í","i").replace("Ó","o").replace("Õ","o").replace("Ô","o").replace("Ú","u").replace("Ç","c").lower()
        subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k {} -o {}".format(item_zabbix,1), shell=False)

    if "🟥 INCIDENTE 🟥" in conteudo:
        hora_mensagem = (re.search('\d[0-9]:\d[0-9]:\d[0-9]',conteudo).group(0))
        data_mensagem = (re.search('\d[0-9]\/\d[0-9]\/\d[0-9]\d[0-9]',conteudo).group(0))
        hora_data = str(hora_mensagem + " " + data_mensagem)
        item_zabbix_hora_data = "downdetector.hora.data." + lista[1].replace(" ","").lower()
        subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k {} -o 'DOWN {}'".format(item_zabbix_hora_data,hora_data), shell=False)
        
        item_zabbix = "downdetector.status." + lista[1].replace(" ","").replace("-","").replace(".","").replace("+","").replace("á","a").replace("ã","a").replace("â","a").replace("à","a").replace("é","e").replace("ê","e").replace("Á","a").replace("Ã","a").replace("Â","a").replace("À","a").replace("É","e").replace("Ê","e").replace("í","i").replace("ó","o").replace("õ","o").replace("ô","o").replace("ú","u").replace("ç","c").replace("Í","i").replace("Ó","o").replace("Õ","o").replace("Ô","o").replace("Ú","u").replace("Ç","c").lower()
        subprocess.run("zabbix_sender -z 127.0.0.1 -s ZabbixSender -k {} -o {}".format(item_zabbix,0), shell=False)
