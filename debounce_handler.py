"""
Klasse  

"""

import time
import RPi.GPIO as GPIO


class debounce_handler(object):
    """Use this handler to keep multiple Amazon Echo devices from reacting to
       the same voice command.
    """
    DEBOUNCE_SECONDS = 0.3

    from switches import TRIGGERS, gpio_ports
    
 

    def __init__(self):
        self.lastEcho = time.time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def on(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, True, name)

    def off(self, client_address, name):
        if self.debounce():
            return True
        return self.act(client_address, False, name)

    def act(self, client_address, state, name):
        print "State", state, "on ", name, "from client @", client_address, "gpio port: ", self.gpio_ports[str(name)]
        self.trigger(self.gpio_ports[str(name)],state)
        return True

    def debounce(self):
        """If multiple Echos are present, the one most likely to respond first
           is the one that can best hear the speaker... which is the closest one.
           Adding a refractory period to handlers keeps us from worrying about
           one Echo overhearing a command meant for another one.
        """
        if (time.time() - self.lastEcho) < self.DEBOUNCE_SECONDS:
            return True

        self.lastEcho = time.time()
        return
    
    def trigger(self,port,state):
        print("port: ", port, "state: ", state)
        if state == True:
            GPIO.setup(port, GPIO.OUT)
            GPIO.output(port,GPIO.HIGH)
        else:
            GPIO.setup(port, GPIO.OUT)
            GPIO.output(port,GPIO.LOW)
