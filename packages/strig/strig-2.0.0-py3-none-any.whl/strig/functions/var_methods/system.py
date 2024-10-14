import getpass
import os
import platform
import socket


class SystemMethods:
    def system(self):
        return platform.system()

    def release(self):
        return platform.release()

    def version(self):
        return platform.version()

    def machine(self):
        """Returns the machine type, e.g., 'x86_64'."""
        return platform.machine()

    def processor(self):
        """Returns the processor name in lowercase and replaces spaces with dashes."""
        return platform.processor().lower().replace(" ", "-")

    def node(self):
        """Returns the network name of the machine."""
        return platform.node()

    def architecture(self):
        """Returns the architecture of the operating system, e.g., '64bit'."""
        return platform.architecture()[0]

    def user(self):
        """Returns the current logged-in user's name."""
        return getpass.getuser()

    def hostname(self):
        """Returns the hostname of the system."""
        return socket.gethostname()

    def ip_address(self):
        """Returns the IP address of the current machine."""
        return socket.gethostbyname(socket.gethostname())

    def os_name(self):
        """Returns the name of the operating system."""
        return os.name  # This returns 'posix', 'nt', etc., depending on the platform.
