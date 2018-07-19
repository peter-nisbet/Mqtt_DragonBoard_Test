import paho.mqtt.client as mqtt
import ssl
import json
import mraa


# Initialize GPIO Port
led_4 = mraa.Led("user4")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mailbox/doorControl")

# This callback is for the mailbox door control topic
def doorcontrol_callback(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

   #parse JSON message and extract command	
    doorStatus=json.loads(str(msg.payload))
    if(doorStatus["Status"] == "Open"):
	print("Door is now Open")
	led_4.setBrightness(1)
    else:
	print("Door is now Closed")
	led_4.setBrightness(0)


client = mqtt.Client()

client.on_connect = on_connect
client.message_callback_add("mailbox/doorControl", doorcontrol_callback)

#Set up TLS secure socket to communicate with the broker
'''
client.tls_set(ca_certs='/home/peter/Desktop/ca_certs/ca.crt',
	certfile='/home/peter/Desktop/certs/client.crt', 
	keyfile='/home/peter/Desktop/certs/client.key',
	cert_reqs=ssl.CERT_NONE,	
	tls_version=ssl.PROTOCOL_TLSv1_2)
'''
client.tls_set(ca_certs='/home/linaro/ca_certs/ca.crt',
	certfile='/home/linaro/certs/client.crt', 
	keyfile='/home/linaro/certs/client.key',
	cert_reqs=ssl.CERT_NONE,	
	tls_version=ssl.PROTOCOL_TLSv1_2)


#Added due to mismatched common name in certificates
client.tls_insecure_set(True)

client.connect("192.168.0.100", 8883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
