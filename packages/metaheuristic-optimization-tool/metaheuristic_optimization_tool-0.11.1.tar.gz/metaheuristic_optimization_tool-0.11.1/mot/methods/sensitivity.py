import numpy as np
import os
from .method import Method
import uuid
import multiprocessing as mp

class sensitivity(Method):
    name = "Sensitivity"
    def __init__(self):
        Method.__init__(self)


    def search(self, Sampler, Fitter, workdir='./',
               n=30, record=True, default_vals=''):
        self.Fitter = Fitter
        self.file_name = os.path.join(workdir, 'sensitivity.csv')
        self.Sampler = Sampler
        self.n_per_gen = n
        self.n_vars = len(self.Sampler.v_min)
        self.avg_values = [(x+y)/2 for x, y in zip(self.Sampler.v_min, self.Sampler.v_max)]
        
        if default_vals != '':
            # check validity
            try:
                if len(list(default_vals)) != self.n_vars:
                    raise ValueError()
            except:
                raise ValueError('The default values you put in should be a list with length equal to the number of variables')
            self.avg_values = default_vals

        try:
            metric_list = [x.name for x in Fitter.function]
        except:
            metric_list = list(range(len(self.Fitter.function)))

        input_list = Sampler.v_label
        self.iter_n = 0
        column_header = ['Sample', 'Uniqid'] + list(input_list) + list(metric_list)

        for indx, variable in enumerate(self.Sampler.v_label):
            filename = variable+'.csv'
            with open(filename, 'w') as outcsv:
                outcsv.write(','.join(column_header))
                outcsv.write('\n')
            self.vv = variable
            Fitter.normalize_weight()

            self.lb = Sampler.v_min
            self.ub = Sampler.v_max

            self.var_len = len(input_list)
            self.obj_len = len(metric_list)
            with mp.Pool(mp.cpu_count()) as p:
                p.map(self.go, list(range(n)))


    def go(self, i):
        uniq_id = str(uuid.uuid4())
        var_new = self.Sampler.random()
        for j in range(len(var_new)):
            if j != self.Sampler.v_label.index(self.vv):
                var_new[j] = self.avg_values[j]
            else:
                var_new[j] = np.linspace(self.Sampler.v_min[j], self.Sampler.v_max[j], self.n_per_gen)[i]
        metric_new, fitness_new = self.Fitter.evaluate(var_new, uniq_id)
        row = [i, uniq_id] + var_new + list(metric_new)
        row = [str(x) for x in row]
        with open(self.vv+'.csv', 'a') as f:
            f.write(','.join(row))
            f.write('\n')