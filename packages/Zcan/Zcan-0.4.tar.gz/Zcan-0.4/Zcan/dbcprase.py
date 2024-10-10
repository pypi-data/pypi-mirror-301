#from zhangzhao

from cantools.database.can.database import Database
import cantools
from can import BusABC ,Message
from collections import deque
import cantools.database.can.message as MS
from Zcan import canMonitor
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

#Zsingal = List[dict[str,Union[int,float]]]
codectpye = List[Dict[str,Union[int,str,List[int]]]] 

class _Mcan_messgae_after_dbcprase():
    singals:Dict[str,float] = {}
    def __init__(self) -> None:
        pass
    def add_singal(str:str,
                   value:float
    ):
        pass

class codec():
    #queue:List[tuple[str,int ,int,float,float]] = []
    #singal:tuple[str,int ,int,float,float]
    pass


class dbc_praser():

    '''
    DBC解析器
    需输入一个bus(类型为python-can标准BusABC)
    需输入一个dbc
    '''

    def __init__(self,
                 bus:BusABC,
                 dbc:str,
    

    ) -> None:
        self.bus = bus
        self.dbc = cantools.database.load_file(dbc)
        self.message = _Mcan_messgae_after_dbcprase()
        self.bitarray = []
        self.monitor = canMonitor(self.bus)
        self.currentid = 0





    def gen_bitarray(self,message:Message) ->list:

        '''
        输入message(类型为python-can标准meassge),
        解析message里面的数据域，转换成64位的bit信息，不够补0，
        每一个bit都单独存到list中，默认大端方式解析，小端方式暂未包含


        '''
        self.rawdata = message.data

        #print(self.rawdata)
        #self.dbc_ms = self.dbc.get_message_by_frame_id(id)
        for data in self.rawdata:
            bin_str = bin(data)[2:]
            bit_num = [0]*8
            if len(bin_str) < 8:
                for i in range(8 - len(bin_str)):
                    bit_num[7-i] = 0
                for i in range(len(bin_str)):
                    bit_num[len(bin_str)-1-i] = int(bin_str[i])
            else:
                for i in range(len(bin_str)):
                    bit_num[7-i] = int(bin_str[i])
          
            self.bitarray.extend(bit_num)
            
        #print(self.bitarray)
        return self.bitarray
    

    def gen_codec(self,message:MS) -> codectpye:
        '''
        输入一个message(类型为cantools标准message)，
        过滤生成一个解码器(类型codectpye)，里面包含某条报文的所有子信号的解析规则，包括起始位，长度，
        偏置跟增益等。
        
        '''
        self.currentid = message._frame_id
        sorted_signal:List[Dict[str,Union[int,str,List[int]]]] = []
        #sort_dict:Dict[str,Union[int|str]] = {}
        for singal in message._signals:
            sort_dict:Dict[str,Union[int,str,List[int]]] = {}
            sort_dict["name"] = singal.name
            sort_dict["startbit"] = singal.start
            sort_dict["order"] = singal.byte_order
            sort_dict["fator"] = singal.scale
            sort_dict["offset"] = singal.offset
            sort_dict["bitindex"] = []

            for i in range(singal.length):
                sort_dict["bitindex"].append(singal.start - i)
                #print(sort_dict["bitindex"])
            sort_dict["bitindex"].reverse()
            sorted_signal.append(sort_dict)
        #print(sort_signal)
        sorted_signal = sorted(sorted_signal,key=lambda x:x["startbit"])
        return sorted_signal


    def decode(self,id,name:str,tpye:str = "event") :
        '''
        输入1：can报文ID
        输入2：子信号名称

        从总线获取一条给定id的报文，并解析出其中子信号的值并返回
        
        
        '''
        msg = self.dbc.get_message_by_frame_id(id)
        codec = self.gen_codec(msg)
        if type == "event":
            msg = self.monitor.monitor_one_event_message(self.currentid)
        else:
            msg = self.monitor.monitor_one_period_message(self.currentid)
        self.gen_bitarray(msg)
        decode_info:List[dict[str,Union[int,float]]] = []
        for msg in codec:
            single_info:dict[str,Union[int,float]] = {}
            single_info["name"] = msg["name"]
            single_rawdata = 0
            fator = msg["fator"]
            offset = msg["offset"]
            for i in range(len(msg["bitindex"])):
                listdata = self.bitarray[msg["bitindex"][i]]
                if i == 0:
                    single_rawdata = single_rawdata + listdata
                else:
                    single_rawdata = single_rawdata + listdata*2**i
                
            single_decode = single_rawdata*fator + offset
            single_info["data"] = single_decode
            decode_info.append(single_info)
        for sg in decode_info:
            if sg["name"] == name:
                return sg["data"],decode_info

        return None,decode_info
            
            

        