class RoutineData:
    def __init__(self, config) -> None:
        self.config = config['config']
        self.files = config['files']
        self.metrics = {}

    def getParams(self):
        return self.config
    
    def publishMetric(self, key, val):
        self.metrics[key] = val

    def publishFile(self, file):
        self.files.append(file)
    
    def getPayload(self):
        return {
            "metrics": self.metrics,
            "files": self.files,
        }