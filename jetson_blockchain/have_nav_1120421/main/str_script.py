import csv
#from pymavlink import mavutil
import time

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

    """
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
        """ """txt專用
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
        """"""
        #csv專用
        with open('gps.csv', 'w', newline='') as gps_csvfile:
            writer = csv.writer(gps_csvfile)
            writer.writerow(['ID', 'Timestamp', 'gps_lat', 'gps_lng'])
            for _ in range(len(gps_time_stamp_list)):
                writer.writerow([str(_ + 1), gps_time_stamp_list[_], gps_lat_list[_], gps_lng_list[_]])
            gps_csvfile.close()
        with open('bat.csv', 'w', newline='') as bat_csvfile:
            writer = csv.writer(bat_csvfile)
            writer.writerow(['ID', 'Timestamp', 'bat_volt', 'bat_cur', 'bat_power'])
            for _ in range(len(bat_volt_list)):
                writer.writerow([str(_ + 1), bat_time_stamp_list[_], bat_volt_list[_], bat_cur_list[_], str(float(bat_cur_list[_]) * float(bat_cur_list[_]))])
            bat_csvfile.close()
        f.close()
        """"""
    
        master = mavutil.mavlink_connection('/dev/serial/by-id/usb-Holybro_Pixhawk6C_27009000551313133343532-if02',baud = 115200)

        while True:
            try:
                msg = master.recv_match(type='GPS_RAW_INT', blocking = True)
                battery = master.recv_match(type='SYS_STATUS, blocking', blocking = True)
                gps = 0
                with open('gps.csv', 'a', newline='') as gps_csvfile:
                    writer = csv.writer(gps_csvfile)
                    writer.writerow(['ID', 'Timestamp', 'gps_lat', 'gps_lng'])
                    if msg is not None:
                        lat = msg.lat / 1.0e7
                        lon = msg.lon / 1.0e7
                        print(f'Current GPS coordinates: Latitude={lat}, Longitude={lon}')
                        writer.writerow([str(gps + 1), str(time.ctime()), str(lng), str(lon)])
                    gps_csvfile.close()

                bat = 0
                with open('bat.csv', 'a', newline='') as bat_csvfile:
                    writer = csv.writer(bat_csvfile)
                    writer.writerow(['ID', 'Timestamp', 'bat_volt(V)', 'bat_cur(mA)', 'bat_power(%)'])
                    if battery is not None:
                        vol = battery.voltage_battery / 1.0e3
                        amp = battery.current_battery / 1.0e3
                        per = battery.battery_remain
                        print(f'Current Battery status: Voltage={vol} V, Ampere={amp} A,Percent={per}')
                        writer.writerow([str(bat + 1), str(time.ctime()), str(vol), str(amp), str(per)])
                    bat_csvfile.close()
                time.sleep(2)
            except:
                pass
            """
    
import csv
import time

def claw_v3(uav_pihawk): #最後server用

    data_list = list()
    gps_lat_list = list()
    gps_lng_list = list()
    bat_volt_list = list()
    bat_cur_list = list()
    bat_power_list = list()
    timestamp_list = list()

    uav_pihawk = 'lat:23.333,lon:121.3333,vol:15.22,amp:77.2,per:78'  #我是data
    time_stamp = time.strftime("%H:%M:%S", time.localtime())
    uav_data = 'time:' + str(time_stamp) + ',' + uav_pihawk

    data_content = uav_data.split(",")
    data_list.append(data_content)
    for i in range(len(data_content)):
        if("time:" in data_content[i]):
            timestamp = data_content[i].split("time:")[1]
            timestamp_list.append(timestamp)
        if("lat:" in data_content[i]):
            gps_lat = data_content[i].split("lat:")[1]
            gps_lat_list.append(gps_lat)
        if("lon:" in data_content[i]):
            gps_lng = data_content[i].split("lon:")[1]
            gps_lng_list.append(gps_lng)
        if("vol:" in data_content[i]):
            bat_volt = data_content[i].split("vol:")[1]
            bat_volt_list.append(bat_volt)
        if("amp:" in data_content[i]):
            bat_cur = data_content[i].split("amp:")[1]
            bat_cur_list.append(bat_cur)
        if("per:" in data_content[i]):
            bat_power = data_content[i].split("per:")[1]
            bat_power_list.append(bat_power)

    gps = 0 ##len(list) + 1
    with open('gps.csv', 'a', newline='') as gps_csvfile:
        writer = csv.writer(gps_csvfile)
        writer.writerow(['ID', 'Timestamp', 'gps_lat', 'gps_lng'])                  #先寫好一個csv，之後就直接加資料上去就好
        writer.writerow([str(gps + 1), str(timestamp), str(gps_lat), str(gps_lng)])
        gps_csvfile.close()
        
    bat = 0 ##len(list) + 1
    with open('bat.csv', 'a', newline='') as bat_csvfile:
        writer = csv.writer(bat_csvfile)
        writer.writerow(['ID', 'Timestamp', 'bat_volt(V)', 'bat_cur(mA)', 'bat_power(%)'])
        writer.writerow([str(bat + 1), str(timestamp), str(bat_volt), str(bat_cur), str(bat_power)])
        bat_csvfile.close()
        
def claw_v4(address): #最後server用

    with open(address, 'r', encoding='utf-8') as f:    #寫入txt用w，寫到最新行，之後再用a謝新資料進csv
        content = f.readlines()
        
        data_list = list()
        gps_lat_list = list()
        gps_lng_list = list()
        bat_volt_list = list()
        bat_cur_list = list()
        bat_power_list = list()
        timestamp_list = list()
        
        for _ in range(len(content)):
            data_content = content[_].split(",")
            data_list.append(data_content)

        for _ in range(len(content)):
            for i in range(len(data_content)):
                if("time:" in data_list[_][i]):
                    timestamp = data_list[_][i].split("time:")[1]
                    timestamp_list.append(timestamp)
                if("lat:" in data_list[_][i]):
                    gps_lat = data_list[_][i].split("lat:")[1]
                    gps_lat_list.append(gps_lat)
                if("lon:" in data_list[_][i]):
                    gps_lng = data_list[_][i].split("lon:")[1]
                    gps_lng_list.append(gps_lng)
                if("vol:" in data_list[_][i]):
                    bat_volt = data_list[_][i].split("vol:")[1]
                    bat_volt_list.append(bat_volt)
                if("amp:" in data_list[_][i]):
                    bat_cur = data_list[_][i].split("amp:")[1]
                    bat_cur_list.append(bat_cur)
                if("per:" in data_list[_][i]):
                    bat_power = data_list[_][i].split("per:")[1]
                    bat_power_list.append(bat_power[0:2])

        gps = 0 ##len(list) + 1
        with open('gps.csv', 'a', newline='') as gps_csvfile:
            writer = csv.writer(gps_csvfile)
            writer.writerow(['ID', 'Timestamp', 'gps_lat', 'gps_lng'])                  #先寫好一個csv，之後就直接加資料上去就好
            for _ in range(len(timestamp_list)): 
                writer.writerow([str(_ + 1), str(timestamp_list[_]), str(gps_lat_list[_]), str(gps_lng_list[_])])
            gps_csvfile.close()
            
        bat = 0 ##len(list) + 1
        with open('bat.csv', 'a', newline='') as bat_csvfile:
            writer = csv.writer(bat_csvfile)
            writer.writerow(['ID', 'Timestamp', 'bat_volt(V)', 'bat_cur(mA)', 'bat_power(%)'])
            for _ in range(len(timestamp_list)): 
                writer.writerow([str(_ + 1), str(timestamp_list[_]), str(bat_volt_list[_]), str(bat_cur_list[_]), str(bat_power_list[_])])
            bat_csvfile.close()
    f.close()

#claw_v2(claw_v1("name.txt")) #數枚派用

#name = "2023-03-30 15-{time}-50.bin.txt".format(time = time)

claw_v4('main/test.txt')
