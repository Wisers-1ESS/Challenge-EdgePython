import os, requests, json
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone, timedelta

def main():
    load_dotenv() # Carrega as variáveis de ambiente
    apiKey = os.getenv("API_KEY") # Atribui o valor da variável de ambiente API_KEY à variável apiKey
    seasonID = most_recent_season_ID(get_seasons(apiKey)) # Chama a função most_recent_season_ID() e armazena o retorno na variável seasonID
    events = get_events(seasonID, apiKey) # Chama a função get_events() e armazena o retorno na variável events
    most_recent_event(events) # Chama a função most_recent_event() passando o objeto events como argumento

def get_seasons(apiKey): # Retorna um objeto com todas as temporadas
    url =(f"https://api.sportradar.com/formulae/trial/v2/pt/seasons.json?api_key={apiKey}") # Define a URL da API
    headers = {"accept": "application/json"} # Define o cabeçalho da requisição
    response = requests.get(url, headers=headers) # Faz a requisição GET
    data = json.loads(response.text) # Converte o JSON para um objeto
    return data # Retorna o objeto com as temporadas

def get_events(seasonID, apiKey): # Retorna um objeto com todos os eventos de uma temporada
    url =(f"https://api.sportradar.com/formulae/trial/v2/pt/sport_events/{seasonID}/schedule.json?api_key={apiKey}")
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers) 
    data = json.loads(response.text)
    return data # Retorna o objeto com os eventos

def most_recent_event(events):
    timezone_br = timezone(timedelta(hours=-3))
    # Converte a data de string para datetime e ajusta o fuso horário para o horário de Brasília
    for stage in events['stages']:
        stage['scheduled'] = datetime.fromisoformat(stage["scheduled"]).astimezone(timezone_br)
        
    events_sorted = sorted(events['stages'], key=lambda x: x["scheduled"], reverse=True) # Ordena os eventos da data mais recente para a mais antiga
    
    now = datetime.now(events_sorted[0]["scheduled"].tzinfo) # Pega a data e hora atual
    # Encontra a data mais próxima de acontecer
    closest_event = min(events_sorted, key=lambda x: (x["scheduled"] - now).total_seconds() if x["scheduled"] > now else float('inf'))
    
    # print(f"A data do evento mais próximo é: {closest_event['scheduled'].strftime('%d/%m/%Y %H:%M')}")
    # Retorna o evento mais próximo de acontecer
    return closest_event

def most_recent_season_ID(seasons): # Retorna o ID da temporada mais recente
    return seasons["stages"][0]["id"] # Retorna o ID da temporada mais recente

main()