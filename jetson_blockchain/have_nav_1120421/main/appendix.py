import zero_knowledge_change

def zkp_parameter_product(info_dec):
    puzzle, presets = zero_knowledge_change.gen_sudoku_puzzle()
    solution = zero_knowledge_change.solve_sudoku_puzzle(puzzle)
    permutations = zero_knowledge_change.create_permutations()

    permuted_solution = zero_knowledge_change.puzzle_permute(solution, permutations)
    nonces = zero_knowledge_change.gen_nonces()
    commitment = zero_knowledge_change.puzzle_commitment(permuted_solution, nonces)

    sender_solution = []
    sender_solution_commitment = []
    
    random_nonce = info_dec

    for a in range(len(str(info_dec))):
        if random_nonce % 10 != 9:
            sender_solution_column = zero_knowledge_change.puzzle_columns(permuted_solution)[random_nonce % 10]
            sender_solution.append(sender_solution_column)
            sender_solution_commitment_column = zero_knowledge_change.puzzle_columns(commitment)[random_nonce % 10]
            sender_solution_commitment.append(sender_solution_commitment_column)
        else:
            sender_solution.append(tuple([9,9,9,9,9,9,9,9,9]))
            sender_solution_commitment.append(tuple(['9','9','9','9','9','9','9','9','9']))
        random_nonce = random_nonce // 10
    
    return sender_solution,sender_solution_commitment,nonces

def zkp_parameter(appendix):
    nonce = 0
    nonce_list = []
    for a in range(((len(commitment_cal().sequence(appendix))) -1)  // 2):    ###====###零知識
        flag_zkp = True
        flag_zkp_nine = False
        for _ in range(9):
            if commitment_cal().sequence(appendix)[a][_] == 9:
                pass
            else:
                break
            if _ == 8:
                flag_zkp_nine = True
        if (flag_zkp_nine):
            pass
        else:
            sudoku_verification = zero_knowledge_change.all_digits_exist_once(commitment_cal().sequence(appendix)[a])
            assert sudoku_verification == True
        sender_solution_nonce = zero_knowledge_change.puzzle_columns(commitment_cal().sequence(appendix)[-1])
        for _ in range(9):
            flag_zkp_count = False
            receiver_verification_commitment = zero_knowledge_change.puzzle_commitment(commitment_cal().sequence(appendix)[a], sender_solution_nonce[_])                                                       
            flag_zkp_nine_str = False
            for i in range(9):
                if commitment_cal().sequence(appendix)[a + (((len(commitment_cal().sequence(appendix))) -1)  // 2)][i] == '9':
                    pass
                else:
                    break
                if i == 8:
                    flag_zkp_nine_str = True
            if (flag_zkp_nine_str):
                nonce_list.append(9)
                flag_zkp = False
                break
            else:
                for b in range(9):
                    if commitment_cal().sequence(appendix)[a + (((len(commitment_cal().sequence(appendix))) -1)  // 2)][b] != receiver_verification_commitment[b]:
                        break
                    if b == 8:
                        flag_zkp_count = True
                if(flag_zkp_count):
                    nonce_list.append(_)
                    flag_zkp = False                    ###====###零知識
        if(flag_zkp):
            print("not pass verification_update")
            raise AssertionError
    
    for _ in range(len(nonce_list)):
        nonce = (nonce_list[len(nonce_list)-1-_] + (nonce * 10))

    return nonce


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
            if("commitment:" in string):
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
                return data
            else:
                pass
            
    def sequence_info(self,string):
            string = string.replace("[","").replace("]","")
            data = list()
            string = string.split(",")
            for _ in string:
                data.append(int(_))
            return data

if __name__ == "__main__":
    print("this is program is not for running directly")