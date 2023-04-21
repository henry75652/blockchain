
class DataParser():
    def __init__(self):
        self.FileName = "data.bin.txt"
    def Check(self):    #檢查內容 無的話回傳False有的話直接回傳list
        try:
            with open(self.FileName,"r") as f:
                ret = self.Parser(f.readlines())
                if ret == []: return False
                else: return ret
        except Exception as e:
            print("(exception)[DataParser.Check]e:",e)
    def Parser(self,listFileContext):
        try:
            ret = []
            for line in listFileContext:
                if(line[24:27] == "GPS"): ret.append(line)
            return ret
        except Exception as e:
            print("(exception)[DataParser.Parser]e:",e)
    def Clear(self):
        pass

if __name__ == "__main__":
    print("(Hello World)")
    data_parser = DataParser()
    ret = data_parser.Check()
    if(ret == False): print("no!")
    else:
        for x in ret:
            print(x)
            