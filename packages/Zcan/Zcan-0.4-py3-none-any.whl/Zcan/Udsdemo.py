#from zhangzhao

from can import BusABC,Message
from Zcan import canMonitor
import copy
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import platform
from ctypes import *
import time
import re


class udsdemo():
    '''
    uds demo
    '''
    def __init__(self,id,id1,bus:BusABC,dll:str = "./key.dll",channel = 42):
        self.bus = bus 
        self.id = id
        self.id1 = id1
        self.dll = dll
        self.monitor = canMonitor(self.bus)
        self.start = True
        self.message = Message(
            timestamp=0,
            is_remote_frame=False,
            is_extended_id=True,
            is_error_frame=False,
            arbitration_id=self.id,
            dlc=8,
            data=[0]*8,
            channel = self.bus.channel
        )
        if platform.system() == "Windows":
            self.__dll = windll.LoadLibrary("./key.dll")
        else:
            self.__dll = CDLL('./test.so')
        if self.__dll == None:
            print("seedkeyDLL couldn't be loaded!")

    def session_control(self,sub) -> bool:
        message = copy.deepcopy(self.message)
        message.data[0] = 0x02
        message.data[1] = 0x10
        message.data[2] = sub
        self.bus.send(message)
        msg = self.monitor.monitor_one_event_message(self.id1)
        if(msg.data[1] == 0x50 and msg.data[2] == sub):
            return True
        return False
    
    def read_by_DID(self,DID:int = 0xF101)->Tuple[bool,List]:
        Eol_list = []
        message = copy.deepcopy(self.message)
        str_did = hex(DID)[2:]
        len_str_did = len(str_did)//2
        data1 = str_did[:len_str_did]
        data2 = str_did[len_str_did:]
        message.data[0] = 0x03
        message.data[1] = 0x22
        message.data[2] = int(data1,16)
        message.data[3] = int(data2,16)
        self.bus.send(message)
        print(message)
        msg = self.monitor.monitor_one_event_message(self.id1)
        print(msg)
        if msg.data[0] == 0x10:
            len1 = msg.data[1]
            if (len1-6)%7:
                ff_num = (len1-6)//7 +1
                reminder = (len1-6)%7
            else:
                ff_num = (len1-6)//7 
               
            for i in range(3):
                Eol_list.append(msg.data[i+5])
            FC_msg = copy.deepcopy(self.message)
            FC_msg.data[0] = 0x30
            self.bus.send(FC_msg)
            for i in range(ff_num):
                msg = self.monitor.monitor_one_event_message(self.id1)
                print(msg)
                for i in range(7):
                    Eol_list.append(msg.data[i+1])
                    if len(Eol_list) == len1 -3:
                        break                                         
            return True,Eol_list
        elif msg.data[0] != 0x10 and msg.data[1] == 0x62:
            len2 = msg.data[0]
            len2 = len2 - 3
            for i in range(len2):
                Eol_list.append(msg.data[i+5])
            return True,Eol_list
        else:

            return False,Eol_list
        

    def write_by_DID(self,eol_list:List[int],DID:int = 0xF101)->bool:
        eol_len = len(eol_list)
        ret = self.session_control(0x03)
        if ret:
            time.sleep(0.05)
            ret = self.security_access()
            time.sleep(0.05)
            if ret:
                if eol_len < 5:
                    message = copy.deepcopy(self.message)
                    message.data[0] = 3 + eol_len
                    message.data[1] = 0x2E
                    str_did = hex(DID)[2:]
                    len_str_did = len(str_did)//2
                    data1 = str_did[:len_str_did]
                    data2 = str_did[len_str_did:]
                    message.data[2] = int(data1,16)
                    message.data[3] = int(data2,16)
                    for i in range(eol_len):
                        message.data[i+4] = eol_len[i]
                    self.bus.send(message)
                    msg_fb = self.monitor.monitor_one_event_message(self.id1)
                    if msg_fb.data[1] == 0x6E:
                        return True          
                else:
                    message = copy.deepcopy(self.message)
                    
                    data_len = 3 + eol_len
                    if (eol_len-3)%7 and eol_len-3 > 7:
                        ff_num = (eol_len-3)//7 +1
                        reminder = (eol_len-3)%7
                    elif (eol_len-3)%7 and eol_len-3 < 7:
                        ff_num = 1
                    else:
                        ff_num = (eol_len-3)//7
                    print(ff_num)
                    ff_list = []
                    message.data[0] = 0x10
                    message.data[1] = data_len
                    str_did = hex(DID)[2:]
                    len_str_did = len(str_did)//2
                    data1 = str_did[:len_str_did]
                    data2 = str_did[len_str_did:]
                    message.data[2] = 0x2E
                    message.data[3] = int(data1,16)
                    message.data[4] = int(data2,16)
                    for i in range(3):
                        message.data[i+5] = eol_list[i]
                    self.bus.send(message)
                    print(message)
                    for i in range(ff_num):
                        temp = copy.deepcopy(self.message)

                        for j in range(7):
                            temp.data[0] = 0x21 + i
                            temp.data[j+1] = eol_list[3+7*i+j]

                            if 3+7*i+j == eol_len -1:
                                break
                        ff_list.append(temp)
                    msg_fb = self.monitor.monitor_one_event_message(self.id1)
                    print(msg_fb)
                    if msg_fb.data[0] == 0x30:
                        for i in range(ff_num):
                            self.bus.send(ff_list[i])
                            time.sleep(0.05)
                            print(ff_list[i])
                        msg_fb = self.monitor.monitor_one_event_message(self.id1)
                        print(msg_fb)
                        if msg_fb != None and msg_fb.data[0]==0x03 and msg_fb.data[1] == 0x6E:
                            time.sleep(3)
                            self.ecu_reset()
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        else:
            return False


        

    def test_present(self):
        '''
        周期性任务，需要放在子线程里面
        '''
        message = copy.deepcopy(self.message)
        while(self.start):
            message.data[0] = 0x02
            message.data[1] = 0x3E
            message.data[2] = 0x80
            self.bus.send(message)
            time.sleep(2)
        

    def clear_DTC(self,sub:int = 0xFFFFFF):
        message = copy.deepcopy(self.message)
        message.data[0] = 0x04
        message.data[1] = 0x14
        str_sub = hex(sub)[2:]
        data_sub =  re.findall(r'.{2}', str_sub)
        for i, data1 in enumerate(data_sub):
            message.data[i+2] = int(data1,16)
        self.bus.send(message)
        msg_fd = self.monitor.monitor_one_event_message(self.id1)
        if msg_fd.data[1] == 0x54:
            return True
        else:
            return False



    def read_DTC(self,sub:int = 0x02,mask:int =0x01):
        DTC_list = []
        message = copy.deepcopy(self.message)
        message.data[0] = 0x03
        message.data[1] = 0x19
        message.data[2] = sub
        message.data[3] = mask
        self.bus.send(message)
        msg = self.monitor.monitor_one_event_message(self.id1)
        if msg.data[0] == 0x10:
            len1 = msg.data[1]

            if (len1-6)%7:
                ff_num = (len1-6)//7 +1
                reminder = (len1-6)%7
            else:
                ff_num = (len1-6)//7 
                
            for i in range(4):
                DTC_list.append(msg.data[i+4])
            FC_msg = copy.deepcopy(self.message)
            FC_msg.data[0] = 0x30
            self.bus.send(FC_msg)
            print(FC_msg)
            print(ff_num,len1)
            for i in range(ff_num):
                msg = self.monitor.monitor_one_event_message(self.id1)
                print(msg)
                for i in range(7):
                    DTC_list.append(msg.data[i+1])
                    if len(DTC_list) == len1 -2:
                        break                                         
            return True,DTC_list
        elif msg.data[0] != 0x10 and msg.data[1] == 0x69:
            len2 = msg.data[0]
            len2 = len2 - 2
            for i in range(len2):
                DTC_list.append(msg.data[i+5]) 
            return True,DTC_list
        else:

            return False,DTC_list




    def ecu_reset(self) -> bool:
        message = copy.deepcopy(self.message)
        message.data[0] = 0x02
        message.data[1] = 0x11
        message.data[2] = 0x03
        self.bus.send(message)
        msg_fd = self.monitor.monitor_one_event_message(self.id1)
        if msg_fd.data[1] == 0x51 and msg_fd.data[2] == 0x03:
            return True
        else:
            return False
        

    def security_access(self)->bool:
        if self.__dll == None:
            print("seedkeyDLL couldn't be loaded!")
            return False
        seedlsit = [0]*4
        keylist = [0]*4
        keylen = c_ubyte()
            
        c_array_seed = (c_ubyte * 4)()
        c_array_key = (c_ubyte * 4)()
        for i, val in enumerate(keylist):  
            c_array_key[i] = val  
        seed = (c_ubyte*4)(0xe1,0x20,0xbc,0x5f)
        key = (c_ubyte*4)(0)
        keylen = c_ubyte(0)

        #c_array_key_ptr = cast(c_array_key, POINTER(c_int))  # type: ignore
        message = copy.deepcopy(self.message)
        message.data[0] = 0x02
        message.data[1] = 0x27
        message.data[2] = 0x01
        self.bus.send(message)
        msg = self.monitor.monitor_one_event_message(self.id1)
        #print(msg)
        if msg.data[1] == 0x67 and msg.data[2] == 0x01:
            for i in range(4):
                seedlsit[i] = msg.data[3+i]
            for i, val in enumerate(seedlsit):  
                c_array_seed[i] = val 
                seed[i] = val
            #print(c_array_seed_ptr,c_array_key_ptr,keylen_ptr)
            if platform.system() == "windows":
                ret = self.__dll.GenerateKgeneyEx(byref(c_array_seed),4,1,"one",byref(c_array_key),4,byref(keylen))
            else:
                self.__dll.GenerateKgeneyEx.argtypes = [POINTER(c_ubyte*4), c_ubyte,c_ubyte,c_char_p,POINTER(c_ubyte*4),c_ubyte,POINTER(c_ubyte)]
                self.__dll.GenerateKgeneyEx.restype = c_int
                ret = self.__dll.GenerateKgeneyEx(byref(seed),4,1,b'one',byref(key),4,byref(keylen))
            if ret:
                keymsg = message.__copy__()
                keymsg.data[0] = 0x06
                keymsg.data[1] = 0x27
                keymsg.data[2] = 0x02
                for i in range(4):
                    #keymsg.data[3+i] = c_array_key[i]
                    keymsg.data[3+i] = key[i]
                time.sleep(0.05)
                self.bus.send(keymsg)
                keymsg_fb = self.monitor.monitor_one_event_message(self.id1)
                if keymsg_fb .data[1] == 0x67 and keymsg_fb .data[2] == 0x02:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False






        
        
        



