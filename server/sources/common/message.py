class Message:
    def __init__(self, perception: float, popularity: int, platform: str, content: str):
        self.perception: float = perception
        self.popularity: int = popularity
        self.platform: str = platform
        self.content: str = content