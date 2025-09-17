from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import subprocess
import time
from datetime import datetime

ruta = "/home/Cesarin/log_script.txt"

# Diccionario de acciones (comando → script/programa a ejecutar)
actions = {
        "a": "/home/Cesarin/Alexa/Server/adelante.py",	# Adelante
        "r": "/home/Cesarin/Alexa/Server/atras.py",	# Retrocede
        "i": "/home/Cesarin/Alexa/Server/izquierda.py",	# Izquierda
        "d": "/home/Cesarin/Alexa/Server/derecha.py",	# Derecha
        "p": "/home/Cesarin/Alexa/Server/paro.py"	# Detener
}

def escribir_log(mensaje):
	fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	linea = f"[{fecha_actual}] {mensaje}\n"
	with open(ruta, "a") as archivo:
		archivo.write(linea)

def on_message_received(payload, **kwargs):
        command = payload.decode('utf-8').strip().lower()  # Limpia el comando

        if command in actions:
                print(f"Ejecutando: {command}")
                subprocess.run(["sudo", "python3", actions[command]])  # Ejecuta el script Python
        else:
                print(f"Comando no reconocido: {command}")

# Configuración MQTT
mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint="anw65onk7dl8o-ats.iot.us-east-2.amazonaws.com",
        cert_filepath="/home/Cesarin/certs/certificate.pem.crt",
        pri_key_filepath="/home/Cesarin/certs/private.pem.key",
        ca_filepath="/home/Cesarin/certs/AmazonRootCA1.pem",
        client_id="LaptopTest",
        clean_session=False,
        keep_alive_secs=30
)

# Intentar conexión con AWS con reintentos
connected = False
while not connected:
        try:
                print("Conectando a AWS IoT Core...")
                mqtt_connection.connect().result()
                print("Conexión exitosa")
                connected = True
        except Exception as e:
                print(f"Error de conexión: {e}")
                time.sleep(5)

# Intentar suscripción al tema MQTT con reintentos
subscribed = False
while not subscribed:
        try:
                print("Suscribiendose a robot/control...")
                mqtt_connection.subscribe(
                        topic="robot/control",
                        qos=mqtt.QoS.AT_LEAST_ONCE,
                        callback=on_message_received
                ).result()
                print("Suscripción exitosa")
                mensaje = f"El programa se ha ejecutado con éxito: [{fecha_actual}]\n"
                with open(ruta, "a") as archivo:
                        archivo.write(mensaje)
                subscribed = True
        except Exception as e:
                print(f"Error de suscripción: {e}")
                time.sleep(5)

# Mantén el script en ejecución
try:
        while True:
                time.sleep(1)
except KeyboardInterrupt:
        mqtt_connection.disconnect().result()
        print("Desconectado")
