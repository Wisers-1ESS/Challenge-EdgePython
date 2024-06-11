import serial
import time
import random

def main():
    porta = input("Digite a porta COM que deseja usar: ")
    ser = serial.Serial(porta, 9600, timeout=1)  # Use a segunda porta criada pelo VSPE

    try:
        while True:
            # Gera valores aleatórios para simular os dados de telemetria
            temperature = round(random.uniform(20.0, 30.0), 1)  # Temperatura entre 20.0 e 30.0 °C
            velocity = random.randint(0, 200)  # Velocidade entre 0 e 200 KM/Hr
            energy_consumption = random.randint(50, 150)  # Consumo de energia entre 50 e 150 KW

            # Envia os dados pela porta serial
            ser.write(f"Temperatura: {temperature} °C\n".encode())
            ser.write(f"Velocidade: {velocity} KM/Hr\n".encode())
            ser.write(f"Uso da bateria: {energy_consumption} KW\n".encode())
            print(f"Sent: {temperature} °C, {velocity} KM/Hr, {energy_consumption} KW")

            # Aguarda 1 segundo antes de enviar os próximos dados
            time.sleep(1)
    except KeyboardInterrupt:
        # Fechar a porta serial ao interromper o programa
        ser.close()
        print("\nSerial port closed.")
            
main()
