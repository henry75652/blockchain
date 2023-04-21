import msvcrt

class myNonBlockingInput():
    def __init__(self):
        self.buffer = str()
        self.ret = str()

    def ReceiveInput(self):
        if(msvcrt.kbhit()):
            self.buffer += msvcrt.getch().decode("utf-8")
        if(len(self.buffer) > 0 and self.buffer[-1] == '\r'):
            self.ret = self.buffer
            self.buffer = ""
            return self.ret
        else: return ""