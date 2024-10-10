#from zhangzhao

from can.io.asc import ASCWriter
import threading
import datetime
from can import BusABC ,Message
#from can.io.generic import TextIOMessageReader
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

class canMonitor():

    _instance = None
    _bus = None


    def __init__(self,
                 bus:BusABC
                 
    ):
        
        '''

        监控器
        
        '''
        self.logflag = True
        self.bus = bus


    def __new__(cls,bus):
        if not cls._instance:
            instance = super(canMonitor, cls).__new__(cls)
            cls._instance = instance
            cls._bus = bus
        elif cls._bus is not bus:
            instance = super(canMonitor, cls).__new__(cls)
            cls._instance = instance
            cls._bus = bus


        return cls._instance
        

    def monitor_id_exc(self,
                       interface,
                       id:int = None,
                       
                       method:Any = None
                       
    ):
        '''
        输入1：报文id，默认无
        输入2：方法获函数
        从总线上获取一条报文，获取到后执行method
        
        '''
        
        recieved = False
        while(recieved == False):
            if interface == "neovi":
                msg = self.bus.recv(timeout = 0.1)
            else:
                msg = self.bus.recv()
            msg = self.bus.recv(timeout = 0.1)
            if msg != None:
                print(msg)
                if(msg.arbitration_id == id):
                    recieved = True
            #print("testing")
            #time.sleep(1)
        if method != None and recieved:
            method()

    def monitor_one_event_message(self,id,timeout:float = 1)-> Message:
        '''
        输入1：can报文ID

        从总线上以阻塞的方式获取一条事件报文、ID为id的报文，并返回该报文，需放在子线程里面使用！！！
        '''
        #msg = None
        recieved = False
        interface = self.bus.interface
        start = datetime.datetime.now().timestamp()
        while(recieved == False):
            end = datetime.datetime.now().timestamp()
            if interface == "neovi":
                msg = self.bus.recv(timeout = 0.1)
            else:
                msg = self.bus.recv()
            if msg != None and msg.arbitration_id == id:
                recieved = True
                return msg
            if end - start > timeout:
                return None
        return None      
    

    def monitor_one_period_message(self,id)-> Message:
        '''
        输入1：can报文ID

        从总线上以阻塞的方式获取一条周期报文、ID为id的报文，并返回该报文，需放在子线程里面使用！！！
        '''
        self.bus.Clear_rx_buffer()
        recieved = False
        interface = self.bus.interface
        while(recieved == False):
            if interface == "neovi":
                msg = self.bus.recv(timeout = 0.1)
            else:
                msg = self.bus.recv()
            if msg != None and msg.arbitration_id == id:
                recieved = True
                return msg
        return None   



    def start():
        pass

    
    def log_asc(self,file,timeout:float = None):
        writer = ASCWriter(file)
        start = datetime.datetime.now().timestamp()
        while self.logflag:
            end = datetime.datetime.now().timestamp()
            msg = self.bus.recv()
            writer.on_message_received(msg)
            if timeout is not None:
                if end - start >timeout:
                    return 



          

    def log_asc_thread(self,file,timeout:float = None):
        threading.Thread(target=(self.log_asc),args=(file,timeout,)).start()
        pass    

    def log_blf(self):
        pass
