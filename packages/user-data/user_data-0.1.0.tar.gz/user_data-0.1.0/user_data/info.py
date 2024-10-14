import platform

class SystemInfo:
    @staticmethod
    def get_os_name():
        """
        Returns the name of the operating system.
        """
        return platform.system()

    @staticmethod
    def get_os_version():
        """
        Returns the version of the operating system.
        """
        return platform.version()

    @staticmethod
    def get_machine_type():
        """
        Returns the machine type (e.g., x86_64).
        """
        return platform.machine()

    @staticmethod
    def get_processor():
        """
        Returns the processor name.
        """
        return platform.processor()