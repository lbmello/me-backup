
import logging
from wakeonlan import send_magic_packet

class wake_on_lan:

    def __init__(self, mac_address):
        self.mac_address = mac_address

    
    def send_package(self):
        """Send the magic packet using wakeonlan module."""
        
        try:
            send_magic_packet(self.mac_address)
            logging.info(f"Magic packet sended to {self.mac_address} to wake up!")
        
        except ValueError:
            logging.error(f"MAC address {self.mac_address} is wrong.")

        