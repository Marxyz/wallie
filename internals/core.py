import internals.system


class Application:
    def __init__(config, fetcher, recognizer):
        self.Commands = []

    def Invoke(self, commands):
        
        for command in commands:
            self.Commands[command.Name]()
                

