################################################################################################ 
####################################### CLIENTE MQTT ########################################### 
################################################################################################
import random
import time
import geocoder
import geopy.distance

# Aquí puedes utilizar la función nombre_de_la_funcion

from paho.mqtt import client as mqtt_client

#Local
#BROKER = 'localhost'
#PORT = 1883
#0TOPIC = "/test"
# generate client ID with pub prefix randomly
#CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
#USERNAME = 'admin'
#PASSWORD = 'public'
#FLAG_CONNECTED = 0

##Posicion actual
def obtener_posicion_actual():
    g = geocoder.ip('me')
    if g.latlng is not None:
        latitud, longitud = g.latlng
        return latitud, longitud
    else:
        return None

posicion = obtener_posicion_actual()
if posicion is not None:
    latitud, longitud = posicion
    print(f"La posición actual es: Latitud = {latitud}, Longitud = {longitud}")
else:
    print("No se pudo obtener la posición actual.")

# Punto A: Posición actual
latitud_a, longitud_a = 40.7128, -74.0060  # Actualiza con tu posición actual

# Punto B: Posición cercana
latitud_b, longitud_b = 40.7129, -74.0059  # Actualiza con las coordenadas del punto B cercano

# Calcular la distancia entre los puntos A y B
distancia = geopy.distance.distance((latitud_a, longitud_a), (latitud_b, longitud_b)).meters

# Distancia máxima permitida
distancia_maxima = 100  # Actualiza con la distancia máxima permitida

# Simular el movimiento en incrementos de 10 metros
incremento = 10
while distancia > incremento:
    # Calcular la dirección del movimiento
    delta_latitud = (latitud_b - latitud_a) / distancia * incremento
    delta_longitud = (longitud_b - longitud_a) / distancia * incremento

    # Actualizar la posición actual
    latitud_a += delta_latitud
    longitud_a += delta_longitud

    # Recalcular la distancia restante
    distancia = geopy.distance.distance((latitud_a, longitud_a), (latitud_b, longitud_b)).meters

    # Verificar si se excede la distancia máxima
    if distancia > distancia_maxima:
        # Configurar cliente MQTT
        client = mqtt.Client()
        client.connect(broker, port)

        # Enviar mensaje MQTT
        mensaje = "La trayectoria excede la distancia máxima permitida"
        client.publish(topic, mensaje)

        # Cerrar conexión MQTT
        client.disconnect()
        break

# Imprimir la posición final cercana al punto B
print(f"La posición final es: Latitud = {latitud_a}, Longitud = {longitud_a}")

#Hive
BROKER = 'mqtt-dashboard.com'
PORT = 8884
TOPIC_DATA = "arquitectura"
TOPIC_ALERT = "arquitecturav2"
##generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    ##print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
       ##publish(client,TOPIC_ALERT,"Hola")               

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)


client = connect_mqtt()
def run():
    while True:
        client.loop_start()
        time.sleep(1)
        if FLAG_CONNECTED:
            print("Wait for message...")
        else:
            client.loop_stop()


if __name__ == '__main__':
    run()