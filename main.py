import os, requests, json
from dotenv import load_dotenv, dotenv_values

def main():
    load_dotenv() # Carrega as variáveis de ambiente
    apiKey = os.getenv("API_KEY") # Atribui o valor da variável de ambiente API_KEY à variável apiKey
    seasonID = most_recent_season_ID(get_seasons(apiKey)) # Chama a função most_recent_season_ID() e armazena o retorno na variável seasonID
    events = get_events(seasonID, apiKey) # Chama a função get_events() e armazena o retorno na variável events
    print(events) # Chama a função most_recent_event() 


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
    return events["stages"][0]["events"][0]["scheduled"] # Retorna a data do evento mais recente

def most_recent_season_ID(seasons): # Retorna o ID da temporada mais recente
    return seasons["stages"][0]["id"] # Retorna o ID da temporada mais recente

main()