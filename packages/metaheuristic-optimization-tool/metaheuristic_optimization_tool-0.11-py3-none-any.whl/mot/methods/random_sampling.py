import numpy as np
import os
from .method import Method
import uuid
import multiprocessing as mp

class random_sampling(Method):
    name = "Random sampling"
    def __init__(self):
        Method.__init__(self)

    # just for consistency, it is not actually searching for anything
    def search(self, Sampler, Fitter, workdir='./',
               n=100, record=True):
        self.Fitter = Fitter
        self.file_name = os.path.join(workdir, 'random_sampling.csv')
        self.Sampler = Sampler
        self.n_per_gen = n

        try:
            metric_list = [x.name for x in Fitter.function]
        except:
            metric_list = list(range(len(self.Fitter.function)))

        input_list = Sampler.v_label
        self.iter_n = 0
        column_header = ['Sample', 'Uniqid'] + list(input_list) + list(metric_list)
        self.f = open(self.file_name, 'w')
        self.f.write(','.join(column_header))
        self.f.write('\n')
        self.f.close()

        Fitter.normalize_weight()

        self.lb = Sampler.v_min
        self.ub = Sampler.v_max

        self.var_len = len(input_list)
        self.obj_len = len(metric_list)

        # start
        pool = mp.Pool(mp.cpu_count())
        self.s = Sampler
        self.f = Fitter
        pool.map(self.go, list(range(n)))
        # do = [pool.apply(self.go, args=(Sampler, Fitter, i)) for i in list(range(n))]
        pool.close()


    def go(self, i):
        uniq_id = str(uuid.uuid4())
        var_new = self.s.random()
        metric_new, fitness_new = self.f.evaluate(var_new, uniq_id)
        row = [i, uniq_id] + var_new + list(metric_new)
        row = [str(x) for x in row]
        with open(self.file_name, 'a') as f:
            f.write(','.join(row))
            f.write('\n')