class Singleton:
    _inst = None
    
    def __init__(self):
        # print(f'Singleton self.__class__:', self.__class__)
        # print(f'Singleton self.__class__.__class__:', self.__class__.__class__)
        if self.__class__._inst:
            return
        self.__class__._inst = self
    
    def __new__(cls, *args):
        if cls._inst:
            return cls._inst
        # print(f'Singleton cls:', cls)
        # print(f'Singleton cls.__class__:', cls.__class__)
        inst = super().__new__(cls)
        return inst


class Settings(Singleton):
    def __init__(self):
        super().__init__()
        self.print = False
        self.debug = False


settings = Settings()
