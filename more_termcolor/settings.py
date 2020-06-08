from more_termcolor.util import Singleton


class Settings(Singleton):
    def __init__(self):
        super().__init__()
        self.print = False
        self.debug = False


settings = Settings()
