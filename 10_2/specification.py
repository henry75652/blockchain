from block import Block, Information
from blockchain import Blockchain

#return {"tag":tag,"content":content}
#tag:
#   block
#   cmd

# block//56\Mon Feb 21 14:29:13 2022\177\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\Hello\0.0.0.0//appendix//test

def specification(sMsg):
    lMsg = sMsg.split("||") #有東西(block)//區塊(id/timestamp...)
    if(len(lMsg) > 1):  #['block', '56\\Mon Feb 21 14:29:13 2022\\177\\00079bcd42436498efda60b225436ec25c8db797be85775b0271bbba4a776ddf\\Hello\\0.0.0.0']
        #進度 判斷是否有appendix
        if len(lMsg) >= 2 and lMsg[2] == "appendix":
            if len(lMsg) >= 3:
                appendix = lMsg[3]
            else:
                appendix = ""

        if(lMsg[0] == "block"):
            block = Block()
            if block.conv_str_to_block(lMsg[1]):
                #print("[specification]:type == block")
                return {"tag":"block","content":block,"appendix":appendix}
            else:
                return False
        elif(lMsg[0] == "update"):
            block = Block()
            if block.conv_str_to_block(lMsg[1]):
                #print("[specification]:type == update")
                return {"tag":"update","content":block,"appendix":appendix}
            else:
                return False
        elif(lMsg[0] == "stop"):
            return {"tag":"stop","content":lMsg[1],"appendix":appendix}
        else:return lMsg

    else:return {"tag":"cmd","content":sMsg,"appendix":"test this is cmd"}

if __name__ == "__main__":
    msg = input()
    print(specification(msg))
