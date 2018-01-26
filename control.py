""" 
  Make 1/18
  Aus diversen Quellen inspiriertes Skript zum Steuern eines Raspberry Pi per Alexa
  
  Alle Funktionen in eine Klasse ausgelagert
  Die zu konfigurierenden GPIOS und Trigger zur besseren Uebersixchtlichkeit in switches.py ausgelagert
  Daniel Bachfeld, dab@make-magazin.de, dab@ct.de, Make Magazin 2018
  
"""

import fauxmo
import logging
import time


from debounce_handler import debounce_handler

 
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
    
    # Register the device callback as a fauxmo handler
    d = debounce_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
