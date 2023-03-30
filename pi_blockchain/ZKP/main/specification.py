from block import Block, Information
from blockchain import Blockchain
from appendix import zkp_parameter

#return {"tag":tag,"content":content}
#tag:
#   block
#   cmd

# block//56\Mon Feb 21 14:29:13 2022\177\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\Hello\0.0.0.0//appendix//test

def specification(sMsg):
    #print("(debug)[specification]sMsg:",sMsg)
    if(type(sMsg) != str): return False
    lMsg = sMsg.split("||") #有東西(block)//區塊(id/timestamp...)
    #print("(debug)[specification]len = ",len(lMsg),"lMsg =",lMsg)
    if(len(lMsg) > 1):  #['block', '56\\Mon Feb 21 14:29:13 2022\\177\\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\\Hello\\0.0.0.0']
        #判斷是否有appendix
        if len(lMsg) >= 3:
            if lMsg[2] == "appendix":
                if len(lMsg) >= 3:
                    appendix = lMsg[3]
                else:
                    appendix = ""

        if(lMsg[0] == "block"):
            block = Block()
            nonce = zkp_parameter(appendix)
            if block.conv_str_to_block(lMsg[1],nonce):
                #print("[specification]:type == block")
                return {"tag":"block","content":block.conv_str_to_block(lMsg[1],nonce),"appendix":appendix}
            else:
                return False
        elif(lMsg[0] == "update"):
            block = Block()
            nonce = zkp_parameter(appendix)
            if block.conv_str_to_block(lMsg[1],nonce):
                #print("[specification]:type == update")
                return {"tag":"update","content":block.conv_str_to_block_zpk(lMsg[1],nonce),"appendix":appendix}
            else:
                return False
        elif(lMsg[0] == "ledge"):
            block = Block()
            nonce = zkp_parameter(appendix)
            print("(debug)[specification._nonce]",nonce)
            if block.conv_str_to_block(lMsg[1],nonce):
                #print("[specification]:type == update")
                #print("(debug)[specification.elif ledge]")
                #print("\t",sep="",end="")
                #block.print_block()
                return {"tag":"ledge","content":block.conv_str_to_block(lMsg[1],nonce),"appendix":appendix}
            else:
                return False
        elif(lMsg[0] == "data"):
            return {"tag":"data","content":lMsg[1],"appendix":appendix}


        #else:return lMsg
        else:return False

    else:return {"tag":"cmd","content":sMsg,"appendix":"test this is cmd"}

if __name__ == "__main__":
    msg = input()
    print(specification(msg))