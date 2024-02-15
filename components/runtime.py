class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None
        
    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self
    
    def __repr__(self) -> str:
        return f"<RunTimeResult:{self.value}:{self.error}>"