class RequestContext:
    def __init__(self, data: dict, context: dict) -> None:
        self.data = data
        self.context = context