from system_executor import SysExecutor
from definition import *
from threading import Thread

from concurrent import futures


class SystemSimulator(object):
    __metaclass__ = SingletonType
    _engine = {}

    @staticmethod
    def register_engine(sim_name, sim_mode='VIRTUAL_TIME', time_step=1):
        SystemSimulator._engine[sim_name] = SysExecutor(
            time_step, sim_name, sim_mode)

    @staticmethod
    def remove_engine(sim_name):
        del SystemSimulator._engine[sim_name]

    @staticmethod
    def get_engine_map():
        return SystemSimulator._engine

    @staticmethod
    def get_engine(sim_name):
        return SystemSimulator._engine[sim_name]

    @staticmethod
    def is_terminated(sim_name):
        return SystemSimulator._engine[sim_name].is_terminated()

    @staticmethod
    def set_learning_module(sim_name, learn_module):
        SystemSimulator._engine[sim_name].set_learning_module(learn_module)
        pass

    @staticmethod
    def get_learning_module(sim_name):
        return SystemSimulator._engine[sim_name].get_learning_module()

    @staticmethod
    def is_terminated(sim_name):
        return SystemSimulator._engine[sim_name].is_terminated()

    @staticmethod
    def exec_non_block_simulate(sim_list, time = Infinite):
        for sim_name in sim_list:
            sim_inst = SystemSimulator._engine[sim_name]
            # p = Thread(target=sim_inst.simulate, args=(time,))
            # p.start()
            
            with futures.ThreadPoolExecutor() as executor:
                future = executor.submit(sim_inst.simulate, time)


    def __init__(self):
        pass