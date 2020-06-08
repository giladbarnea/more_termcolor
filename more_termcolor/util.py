def confirm(prompt='continue?') -> bool:
    answer = input(f'{prompt} y/n/q\t').lower()
    if answer == 'q':
        import sys
        sys.exit()
    return answer == 'y' or answer == 'yes'


def spacyprint(*values):
    print('\n', *values, sep='\n', end='\n')


class Singleton(object):
    _inst = None
    
    def __init__(self):
        
        if self.__class__._inst:
            return
        self.__class__._inst = self
    
    def __new__(cls, *args):
        
        if cls._inst:
            return cls._inst
        inst = super().__new__(cls)
        return inst
