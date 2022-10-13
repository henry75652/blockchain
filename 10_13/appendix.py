
def finish_time(appendix):

    if("finish_time:" in appendix):
        print("[appendix.finish_time]finish_time is in appendix")
        appendix = appendix.split("\\")
        for _ in appendix:
            if("finish_time:" in _):
                appendix = _.split("finish_time:")[1]
                break
        print("[appendix.finish_time]finish_time = ",appendix)
        return appendix
    else:
        print("[appendix.finish_time]finish_time is not in appendix")

def miner(appendix):

    if("miner:" in appendix):
        print("[appendix.miner]miner is in appendix")
        appendix = appendix.split("\\")
        for _ in appendix:
            if("miner:" in _):
                appendix = _.split("miner:")[1]
                break
        print("[appendix.miner]miner = ",appendix)
        return appendix
    else:
        print("[appendix.miner]miner is not in appendix")

def verification(appendix):

    if("verification:" in appendix):
        print("[appendix.verification]verification is in appendix")
        appendix = appendix.split("\\")
        for _ in appendix:
            if("verification:" in _):
                appendix = _.split("verification:")[1]
                break
        print("[appendix.verification]verification = ",appendix)
        return appendix
    else:
        print("[appendix.verification]verification is not in appendix")

class commitment_cal():
    def __init__(self,data = (0,0,0,0,0,0,0,0,0)):
        self.data = data
        #print("init data = ",self.data)
        arr = list()
        arr.append(self.data)

    def getobj(self):
        return self
    
    def to_string(self):
        return str(self.data)
    def to_obj(self,string):
        #print("para in:",string)

        return string
    
    def sequence(self,string):
            #print("[go_fuck_yourself.go_fuck]======================")
            #print("[go_fuck_yourself.go_fuck]string:",string)
            if("commitment:" in string):
                #print("fuck: is in string")
                string = string.split("commitment:")
                #print(string)
                #print(string[1])    #[(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)]
                string = string[1].replace("[","").replace("]","")
                #print(string)   #(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)
                string = string.replace("(","")
                #print(string)
                string = string.split(")")
                string = string[0:-1]
                #print(string)   #['9, 8, 7, 6, 5, 4, 3, 2, 1', '1, 2, 3, 4, 5, 6, 7, 8, 1', '']
                data = list()
                for _ in string:
                    temp = _.split(",")
                    row = list()
                    for x in temp:
                        try:
                            row.append(int(x))
                        except:
                            x = x.replace(" '","").replace("'","")
                            row.append(x)
                            pass 
                    #print(temp)
                    data.append(row)
                #print("[go_fuck]",data)
                return data
            else:
                pass
                #print("fuck: is not in string")
            #print("[go_fuck_yourself.go_fuck]======================")
            
    def sequence_info(self,string):
            string = string.replace("[","").replace("]","")
            data = list()
            string = string.split(",")
            for _ in string:
                data.append(int(_))
            return data

if __name__ == "__main__":
    print("this is program is not for running directly")