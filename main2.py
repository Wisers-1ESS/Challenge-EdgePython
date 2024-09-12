import os
import requests
import time
import msvcrt
import flet as ft
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, Back, init
import serial  # Importa a biblioteca serial

def main(page: ft.Page):
    page.title = "Hub da Formula E"
    page.window.width = 450
    page.window.height = 700
    page.window.maximizable = False
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    load_dotenv()  # Carrega as variáveis de ambiente
    apiKey = os.getenv("API_KEY")  # Atribui o valor da variável de ambiente API_KEY à variável apiKey
    seasonID = most_recent_season_ID(get_seasons(apiKey))  # Chama a função most_recent_season_ID() e armazena o retorno na variável seasonID
    time.sleep(1)  # Aguarda 1 segundo
    stage_infos = get_stage_infos(seasonID, apiKey)
    closestEvent = closest_event(stage_infos)

    def show_probability():
        teams_win_probabilities = get_teams_win_probabilities(seasonID, apiKey)
        for i, team in enumerate(teams_win_probabilities):
            win_probabilities.content.content.controls.append(ft.Text(value=(f"- {team['name']} - {team['probability']}%"), size=18, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY))
            
    def show_next_event(e):  # Mostra o evento mais próximo
        print(Fore.GREEN + f"{'*'*50}\n\nO evento mais próximo da Formula E ocorrerá em {closestEvent['scheduled'].strftime('%d/%m/%Y %H:%M')}." +
        f"\nO evento acontecerá no {closestEvent['venue']['name']}, em {closestEvent['venue']['city']}, {closestEvent['venue']['country']}\n\n{'*'*50}." + Style.RESET_ALL)
    
    def show_teams(e):  # Retorna um objeto com as equipes
        teams = stage_infos['teams']
        print(f"{Style.BRIGHT+Fore.GREEN}Selecione a equipe para ver mais informações:")
        for i, team in enumerate(teams):
            print(f"{Back.YELLOW+Fore.MAGENTA}{i+1}. {team['name']}{Back.RESET}")  # Imprime o nome das equipes
        teamID = input(f"{Style.RESET_ALL+Fore.LIGHTWHITE_EX}Digite o número da equipe desejada: ")  # Pede ao usuário para digitar o número da equipe desejada
        teamID = int(teamID) if teamID.isdigit() else 0
        if teamID < 1 or teamID > len(teams):
            return print(Fore.RED + "Equipe inválida")
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
        selected_team = teams[teamID - 1]
        team_result = selected_team['result']
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.GREEN}Informações sobre a equipe {selected_team['name']}:\n")
        print(f"Nome: {Fore.BLACK+selected_team['name']+Fore.GREEN}")
        print(f"País: {Fore.BLACK+selected_team['nationality']+Fore.GREEN}")
        print(f"Pontos nessa temporada: {Fore.BLACK}{team_result.get('points', '0')} {Fore.GREEN}")
        print(f"Posição no campeonato: {Fore.BLACK}{team_result.get('position', 'N/A')}º lugar{Fore.GREEN}")
        print(f"Vitórias: {Fore.BLACK}{team_result.get('victories', '0')} {Fore.GREEN}")
        print(f"Podiums: {Fore.BLACK}{team_result.get('podiums', '0')} {Fore.GREEN}")
        print(f"Voltas mais rápidas: {Fore.BLACK}{team_result.get('fastest_laps', '0')} {Fore.GREEN}")
        print(f"Pole Positions: {Fore.BLACK}{team_result.get('pole_positions', '0')} {Fore.GREEN}\n")
        print(f"Pilotos: {Fore.BLACK}")

        for driver in selected_team['competitors']:
            driver_result = driver['result']
            print(f"{Fore.GREEN} {driver_result.get('position', 'N/A')}º lugar - {Fore.CYAN}{driver_result.get('car_number', 'N/A')}{Fore.BLACK} - {' '.join(reversed(driver['name'].split(', ')))} - {driver['nationality']}")
    
    def clear_stack():
        _stack_main.controls.clear()
        _stack_main.update()
        
    def on_page_resize(e):
        next_event.height = page.window.height - 140
        teams.height = page.window.height - 140
        win_probabilities.height = page.window.height - 140
        telemetry.height = page.window.height - 140
        page.update()  # Atualiza a página para aplicar as mudanças
    
    page.on_resized = on_page_resize
    
    def navHandler(e):
        selected_index = e.control.selected_index
        page.update()
        if selected_index == 0:
            clear_stack()  # Limpa o conteúdo da página
            _stack_main.controls.append(next_event)
            page.update()
            next_event.content = ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            value="Próximo Evento da Fórmula E",
                            size=24,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.SECONDARY
                        ),
                        ft.Divider(height=10, thickness=2),  # Adicionando um divisor
                        ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Text(
                                    value="Data e Hora:",
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.SECONDARY
                                ),
                                ft.Text(
                                    value=closestEvent['scheduled'].strftime('%d/%m/%Y %H:%M'),
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    color=ft.colors.PRIMARY  # Cor diferente para o valor
                                ),
                                ft.Text(
                                    value="Local:",
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.SECONDARY
                                ),
                                ft.Text(
                                    value=closestEvent['venue']['name'],
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    color=ft.colors.PRIMARY
                                ),
                                ft.Text(
                                    value="Cidade:",
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.SECONDARY
                                ),
                                ft.Text(
                                    value=closestEvent['venue']['city'],
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    color=ft.colors.PRIMARY
                                ),
                                ft.Text(
                                    value="País:",
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.SECONDARY
                                ),
                                ft.Text(
                                    value=closestEvent['venue']['country'],
                                    size=18,
                                    text_align=ft.TextAlign.LEFT,
                                    color=ft.colors.PRIMARY
                                ),
                            ]
                        )
                    ]
                ),
                padding=20,
                border_radius=15,
                expand=0.8
            )
        elif selected_index == 1:
            clear_stack()  # Limpa o conteúdo da página
            _stack_main.controls.append(teams)
        elif selected_index == 2:
            clear_stack()  # Limpa o conteúdo da página
            _stack_main.controls.append(win_probabilities)
            win_probabilities.content = ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            value="Probabilidade de Vitória das Equipes",
                            size=24,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.SECONDARY
                        ),
                        ft.Divider(height=10, thickness=2),  # Adicionando um divisor
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            scroll=ft.ScrollMode.AUTO,
                        )
                    ]
                ),
                padding=20,
                border_radius=15,
                expand=0.8
            )
            show_probability()
        elif selected_index == 3:
            clear_stack()  # Limpa o conteúdo da página
            _stack_main.controls.append(telemetry)
        page.update()
        
        
    page.navigation_bar = ft.NavigationBar(
        on_change=navHandler,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.ACCESS_TIME_FILLED, label="Próximo Evento"),
            ft.NavigationBarDestination(icon=ft.icons.GROUPS, label="Equipes"),
            ft.NavigationBarDestination(icon=ft.icons.PERCENT, label="Chance de Vitória"),
            ft.NavigationBarDestination(icon=ft.icons.RADAR, label="Telemetria",),
        ]
    )
        
    next_event = ft.Container(
        height = page.window.height - 140,
        border_radius=10,
        bgcolor="#1d2024",
        alignment=ft.alignment.center,
        content=ft.Text("Próximo Evento")
    )
    
    teams = ft.Container(
        height = page.window.height - 140,
        border_radius=10,
        bgcolor="#1d2024",
        alignment=ft.alignment.center,
        content=ft.Text("Equipes")
    )
    
    win_probabilities = ft.Container(
        height = page.window.height - 140,
        border_radius=10,
        bgcolor="#1d2024",
        alignment=ft.alignment.center,
        content=ft.Text("Probabilidades")
    )
    
    telemetry = ft.Container(
        height = page.window.height - 140,
        border_radius=10,
        bgcolor="#1d2024",
        alignment=ft.alignment.center,
        content=ft.Text("Telemetria")
    )
        
    _main = ft.Container(
        width=450,
        height=600,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Bem-vindo ao Hub da Formula E",
                    size=24,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    value="Selecione uma opção no menu abaixo para continuar",
                    text_align=ft.TextAlign.CENTER,
                    size=18
                )
            ]
        )  
    )
    
    _stack_main = ft.Stack(
        controls=[
            _main
        ]    
    )

    page.add(_stack_main)
    
def most_recent_season_ID(seasons):  # Retorna o ID da temporada mais recente
    return seasons["stages"][0]["id"]  # Retorna o ID da temporada mais recente

def get_seasons(apiKey):  # Retorna um objeto com todas as temporadas
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/seasons.json?api_key={apiKey}"  # Define a URL da API
        headers = {"accept": "application/json"}  # Define o cabeçalho da requisição
        response = requests.get(url, headers=headers)  # Faz a requisição GET
        response.raise_for_status()  # Levanta exceção para status de erro HTTP
        data = response.json()  # Converte o JSON para um objeto
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    return data  # Retorna o objeto com as temporadas

def get_stage_infos(seasonID, apiKey):  # Retorna um objeto com as equipes
    try:
        url = f"https://api.sportradar.com/formulae/trial/v2/pt/sport_events/{seasonID}/summary.json?api_key={apiKey}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Erro na requisição da API")
        print(e)
        exit()
    return data['stage']  # Retorna o objeto com as equipes

def get_teams_win_probabilities(seasonID, apiKey):  # Retorna um objeto com as probabilidades de vitória das equipes
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
    return data['probabilities']['markets'][0]['outcomes']  # Retorna o objeto com as equipes

def closest_event(events):
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

    events_sorted = sorted(events['stages'], key=lambda x: x["scheduled"])  # Ordena os eventos da data mais próxima para a mais distante
    now = datetime.now(timezone_br)  # Pega a data e hora atual
    # Encontra a data mais próxima de acontecer
    closest_event = min(events_sorted, key=lambda x: (x["scheduled"] - now).total_seconds() if x["scheduled"] > now else float('inf'))
    # Retorna o evento mais próximo de acontecer
    return closest_event

def read_telemetry_data(e):
    porta = input(Fore.YELLOW + "Digite a porta serial do Arduino (Exemplo: COM5): " + Style.RESET_ALL)
    try:
        ser = serial.Serial(porta, 9600, timeout=1) 
    except serial.SerialException as e:
        print(Fore.RED + "Erro ao abrir a porta serial: " + str(e) + Style.RESET_ALL)
        return
    except Exception as e:
        print(Fore.RED + "Erro inesperado: " + str(e) + Style.RESET_ALL)
        return

    print(Fore.GREEN + Style.BRIGHT + "Dados de Telemetria do Arduino (Digite 'q' para sair):\n" + Style.RESET_ALL)
    time.sleep(2)  # Aguarda a inicialização da porta serial

    try:
        buffer = ""
        temperature = ""
        velocity = ""
        battery_usage = ""
        last_data_time = time.time()
        while True:
            # Verifica se há dados disponíveis na porta serial
            if ser.in_waiting > 0:
                try:
                    buffer += ser.read(ser.in_waiting).decode('utf-8')
                except UnicodeDecodeError:
                    buffer += ser.read(ser.in_waiting).decode('latin-1')
                    
                last_data_time = time.time()    

                # Verifica se há uma linha completa no buffer
                if '\n' in buffer:
                    lines = buffer.split('\n')
                    for line in lines[:-1]:
                        if 'Temperatura' in line:
                            temperature = line.strip()
                        elif 'Velocidade' in line:
                            velocity = line.strip()
                        elif 'Uso da bateria' in line:
                            battery_usage = line.strip()
                    
                    # Mantém a última linha incompleta no buffer
                    buffer = lines[-1]

                    # Exibe os dados quando ambos estão disponíveis
                    if temperature and battery_usage and velocity:
                        format_and_display_data(temperature, battery_usage, velocity)
                        temperature = ""
                        velocity = ""
                        battery_usage = ""
            else:
                # Verifica se passou mais de 5 segundos sem receber dados
                if time.time() - last_data_time > 5:
                    print(Fore.RED + "Erro: Nenhum dado recebido. Verifique a conexão do Arduino e a porta serial." + Style.RESET_ALL)
                    break

            # Verifica se há entrada do usuário
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode('utf-8')
                if user_input == 'q':  # Digite 'q' para sair
                    break
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print(Fore.RED + "Porta serial fechada." + Style.RESET_ALL)
        


def format_and_display_data(temperature, battery_usage, velocity):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + Style.BRIGHT + "Dados de Telemetria do Arduino (Digite 'q' para sair):\n" + Style.RESET_ALL)
    if temperature:
        print(Fore.CYAN + temperature + Style.RESET_ALL)
    if velocity:
        print(Fore.MAGENTA + velocity + Style.RESET_ALL)
    if battery_usage:
        print(Fore.YELLOW + battery_usage + Style.RESET_ALL)
        
ft.app(target=main)