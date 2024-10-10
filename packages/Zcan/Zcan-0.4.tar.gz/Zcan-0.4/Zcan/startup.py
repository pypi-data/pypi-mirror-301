import can
import subprocess

def start(channel:str,bitrate:str):
    subprocess.run(['sudo','ip','link','set',channel,'down'])
    subprocess.run(['sudo','ip','link','set',channel,'type','can','bitrate',bitrate])
    subprocess.run(['sudo','ip','link','set',channel,'up'])

    bus = can.interface.Bus(channel,interface ='socketcan')
    return bus
