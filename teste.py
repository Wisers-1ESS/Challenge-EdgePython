import serial
import time

def main():
    ser = serial.Serial('COM5', 9600, timeout=1)  # Use a segunda porta criada pelo VSPE
    time.sleep(2)  # Aguarda a inicialização da porta serial

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

if __name__ == "__main__":
    main()
