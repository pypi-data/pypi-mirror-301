class AlreadyInjectedException(Exception):
    def __init__(self):
        super().__init__("Already injected")


class ProviderNotConfiguredException(Exception):
    def __init__(self):
        super().__init__("Provider configured")


class NotBoundedException(Exception):
    def __init__(self, cls_name):
        super().__init__(f"{cls_name} is not bounded")
