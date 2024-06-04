import time, random
import DAN

ServerURL = 'https://2.iottalk.tw'
Reg_addr = str(random.randint(100, 300)) # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control',]
DAN.profile['d_name']= Reg_addr + '.Dummy_Device'

DAN.device_registration_with_retry(ServerURL, Reg_addr)

while True:
    try:
        ODF_data = DAN.pull('Dummy_Control') # Pull data
        if ODF_data != None:
            print (ODF_data[0])

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

