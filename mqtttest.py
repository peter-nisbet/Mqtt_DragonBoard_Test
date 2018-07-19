import paho.mqtt.client as mqtt
import ssl
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mailbox/doorcontrol")

# This callback is for the mailbox door control topic
def doorcontrol_callback(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    doorStatus=json.loads(str(msg.payload))
    if(doorStatus['status'] == "Open"):
	print("Door is now Open")
    else:
	print("Door is now Closed")


client = mqtt.Client()

client.on_connect = on_connect
client.message_callback_add("mailbox/doorcontrol", doorcontrol_callback)

#Set up TLS secure socket to communicate with the broker
client.tls_set(ca_certs='/home/peter/Desktop/ca-certs/ca.crt',
	certfile='/home/peter/Desktop/certs/client.crt', 
	keyfile='/home/peter/Desktop/certs/client.key',
	cert_reqs=ssl.CERT_NONE,	
	tls_version=ssl.PROTOCOL_TLSv1_2)
'''
client.tls_set(ca_certs='/home/linaro/ca-certs/ca.crt',
	certfile='/home/linaro/certs/client.crt', 
	keyfile='/home/linaro/certs/client.key',
	cert_reqs=ssl.CERT_NONE,	
	tls_version=ssl.PROTOCOL_TLSv1_2)
'''

#Added due to mismatched common name in certificates
client.tls_insecure_set(True)

client.connect("192.168.0.181", 8883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
