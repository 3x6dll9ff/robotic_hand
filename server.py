import threading

from datetime import datetime
import time

import serial
import serial.tools.list_ports

from flask import Flask, request


class Counter:
    def __init__(self):
        self.count = 0
    
    def count_up(self):
        self.count += 1
    
    def reset(self):
        self.count = 0


class Device:
    VID = '1A86'
    PID = '7523'
    BAUD_RATE = 9600
    
    def __init__(self):
        self.serial = None
        self.waiting = False
        self.message_update_time = 150
        self.waiting_message_counter = Counter()
        threading.Thread(target=self.__connect_loop).start()
    
    def __get_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if f'{self.VID}:{self.PID}' in p.hwid:
                return p.device
        return None
    
    def __connect(self):
        port = self.__get_port()
        if port and not self.serial:
            try:
                self.serial = serial.Serial(port, self.BAUD_RATE, timeout=1)
                self.waiting = False
                print(f'[{datetime.now()}] Connected to device on {port}')
            except serial.SerialException as e:
                print(f'[{datetime.now()}] Failed to connect to device!')
        elif not port:
            if self.serial:
                self.serial = None
                print(f'[{datetime.now()}] Disconnected from device')
            if not self.waiting or self.waiting_message_counter.count >= self.message_update_time:
                self.waiting_message_counter.reset()
                self.waiting = True
                print(f'[{datetime.now()}] Waiting for device...')
            else:
                self.waiting_message_counter.count_up()
    
    def __connect_loop(self):
        while True:
            self.__connect()
            time.sleep(0.1)


app = Flask(__name__)


@app.route('/send_to_arduino', methods=['POST'])
def send_to_arduino():
    if device.serial:
        data = request.data
        try:
            device.serial.write(data)
            return f"Data sent to Arduino: {data.decode('utf-8')}", 200
        except Exception as e:
            return f"Failed to send data: {str(e)}", 500
    else:
        return 'Device not connected', 500


if __name__ == '__main__':
    device = Device()
    app.run(host='0.0.0.0', port=5000)
