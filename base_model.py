from abc import ABC, abstractmethod
import gurobipy as gp
from gurobipy.gurobipy import StatusConstClass


class BaseModel(ABC):
    # 构造方法
    def __init__(self):
        self.m = None
        self.STATUS = dict()

    # 已经实现的普通方法
    def _create_solver(self, params: dict = None):
        self.m = gp.Model()

        for k, v in StatusConstClass.__dict__.items():
            if not k.startswith('__'):
                self.STATUS[v] = k

        if not params:
            return
        for param_name, new_val in params.items():
            self.m.setParam(param_name, new_val)

    @abstractmethod
    def _add_vars(self):
        pass

    @abstractmethod
    def _set_obj(self):
        pass

    @abstractmethod
    def _add_conss(self):
        pass

    def solve(self):
        self.m.optimize()
        return self.get_sol()

    def get_status(self):
        return self.STATUS[self.m.status]

    def get_sol(self):
        status = self.get_status()
        gap = self.m.MIPGap
        lb = self.m.ObjBoundC
        ub = self.m.ObjVal
        runtime = self.m.Runtime

        return {'gap': gap, 'status': status, 'lb': lb, 'ub': ub, 'runtime': runtime}

    def make_model(self, params: dict = None):
        self._create_solver(params)
        self._add_vars()
        self._add_conss()
        self._set_obj()
