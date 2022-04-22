
import logging
from pythonping import ping
from wakeonlan import send_magic_packet

class wake_on_lan:

    def __init__(self, mac_address, ip):
        self.mac_address = mac_address
        self.ip = ip

        self.run_wol()


    def run_wol(self):
        """ Test communication to run WOL."""

        if self.fast_ping():
            logging.debug(f"WOL not sent, host {self.ip} its power on.")
        
        elif self.fast_ping():
            self.send_package()

        elif self.slow_ping():
            logging.error(f"host {self.ip} unreachable.")


    def send_package(self):
        """Send the magic packet using wakeonlan module."""

        try:
            send_magic_packet(self.mac_address)
            logging.debug(
                f"WOL Magic Packet sent to {self.mac_address} to wake up!"
            )
        
        except ValueError:
            logging.error(
                f"MAC address {self.mac_address} is wrong."
            )


    def fast_ping(self):
        """Ping the host ip two times to check communication."""

        response = ping(self.ip,
            timeout = 0.5,
            count = 2,
        )

        if response.success():
            return True
        
        else:
            logging.debug(f"FAIL - host {self.ip} have no ping response.")
            return False


    def slow_ping(self):
        """Ping the host ip more times to check communication."""

        response = ping(self.ip,
            timeout = 5,
            count = 3,
        )

        if response.success():
            return True
        
        else:
            logging.debug(f"FAIL - host {self.ip} have no ping response.")
            return False
