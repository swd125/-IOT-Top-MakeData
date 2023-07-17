import json
import ssl
import time
from paho.mqtt import client as mqtt_client

from decode import top_decode
from influxdb import InfluxDB
from dotenv import dotenv_values

env = dotenv_values(".env")

# ---- IOT Core ----
broker = env.get('TOP_IOT_CORE_BROKER')
port = int(env.get('TOP_IOT_CORE_PORT'))
client_id = env.get('TOP_IOT_CORE_CLIENT_ID')
topic = env.get('TOP_IOT_CORE_TOPIC')
tsl = {
    "ca_certs" : env.get('TOP_IOT_CORE_TSL_CA_CERTS'),
    "certfile" : env.get('TOP_IOT_CORE_TSL_CERT_FILE'),
    "keyfile"  : env.get('TOP_IOT_CORE_TSL_KEY_FILE'),
}

class Mqtt_Subscription_v1():

    def __init__(self, broker, port, client_id, tsl=None) -> None:
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.tsl = tsl

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            print("on_connect")
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)

        if self.tsl and self.tsl.get('ca_certs') and self.tsl.get('certfile') and self.tsl.get('keyfile'):
            client.tls_set(
                ca_certs = self.tsl.get('ca_certs'),
                certfile = self.tsl.get('certfile'),
                keyfile  = self.tsl.get('keyfile'),
                tls_version = ssl.PROTOCOL_TLSv1_2
            )
            
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        self.client = client
        return self.client


    def subscribe(self, topic):
        def on_message(client, userdata, msg):
            message_result = json.loads(msg.payload.decode())
            # result = {"topic": msg.topic, "result": message_result}

            encode_data = top_decode(message_result)
            if encode_data:
                # print("encode_data > ", encode_data)
                InfluxDB().write_json_data(encode_data)


        self.client.subscribe(topic)
        self.client.on_message = on_message
        return self.client.on_message


    def run_subscribe(self, topic):
        client = self.connect_mqtt()
        self.subscribe(topic)
        client.loop_forever()
        # client.loop(timeout=60)


if __name__ == '__main__':
    client = Mqtt_Subscription_v1(broker, port, client_id, tsl)
    client.run_subscribe(topic)
