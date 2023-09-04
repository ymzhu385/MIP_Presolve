import numpy as np
from gurobipy import GRB

from base_model import BaseModel


class One(BaseModel):
    def __init__(self, c: np.ndarray):
        super().__init__()
        self.x = None
        self.c = c

    def _add_vars(self):
        self.x = self.m.addMVar(self.c.shape, vtype=GRB.BINARY, name="x")

    def _set_obj(self):
        self.m.setObjective((self.c * self.x).sum(), GRB.MINIMIZE)

    def _add_conss(self):
        for i in range(self.c.shape[0]):
            self.m.addConstr(self.x[i, :].sum() == 1)
        for j in range(self.c.shape[1]):
            self.m.addConstr(self.x[:, j].sum() <= 1)


if __name__ == '__main__':
    np.random.seed(0)
    m = One(np.random.random([20, 40]))
    # m.make_model({'OutputFlag': 1, 'TimeLimit': 15, 'MIPGap': 0})
    m.make_model()
    m.m.write('test.lp')
    print(m.solve())
