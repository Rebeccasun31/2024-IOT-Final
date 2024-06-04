import time, random
import DAN
from detecter import human_detecter, fall_detecter

ServerURL = 'https://2.iottalk.tw'
Reg_addr = str(random.randint(100, 300)) # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control',]
DAN.profile['d_name']= Reg_addr + '.Dummy_Device'

DAN.device_registration_with_retry(ServerURL, Reg_addr)

human_detected = False
fall_detected = 0

while True:
    try:
        if not human_detected:
            human_detected = human_detecter()   # First, try to detect human
        else:
            if fall_detecter():                 # Then, detect falling
                fall_detected += 1              # Count falling times to avoid error detection

            print(fall_detected)
            if fall_detected >= 10:
                DAN.push ('Dummy_Sensor', 'FALL DETECTED!!!') # Push warning message
                print('FALL DETECTED!!!')
                fall_detected = 0

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)   
            DAN.deregister()
            exit()

    time.sleep(0.2)

