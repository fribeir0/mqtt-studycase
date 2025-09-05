import os
import random
import time
import signal
import paho.mqtt.client as mqtt

# Variáveis de ambiente
BROKER_HOST = os.getenv("BROKER_HOST", "mqtt-broker")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
TOPIC       = os.getenv("TOPIC", "sensor/temperature")
INTERVAL    = float(os.getenv("INTERVAL_SECONDS", "5"))
QOS         = int(os.getenv("QOS", "0"))
RETAIN      = os.getenv("RETAIN", "false").lower() == "true"
USERNAME    = os.getenv("USER")
PASSWORD    = os.getenv("PASSWD")
USE_TLS     = os.getenv("USE_TLS", "false").lower() == "true"
CA_CERT     = os.getenv("CA_CERT_PATH", "/app/certs/mosquitto.crt")

def generate_temperature():
    value = getattr(generate_temperature, "_val", 22.0)
    step = random.uniform(-0.5, 0.7)
    value = max(-40.0, min(140.0, value + step))
    generate_temperature._val = value
    return round(value, 2)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[sensor] ✅ Conectado com sucesso a {BROKER_HOST}:{BROKER_PORT}", flush=True)
    else:
        print(f"[sensor] ❌ Falha na conexão: rc={rc}", flush=True)

def on_disconnect(client, userdata, rc, properties=None):
    print(f"[sensor] 🔌 Desconectado rc={rc}", flush=True)

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # TLS se ativado
    if USE_TLS:
        print("[sensor] 🔐 Ativando TLS", flush=True)
        client.tls_set(ca_certs=CA_CERT)

    # Usuário/senha se definido
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    print(f"[sensor] 🌐 Conectando a {BROKER_HOST}:{BROKER_PORT}...", flush=True)
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=30)
    client.loop_start()

    stop = False
    def handle_sig(signum, frame):
        nonlocal stop
        stop = True
        print("[sensor] 🛑 Encerrando...", flush=True)
    signal.signal(signal.SIGTERM, handle_sig)
    signal.signal(signal.SIGINT, handle_sig)

    while not stop:
        temp = generate_temperature()
        payload = str(temp)
        info = client.publish(TOPIC, payload, qos=QOS, retain=RETAIN)
        info.wait_for_publish()
        print(f"[sensor] 📡 Publicado {payload} em '{TOPIC}' (qos={QOS}, retain={RETAIN})", flush=True)
        time.sleep(INTERVAL)

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
