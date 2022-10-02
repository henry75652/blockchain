def claw_v2(address,node_num = 2): #之後node數決定
    with open(address) as f:
        content = f.readlines()
        #print(content)
        #print(len(content))
        
        fast_time = list()
        
        id_comparison = list()
        for _ in range(len(content)): #直接拉block.id
            if("id:" in content[_]):
                id_content = content[_].split("\n")
                for i in id_content:
                    if("id:" in i):
                        id_num = i.split("id:")[1]
                        id_comparison.append(id_num)
                        
        id_list = list()
        for a in range(len(id_comparison)):
            id_num = int(id_comparison[a])
            id_list.append(id_num)
        #print("id_list",id_list)
        id_num = max(id_list)
        #print("id_num",id_num)
        
        column, row = int(id_num), node_num
        array2D = [[0 for _ in range(row)] for _ in range(column)]
        #print("array2D",array2D)
        #print("len_test4",len(array2D))
        
        for i in range(len(array2D)):
            fast_time = list()
            fast_miner = list()
            start_flag = True
            end_flag = True
            for _ in range(len(content)):
                if("id:" in content[_]):
                    id_content = content[_].split("\n")
                    for a in id_content:
                        if("id:" in a):
                            id_num = a.split("id:")[1]
                            #print("i",i)
                            #print("id_num",id_num)
                    if (start_flag and (int(id_num) == (i+1))):
                        start_line = _
                        print("start_line",start_line)
                        start_flag = False
                    if (end_flag and (int(id_num)) == (i+2)):
                        end_line = _
                        print("end_line",end_line)
                        end_flag = False
                        for b in range(start_line, end_line):
                            if("finish_time:" in content[b]):
                                #print("in")
                                time_content = content[b].split("\n")
                                for c in time_content:
                                    if("finish_time:" in c):
                                        time = c.split("finish_time:")[1]
                                        fast_time.append(time)
                                min_time = min(fast_time)
                            if("miner:" in content[b]):
                                miner_content = content[b].split("\n")
                                for c in miner_content:
                                    if("miner:" in c):
                                        miner = c.split("miner:")[1]
                                        fast_miner.append(miner)
                        array2D[i][0] = min_time
                        for c in range(len(fast_time)):
                            if min_time == fast_time[c]:
                                min_miner = fast_miner[c]
                                array2D[i][1] = min_miner
                        #print("fast_miner_1",fast_miner)
                        #print("fast_time_1",fast_time)

        for b in range(start_line, len(content)):
            if("finish_time:" in content[b]):
                #print("in")
                time_content = content[b].split("\n")
                for c in time_content:
                    if("finish_time:" in c):
                        time = c.split("finish_time:")[1]
                        fast_time.append(time)
                min_time = min(fast_time)
            if("miner:" in content[b]):
                miner_content = content[b].split("\n")
                for c in miner_content:
                    if("miner:" in c):
                        miner = c.split("miner:")[1]
                        fast_miner.append(miner)
        array2D[i][0] = min_time
        for c in range(len(fast_time)):
            if min_time == fast_time[c]:
                min_miner = fast_miner[c]
                array2D[i][1] = min_miner
        print("fast_miner_2",fast_miner)
        print("fast_time_2",fast_time)
        print("array2D",array2D)
        
        msg = str()
        for i in range(len(array2D)):
            msg += "=============\n"+  \
            "id:"+ str(i+1) +   \
            "\ntimestamp:"+array2D[i][0]+ \
            "\nminer:"+array2D[i][1]+ \
            "\n============="
            
        f_1 = open("log.txt",'a')
        f_1.write(msg)
        f_1.close()
            
        f.close()

"""
def claw(address):
    with open(address) as f:
        content = f.readlines()
        print(content)
        print(len(content))
        
        for _ in range(len(content)): #直接拉block.id
            if("id:" in content[_]):
                id_content = content[_].split("\n")
                for i in id_content:
                    if("id:" in i):
                        id_num = i.split("id:")[1]
        print("test_value",id_num)
        #print("test",type(id_num))
        
        fast_time = list()
        for _ in range(len(content)): 
            if("finish_time:" in content[_]):
                time_content = content[_].split("\n")
                for i in time_content:
                    if("finish_time:" in i):
                        time = i.split("finish_time:")[1]
                        fast_time.append(time)
        print("test2",fast_time)
        
        num_list = list()
        for a in range(len(fast_time)):
            num = float(fast_time[a])
            num_list.append(num)
        print("test3",num_list)
        min_num = min(num_list)
        print("test3",min_num)
        
        fast_miner = list()
        for _ in range(len(content)): 
            if("miner:" in content[_]):
                miner_content = content[_].split("\n")
                for i in miner_content:
                    if("miner:" in i):
                        miner = i.split("miner:")[1]
                        fast_miner.append(miner)
        print("test2",fast_miner)
        
        for i in range(len(num_list)):
            if min_num == num_list[i]:
                min_miner = fast_miner[i]
                print("min_node",min_miner)
        msg = str()
        msg += "=============\n"+  \
        "id:"+id_num+   \
        "\ntimestamp:"+str(min_num)+ \
        "\nminer:"+min_miner+ \
        "\n============="
            
        f_1 = open("log.txt",'a')
        f_1.write(msg)
        f_1.close()
            
        f.close()
"""

claw_v2("word.txt")
