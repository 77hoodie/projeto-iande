import serial
import pandas as pd
from datetime import datetime
import os
import time

def formatar_peso(valor):
    """Peso já está em gramas"""
    return round(float(valor), 1)

PORTA = 'COM5'                
BAUD_RATE = 115200
ARQUIVO_SAIDA = 'dados_balanca_agua.csv'
HEADER_ARDUINO = "Timestamp_ms,Peso_kg,AguaPresente,LeituraSensorAgua,EstadoMudou"

dados = []

def verificar_porta():
    """Verifica se a porta está disponível"""
    try:
        ser = serial.Serial(PORTA, BAUD_RATE, timeout=2)
        ser.close()
        return True
    except:
        return False

def criar_arquivo_se_inexistente():
    """Cria arquivo CSV vazio se não existir"""
    if not os.path.exists(ARQUIVO_SAIDA):
        with open(ARQUIVO_SAIDA, 'w') as f:
            f.write("DataHora,Timestamp_ms,Peso_g,AguaPresente,LeituraSensorAgua,EstadoMudou\n")
        print(f"Arquivo {ARQUIVO_SAIDA} criado com sucesso!")

if not verificar_porta():
    print(f"ERRO: Porta {PORTA} não disponível. Verifique:")
    print("1. Se o Arduino está conectado")
    print("2. Se a porta está correta")
    print("3. Se nenhum outro programa está usando a porta")
    exit()

criar_arquivo_se_inexistente()

try:
    ser = serial.Serial(PORTA, BAUD_RATE, timeout=2)
    print(f"\nConectado à porta {PORTA} ({BAUD_RATE} baud)")
    
    print("Aguardando cabeçalho...")
    while True:
        linha = ser.readline().decode('utf-8', errors='ignore').strip()
        if HEADER_ARDUINO in linha:
            print("Cabeçalho detectado. Iniciando coleta...")
            break

    try:
        while True:
            linha = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if not linha or HEADER_ARDUINO in linha:
                continue
                
            try:
                valores = linha.split(',')
                if len(valores) == 5:
                    registro = {
                        'DataHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Timestamp_ms': int(valores[0]),
                        'Peso_g': formatar_peso(valores[1]),
                        'AguaPresente': int(valores[2]),
                        'LeituraSensorAgua': int(valores[3]),
                        'EstadoMudou': int(valores[4])
                    }
                    dados.append(registro)
                    
                    print(f"Leitura: {registro['Timestamp_ms']} | Peso: {registro['Peso_g']}g | Água: {'SIM' if registro['AguaPresente'] else 'NÃO'}")
                    
                    if len(dados) % 10 == 0:
                        pd.DataFrame(dados).to_csv(ARQUIVO_SAIDA, mode='a', header=not os.path.exists(ARQUIVO_SAIDA), index=False)
                        print(f"Dados salvos (total: {len(dados)})")

            except Exception as e:
                print(f"Erro processando linha: {linha} | Erro: {str(e)}")

    except KeyboardInterrupt:
        print("\nFinalizando coleta...")

finally:
    if dados:
        pd.DataFrame(dados).to_csv(ARQUIVO_SAIDA, mode='a', header=not os.path.exists(ARQUIVO_SAIDA), index=False)
        print(f"\nDados finais salvos em {ARQUIVO_SAIDA} ({len(dados)} registros)")
    
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Conexão serial fechada")