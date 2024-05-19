import os
import requests
import json
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, Back, init

def main():
    init()
    load_dotenv() # Carrega as variáveis de ambiente
    apiKey = os.getenv("API_KEY") # Atribui o valor da variável de ambiente API_KEY à variável apiKey
    seasonID = most_recent_season_ID(get_seasons(apiKey)) # Chama a função most_recent_season_ID() e armazena o retorno na variável seasonID
    menu = [
        {"id": 1, "title": "Ver próximo evento da Formula E"},
        {"id": 2, "title": "Ver informações sobre os times da Formula E"},
        {"id": 3, "title": "Ver a probabilidade dos times de ganharem da Formula E"},
        {"id": 4, "title": "Sair"},
    ]
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + "*" * 50)
        print("Bem-vindo às informações sobre a Fórmula E!")
        print("*" * 50)
        print(f"{Fore.YELLOW}Escolha uma opção: {Style.NORMAL}")
        for item in menu:
            print(f"{item['id']} - {item['title']}") # Imprime o menu
        option = input("Digite o número da opção desejada: ") # Pede ao usuário para digitar a opção desejada
        option = int(option) if option.isdigit() else 0
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
        match option:
            case 1:
                closestEvent = closest_event(seasonID, apiKey)
                print(Fore.GREEN + f"{'*'*50}\n\nO evento mais próximo da Formula E ocorrerá em {closestEvent['scheduled'].strftime('%d/%m/%Y %H:%M')}." +
                      f"\nO evento acontecerá no {closestEvent['venue']['name']}, em {closestEvent['venue']['city']}, {closestEvent['venue']['country']}\n\n{'*'*50}." + Style.RESET_ALL)
            case 2:
                get_teams(seasonID, apiKey)
            case 3:
                print(Fore.GREEN + Style.BRIGHT + "Probabilidade de vitória das equipes da Formula E:\n" + Style.RESET_ALL + Fore.LIGHTYELLOW_EX)
                for i, team in enumerate(get_teams_win_probabilities(seasonID, apiKey)):
                    print(f"{i+1}. {team['name']} - {team['probability']}%\n{'-'*50}")
            case 4:
                break
            case _:
                print(Fore.RED + Style.BRIGHT + "Opção inválida")
        print(Fore.RED + "Digite qualquer tecla para voltar ao menu")
        input()
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela

def get_seasons(apiKey): # Retorna um objeto com todas as temporadas
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/seasons.json?api_key={apiKey}" # Define a URL da API
        headers = {"accept": "application/json"} # Define o cabeçalho da requisição
        response = requests.get(url, headers=headers) # Faz a requisição GET
        response.raise_for_status() # Levanta exceção para status de erro HTTP
        data = response.json() # Converte o JSON para um objeto
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    return data # Retorna o objeto com as temporadas

def get_events(seasonID, apiKey): # Retorna um objeto com todos os eventos de uma temporada
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/sport_events/{seasonID}/schedule.json?api_key={apiKey}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    return data # Retorna o objeto com os eventos

def closest_event(seasonID, apiKey):
    events = get_events(seasonID, apiKey) # Chama a função get_events() e armazena o retorno na variável events
    timezone_br = timezone(timedelta(hours=-3))
    # Converte a data de string para datetime e ajusta o fuso horário para o horário de Brasília
    try:
        for stage in events['stages']:
            stage['scheduled'] = datetime.fromisoformat(stage["scheduled"]).astimezone(timezone_br)
    except KeyError:
        print(Fore.RED + "Erro na requisição da API")
        print("Não foi possível encontrar a chave 'scheduled' no JSON")
        print("Reinicie o programa e tente novamente")
        exit()

    events_sorted = sorted(events['stages'], key=lambda x: x["scheduled"]) # Ordena os eventos da data mais próxima para a mais distante
    now = datetime.now(timezone_br) # Pega a data e hora atual
    # Encontra a data mais próxima de acontecer
    closest_event = min(events_sorted, key=lambda x: (x["scheduled"] - now).total_seconds() if x["scheduled"] > now else float('inf'))
    # Retorna o evento mais próximo de acontecer
    return closest_event

def most_recent_season_ID(seasons): # Retorna o ID da temporada mais recente
    return seasons["stages"][0]["id"] # Retorna o ID da temporada mais recente

def get_teams(seasonID, apiKey): # Retorna um objeto com as equipes
    teams = get_teams_win_probabilities(seasonID, apiKey)
    print(f"{Style.BRIGHT+Fore.GREEN}Selecione a equipe para ver mais informações:")
    for i, team in enumerate(teams):
        print(f"{Back.YELLOW+Fore.MAGENTA}{i+1}. {team['team']['name']}{Back.RESET}") # Imprime o nome das equipes
    teamID = input(f"{Style.RESET_ALL+Fore.LIGHTWHITE_EX}Digite o número da equipe desejada: ") # Pede ao usuário para digitar o número da equipe desejada
    teamID = int(teamID) if teamID.isdigit() else 0
    if teamID < 1 or teamID > len(teams): return print(Fore.RED + "Equipe inválida")
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela
    print(f"{Fore.GREEN}Informações sobre a equipe {teams[teamID-1]['team']['name']}:\n")
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/teams/{teams[teamID-1]['team']['id']}/profile.json?api_key={apiKey}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        team = response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    print(f"Nome: {Fore.BLACK+team['team']['name']+Fore.GREEN}")
    print(f"País: {Fore.BLACK+team['team']['nationality']+Fore.GREEN}")
    print(f"Probabilidade de vitória: {Fore.BLACK}{teams[teamID-1]['probability']}% {Fore.GREEN}")
    print(f"Pilotos: {Fore.BLACK}")
    for driver in team['competitors']:
        print(f"{' '.join(reversed(driver['name'].split(', ')))} - {driver['nationality']}")

def get_teams_win_probabilities(seasonID, apiKey): # Retorna um objeto com as probabilidades de vitória das equipes
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/sport_events/{seasonID}/probabilities.json?api_key={apiKey}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    
    return data['probabilities']['markets'][0]['outcomes'] # Retorna o objeto com as equipes

main()