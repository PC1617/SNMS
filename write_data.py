import sounddevice as sd
import numpy as np
from os import system
from time import sleep

from threading import Condition,Thread

###########################################################
#influx
from datetime import datetime
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



# You can generate a Token from the "Tokens Tab" in the UI
token = "OaUUKLPah7ISItDYY78HGIIImMe9-NPyX6AYS7yctOTEadbS3VCPAZuggwPsgjDSk9JWDmht2kjzhPaMh4ZIxA=="
org = "SSIPMT"
bucket = "Pro-tik"
client = InfluxDBClient(url="http://localhost:8086", token=token , org=org)

##########################################################
check_flag=0
volume_norm=0.0
Threshold=20

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def check(faltu):
    global volume_norm
    global check_flag
    global Threshold

    check_flag=1
    sec_flag=0

    for _ in range(10):
        if volume_norm>Threshold:
            sleep(0.1)
        else:
            sec_flag=1
    if sec_flag==1:
        print("Shut up")
        # else:
        #     print("SHut Up")
    check_flag=0

def print_sound(indata, outdata, frames, time, status):
    n=0
    global volume_norm
    global check_flag
    volume_norm = np.linalg.norm(indata)*10
    # print ("|" * int(volume_norm))

    if ((volume_norm>Threshold) and (check_flag==0)):
        print(check_flag,"Idar Dekho Idhar")
        #ts=time.time()
        #n+=1
        Thread(target = check,args=([n])).start()

    print("DB: ",volume_norm)
    
    p = influxdb_client.Point("my_data").tag("DB","db2").field("VolumeNorm", volume_norm)
    write_api.write(bucket=bucket, org=org, record=p)
    sleep(0.1)

    #_ = system('cls')

with sd.Stream(callback=print_sound):
    sd.sleep(-1)