#from zhangzhao

import can 
from can import BusABC
from can.io.generic import BaseIOHandler
from typing import (
    Any,
    Callable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import time

class Mcanplayer():

    '''
    离线回放器
    根据数据库文件解析出来每一个报文，生成回放队列
    
    '''
    def __init__(
        self,
        bus: BusABC,
        file,
        **kwargs,
    ):
        self.bus = bus
        self.src = can.ASCReader(file)
        self.message_tosend__queue = []
        self.channel = None
        self.get_message_queue()
        self.set_channel()

    def get_message_queue(self):
        if self.src == None:
            print("Exception on datareader!")
            raise 
        for msg in self.src:
            self.message_tosend__queue.append(msg)

    def set_channel(
            self,
            channel1: Any = None,
            channel2: Any = None,
    ):
        
        print(self.bus.channel)
        for num in range(len(self.message_tosend__queue)):
            self.message_tosend__queue[num].channel = self.bus.channel

    def start_fast(
            self,
            timeout = 0,
            mode = "once",
            times = 0
    ):
        '''
        输入1：控制每条报文的发送间隔
        输入2：发送模式,控制发送轮次
        输入3：整体循环次数


        '''
        for msg in self.message_tosend__queue:
            self.bus.send(msg)
            if(timeout != 0):
                time.sleep(timeout)
    
    def start_with_ts(self):
        '''
        根据每条报文的时间戳，精确控制报文发送间隔
        
        '''
        for num in range(len(self.message_tosend__queue)):
            if num < len(self.message_tosend__queue)-1:
                self.bus.send(self.message_tosend__queue[num])
                time1 = self.message_tosend__queue[num].timestamp
                time2 = self.message_tosend__queue[num+1].timestamp
                delay = time2-time1

                if(delay != 0):
                    time.sleep(delay)
            else:
                self.bus.send(self.message_tosend__queue[num])


                 

                
    