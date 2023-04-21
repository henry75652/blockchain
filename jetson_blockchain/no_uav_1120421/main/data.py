from pymavlink import mavutil
import time

while True:
    try:
        msg = master.recv_match(type='GPS_RAW_INT', blocking = True)
        battery = master.recv_match(type='SYS_STATUS, blocking', blocking = True)
        if msg is not None:
            lat = msg.lat / 1.0e7
            lon = msg.lon / 1.0e7
            print(f'Current GPS coordinates: Latitude={lat}, Longitude={lon}')

        if battery is not None:
            vol = battery.voltage_battery / 1.0e3
            amp = battery.current_battery / 1.0e3
            per = battery.battery_remain
            print(f'Current Battery status: Voltage={vol} V, Ampere={amp} A,Percent={per}')
        time.sleep(2)
    except:
        pass