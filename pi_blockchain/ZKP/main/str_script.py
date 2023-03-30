def claw_v1(address):
    with open(address) as f:
        content = f.readlines()
        name_list = list()
        for _ in range(len(content)):
            name_content = content[_].split("\n")
            name_list.append(name_content)
    f.close()
    return(name_list[-2])

def claw_v2(address):
    with open(address) as f:
        content = f.readlines()
        #print(content)
        #print(len(content))
        gps_time_stamp_list = list()
        gps_list = list()
        gps_lat_list = list()
        gps_lng_list = list()
        bat_time_stamp_list = list()
        bat_list = list()
        bat_volt_list = list()
        bat_cur_list = list()
        for _ in range(len(content)): #直接拉block.id
            if("GPS {" in content[_]):
                gps_content = content[_].split("\n")
                gps_list.append(gps_content)
                for i in gps_content:
                    if("Lat :" in i):
                        gps_lat = i.split("Lat :")[1]
                        gps_lat_list.append(gps_lat[0:9])
                for j in gps_content:
                    if("Lng :" in j):
                        gps_lng = j.split("Lng :")[1]
                        gps_lng_list.append(gps_lng[0:10])
            if("BAT" in content[_]):
                bat_content = content[_].split("\n")
                bat_list.append(bat_content)
                for a in bat_content:
                    if("VoltR :" in a):
                        bat_volt = a.split("VoltR : ")[1]
                        bat_volt_list.append(bat_volt[0:10])
                for b in bat_content:
                    if("CurrTot :" in b):
                        bat_cur = b.split("CurrTot : ")[1]
                        bat_cur_list.append(bat_cur[0:7])
        for _ in range(len(gps_list)):
            gps_time_stamp_list.append(gps_list[_][0][0:16])
        for _ in range(len(bat_list)):
            bat_time_stamp_list.append(bat_list[_][0][0:16])
        print("=======================================================================================")
        #print("test",len(bat_time_stamp_list))
        #print("test",len(bat_volt_list))
        #print("test",bat_cur_list[3369])
        gps_msg = str()
        bat_msg = str()
        for _ in range(len(gps_time_stamp_list)):
            gps_msg += "=================\n"+  \
            "gps_id: "+ str(_ + 1) +   \
            "\ngps_timestamp: "+gps_time_stamp_list[_]+ \
            "\ngps_lat:"+gps_lat_list[_]+ \
            "\ngps_lng:"+gps_lng_list[_]+ \
            "\n================="
        #print("GPS",gps_msg)
        for _ in range(len(bat_volt_list)):
            #print("test",_)
            bat_msg += "=================\n"+  \
            "bat_id: "+ str(_ + 1) +   \
            "\nbat_timestamp: "+bat_time_stamp_list[_]+ \
            "\nbat_volt:"+bat_volt_list[_]+ \
            "\nbat_cur:"+bat_cur_list[_]+ \
            "\nbat_power:"+str(float(bat_cur_list[_]) * float(bat_cur_list[_]))+ \
            "\n================="
        #print("BAT",bat_msg)
        f_gps = open("gps_log.txt",'w')
        f_gps.write(gps_msg)
        f_bat = open("bat_log.txt",'w')
        f_bat.write(bat_msg)
        f.close()
        
#claw_v2(claw_v1("name.txt")) #數枚派用

#name = "2023-03-30 15-{time}-50.bin.txt".format(time = time)

claw_v2("2022-11-25 14-55-43.bin.txt")
