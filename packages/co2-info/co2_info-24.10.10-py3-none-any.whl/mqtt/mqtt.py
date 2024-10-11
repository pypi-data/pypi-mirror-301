#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Receive data from an MQTT data broker.'''

from paho.mqtt.client import Client
import paho.mqtt.client as client
from uuid import getnode
from time import ctime
from argparse import ArgumentParser

CLIENT_ID = str(getnode()) + ' ' + ctime()

class MQTT():
    
    def __init__(self, server, port, topic, func, username, password):
        self.topic = topic
        self.func = func
        self.mqtt_c = Client(client.CallbackAPIVersion.VERSION1,
                             client_id=CLIENT_ID)
        self.mqtt_c.on_connect = self.on_connect
        self.mqtt_c.on_message = self.on_message
        self.mqtt_c.username_pw_set(username=username, password=password)
        self.mqtt_c.connect(server, port, 60)
        if __name__=='__main__':
            self.mqtt_c.loop_forever()
        else:
            self.mqtt_c.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        '''
        Callback function when a CONNECT response is received.
        '''
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        '''
        Callback function when a PUBLISH message is received.
        '''
        self.func(msg.payload)

    def stop(self):
        '''
        Stop the client, if used as a library.
        '''
        self.mqtt_c.loop_stop()

    def start(self):
        '''
        Start the client, if used as a library.
        '''
        self.mqtt_c.loop_start()
        
    def disconnect(self):
        '''
        Disconnect the client.
        '''
        self.mqtt_c.disconnect()
    
if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--server',
                        type=str,
                        required=False,
                        default='192.168.1.86',
                        help='address of the MQTT server, e.g. ' +
                        '192.168.1.86 or iot.fh-muenster, ...')
    parser.add_argument('--port',
                        type=str,
                        required=False,
                        default='1883',
                        help='MQTT server port, e.g. 1883')
    parser.add_argument('--topic',
                        type=str,
                        required=False,
                        default='sensor/eui-10061c160ef4feff',
                        help='MQTT data topic, e. g. ' +
                             'sensor/eui-10061c160ef4feff')
    parser.add_argument('--username',
                        type=str,
                        required=False,
                        default=None,
                        help='Username for data broker.')
    parser.add_argument('--password',
                        type=str,
                        required=False,
                        default=None,
                        help='Password for data broker.')
    args = parser.parse_args()
    mqtt = MQTT(args.server,
                args.topic,
                args.port,
                lambda x: print(x),
                args.username,
                args.password)
