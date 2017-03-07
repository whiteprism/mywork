# -*- coding:utf-8 -*-
import Queue
import threading
import time

queue = Queue.Queue()
lock = threading.Lock()
class WorkManager(object):
    def __init__(self, thread_num=2):
        self.work_queue = queue
        self.threads = []
#         self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        """
        初始化线程
        """
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))
            
    def add_job(self, func, *args):
        """
        添加一项工作入队
        """
        #print 'add function is :',func
        self.work_queue.put((func, args))
# 
#     def wait_allcomplete(self):
#         """
#         等待所有线程运行完毕
#         """   
#         for item in self.threads:
#             if item.isAlive():
#                 item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，推出条件待定
        #print 'is runing:',self
        i = 0
        while True:
            try:
                lock.acquire()
                if self.work_queue.qsize():
                    do, args = self.work_queue.get(block=True)
                    lock.release()
                    #print args[0]
                    #print do
                    do(args[0])
                    self.work_queue.task_done()
                else:
#                     print self
                    time.sleep(1)
                    i+=1
                    if i == 10:
                        #print '线程池', self ,'工作正常'
                        i = 0
                    lock.release()
            except Exception,e:
                print str(e)

timer_threading = {}
timer_mutex = threading.Lock()

class Timer(threading.Thread):
    '''
    自定义轮寻定时
    '''
    def __init__(self, num):
        self._init_work_manager(num)
        threading.Thread.__init__(self)
        self.start()
    
    def _init_work_manager(self, num=2):
        self.work = WorkManager(num)
        
    def run(self):
        '''
        如果满足条件，添加到queue
        '''
        while True:
            timer_mutex.acquire()
            data_dic = timer_threading
            timer_mutex.release()
            now = time.time()
            if data_dic:
                for key, data in data_dic.items():
                    execution_time = data.keys()[0]
                    func_tuple = data.values()[0]
                    if now >= execution_time:
                        #print func_tuple
                        self.work.add_job(func_tuple[0], func_tuple[1])
                        if timer_threading.get(key, 0):
                            del timer_threading[key]
                            
                time.sleep(1)
            
    @classmethod
    def set_timer_func(cls, key, times, func, **args):
        '''
        增加定时函数
        '''
        timer_dic = {}
        now = time.time()
        execution_time = now + times
        timer_dic[execution_time] = (func, args)
        timer_threading[key] = timer_dic
        
    @classmethod
    def del_timer_func(cls, key):
        '''
        删除定时函数
        '''
        ret = 0
        timer_mutex.acquire()
        if timer_threading.get(key, 0):
            del timer_threading[key]
            ret = 1
        timer_mutex.release()
        return ret
#     work_manager =  WorkManager(10, 2)#或者work_manager =  WorkManager(10000, 20)
#     work_manager.wait_allcomplete()
