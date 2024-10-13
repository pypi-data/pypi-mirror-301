from ..universal.get_subdict import get_subdict

class MyDict(dict):
    def __init__(self, d: dict = {}):
        super().__init__(d)

    def sub(self, prefix: str, splitter: str = "/"):
        return MyDict( get_subdict(self, prefix, splitter) )
        
    def __call__(self, prefix: str, splitter: str = "/"):
        return self.sub(prefix, splitter)
