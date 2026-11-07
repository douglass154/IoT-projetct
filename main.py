# IoT-projetct

import network
import time
import urequests
from machine import Pin

# ===== CONFIGURACAO DO WIFI =====
SSID = "iPhone de Isaías"
SENHA_WIFI = "teste123"

# ===== CONFIGURACAO DO TELEGRAM =====
BOT_TOKEN = "8928635100:AAE10FY0uy-ECC6CJ8GELe6rrSNPGnjOPAE"
CHAT_ID = "8264299707"

# ===== BOTAO =====
# Botao ligado entre GPIO 23 e GND
botao = Pin(23, Pin.IN, Pin.PULL_UP)

# ===== LED DA ESP32 =====
led = Pin(2, Pin.OUT)
led.off()

# Funcao para piscar o LED
def piscar_led():
    print("Mensagem enviada! Piscando LED...")

    for i in range(3):
        led.on()
        time.sleep_ms(300)
        led.off()
        time.sleep_ms(300)

# ===== CONEXAO WIFI =====
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Conectando ao Wi-Fi...")

wifi.connect(SSID, SENHA_WIFI)

tentativas = 0

while not wifi.isconnected() and tentativas < 30:
    time.sleep(1)
    tentativas += 1
    print("Aguardando conexao...")

if not wifi.isconnected():
    raise RuntimeError("Nao foi possivel conectar ao Wi-Fi")

print("Wi-Fi conectado!")
print("Endereco IP:", wifi.ifconfig()[0])
print("Sistema pronto. Aperte o botao.")

# ===== ENVIO DA MENSAGEM =====
def enviar_mensagem():

    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"

    dados = {
        "chat_id": CHAT_ID,
        "text": "ALERTA DE EMERGENCIA!\n\n"
                "Samu - Emergencia Medica: 192\n"
                "CVV - Apoio Emocional: 188"
    }

    resposta = None

    try:
        resposta = urequests.post(url, json=dados)

        if resposta.status_code == 200:

            resultado = resposta.json()

            if resultado.get("ok"):
                print("Mensagem enviada com sucesso!")
                return True

            else:
                print("Telegram recusou a mensagem.")
                return False

        else:
            print("Erro HTTP:", resposta.status_code)
            return False

    except Exception as erro:
        print("Erro ao enviar mensagem:", erro)
        return False

    finally:
        if resposta is not None:
            resposta.close()

# ===== LOOP PRINCIPAL =====
while True:

    if botao.value() == 0:

        time.sleep_ms(50)

        if botao.value() == 0:

            print("Botao pressionado!")

            if wifi.isconnected():

                sucesso = enviar_mensagem()

                if sucesso:
                    piscar_led()
                else:
                    print("Mensagem nao enviada. Verifique a conexao.")

            else:
                print("Wi-Fi desconectado.")

            # Espera soltar o botao
            while botao.value() == 0:
                time.sleep_ms(20)

            time.sleep_ms(50)

    time.sleep_ms(20)