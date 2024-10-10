import numpy as np
import os
from math import floor
# from tabulate import tabulate
import multiprocessing as mp
from functools import partial
import signal
import uuid
import json


#==============================================================================
# PERTURBER
#==============================================================================

class Perturber():
    v_label = []
    v_unit  = []
    v_min   = []
    v_max   = []
    v_step  = []
    NV      = 0
    integer = []

    def __init__(self):
        self.v_label = []
        self.v_unit  = []
        self.v_min   = []
        self.v_max   = []
        self.v_step  = []
        self.NV      = 0
        self.integer = []

    def add_variable(self,v_label,v_min,v_max,unit="",integer=False):
        self.v_label.append(v_label)
        self.v_unit.append(unit)
        self.v_min.append(v_min)
        self.v_max.append(v_max)
        self.v_step.append(v_max-v_min)
        self.NV += 1
        self.integer.append(integer)

    def check_var(self,v):
        for i in range(self.NV):
            v[i] = min(v[i],self.v_max[i])
            v[i] = max(v[i],self.v_min[i])
            if self.integer[i]:
                v[i] = round(v[i])

    def perturb(self, v, frac):
        v_new = v[:]
        for i in range(self.NV):
            v_new[i] = v[i] + self.v_step[i] * frac * (np.random.uniform() - 0.5)
        self.check_var(v_new)
        return v_new

    def random(self):
        v_new = self.v_min[:]
        for i in range(self.NV):
            v_new[i] = v_new[i] + self.v_step[i] * np.random.uniform()
        self.check_var(v_new)
        return v_new
    
#==============================================================================
# FITTER
#==============================================================================

class Fitter():
    function   = []
    simulation = []
    weight     = []
    norm_min   = []
    norm_max   = []
    norm_step  = []
    limit_min  = []
    limit_max  = []
    limit_hard = [] # True: hard, False: penalty
    J          = 0  # Number of penalizing constraints
    NF         = 0

    def __init__(self):
        self.function   = []
        self.simulation = []
        self.weight     = []
        self.norm_min   = []
        self.norm_max   = []
        self.norm_step  = []
        self.limit_min  = []
        self.limit_max  = []
        self.limit_hard = [] # True: hard, False: penalty
        self.J          = 0  # Number of penalizing constraints
        self.NF         = 0

    def add_simulation(self, simulation):
        self.simulation.append(simulation)

    def add_function(self, f, weight = 1.0, 
                     limit_min = -float("inf"), limit_max = float("inf"), 
                     norm_min = 0.0, norm_max = 1.0,
                     limit_hard = True):
        self.function.append(f)
        self.weight.append(weight)
        self.limit_min.append(limit_min)
        self.limit_max.append(limit_max)
        self.norm_min.append(norm_min)
        self.norm_max.append(norm_max)
        self.norm_step.append(norm_max-norm_min)
        self.limit_hard.append(limit_hard)
        ## !!! this a bug since
        ## if (list object) is always true
        if not limit_hard: self.J = self.J + 1
        self.NF = self.NF + 1

    def violate_max(self,score,i):
        return ( (score - self.limit_max[i]) \
                 / (self.norm_max[i] - self.limit_max[i]) )
    
    def violate_min(self,score,i):
        return ( (self.limit_min[i] - score) \
                 / (self.limit_min[i] - self.norm_min[i]) )

    def evaluate(self,loc, uniq_id):
        # Run simulations
        for s in self.simulation:
            s(loc, uniq_id)

        val = []
        fit = 0.0
        vio_hard    = 0.0
        vio_penalty = 0.0
        for i in range(self.NF):
            score = self.function[i](uniq_id)
            val.append(score)
            # Compute violation
            if score >= self.limit_max[i]:
                if self.limit_hard[i]:
                    vio_hard = vio_hard - self.violate_max(score,i)
                else:
                    vio_penalty = vio_penalty - self.violate_max(score,i)
            elif score <= self.limit_min[i]:
                if self.limit_hard[i]:
                    vio_hard = vio_hard - self.violate_min(score,i)
                else:
                    vio_penalty = vio_penalty - self.violate_min(score,i)
            # Compute fitness
            fit = fit + (score - self.norm_min[i]) / (self.norm_step[i]) \
                        * self.weight[i]
        if vio_hard != 0.0: return val,vio_hard
        elif vio_penalty != 0.0: return val,fit*(1.0-vio_penalty/self.J)
        else: return val,fit

    def normalize_weight(self):
        tot = 0.0
        for w in self.weight:
            tot = tot + abs(w)
        for i in range(self.NF):
            self.weight[i] = self.weight[i]/tot


#==============================================================================
# METHOD
#==============================================================================

class Particle():
    loc          = []            # Location in serach space
    loc_best     = []            # Personal best location
    vel          = []            # Velocity
    metric        = []            # Current location metric by each function
    metric_best   = []            # Personal best metric
    fitness      = None          # Current location fitness
    fitness_best = -float("inf") # Personal best fitness
    ID           = None          # ID#

    def __init__(self,loc,vel):
        self.loc = loc[:]
        self.vel = vel[:]

class Method():
    name         = ""
    populational = False

    def __init__(self):
        # Optimum results
        self.var_best     = 0
        self.metric_best   = 0
        self.fitness_best = 0

        # Stored results
        self.var_stored     = []
        self.metric_stored   = []
        self.fitness_stored = []

    def record(self,g,Pbank,file_name,Perturber,Fitter):
        with open(file_name,"a") as f_out:
            if self.populational:
                for p,P in enumerate(Pbank, 1):
                    row = [g] + P.loc + P.metric + [P.fitness]
                    row = [str(x) for x in row]
                    f_out.write(','.join(row))
                    f_out.write('\n')
                return
            else:
                row = [g] + Pbank.loc + Pbank.metric + [Pbank.fitness]
                row = [str(x) for x in row]
                f_out.write(','.join(row))
                f_out.write('\n')
                return


    def store(self,Pbank):
        if self.populational:
            self.var_stored.append([P.loc[:]   for P in Pbank])
            self.metric_stored.append([P.metric[:] for P in Pbank])
            self.fitness_stored.append([P.fitness  for P in Pbank])
        else:
            self.var_stored.append(Pbank.loc[:])
            self.metric_stored.append(Pbank.metric[:])
            self.fitness_stored.append(Pbank.fitness)

    def report_start(self,print_out,file_name,report,record):
        if report: print(print_out)
        if record: 
            with open(file_name,"w") as f_out: f_out.write(print_out)

    def report_finish(self,file_name,Perturber,Fitter,report,record):
        print_out = "\n============\nFinal Report\n============\n"
        if report: print(print_out)
        if record: 
            with open(file_name,"a") as f_out: f_out.write(print_out)
        #Perturber.tabulate(self.var_best[:],file_name,report=report,
        #                   record=record)
        #Fitter.tabulate(self.metric_best[:],self.fitness_best,file_name,
        #                report=report,record=record)
 




class Sampler():
    v_label = []
    v_unit = []
    v_min = []
    v_max = []
    v_step = []
    v_dist_fcn = []
    v_fcn_args = []
    NV = 0

    dist_param_dict = {'beta': ['a', 'b'],
                       'binomial': ['n', 'p'],
                       'f': ['dfnum', 'dfden'],
                       'gamma': ['shape', 'scale'],
                       'logistic': ['loc', 'scale'],
                       'lognormal': ['mean', 'sigma'],
                       'poisson': ['lam'],
                       'rayleigh': ['scale'],
                       'standard_t': ['df'],
                       'weibull': ['a'],
                       'normal': ['loc', 'scale'],
                       'choice': ['a', 'p'],
                       'custom': ['pdf']
                       }

    def clear(self):
        self.v_label = []
        self.v_unit = []
        self.v_min = []
        self.v_max = []
        self.v_step = []
        self.v_dist_fcn = []
        self.v_fcn_args = []
        self.NV = 0

    def clear(self):
        self.v_label = []
        self.v_unit = []
        self.v_min = []
        self.v_max = []
        self.v_step = []
        self.v_dist_fcn = []
        self.v_fcn_args = []
        self.NV = 0

    def add_variable(self, v_label, v_min, v_max, unit='', dist_fcn='uniform',
                     **kwargs):

        self.v_label.append(v_label)
        self.v_unit.append(unit)
        self.v_min.append(v_min)
        self.v_max.append(v_max)
        self.v_step.append(v_max-v_min)
        self.NV += 1


        if dist_fcn == 'uniform':
            self.v_dist_fcn.append(np.random.uniform)
            self.v_fcn_args.append({'low':v_min, 'high': v_max})
        else:
            if dist_fcn not in self.dist_param_dict.keys():
                raise ValueError('Not a valid distribution function. Valid ones are:\n%s' %'\n'.join(dist_param_dict.keys()))
            fcn, arg_dict = self.check_kwargs(dist_fcn, kwargs)
            self.v_dist_fcn.append(fcn)
            self.v_fcn_args.append(arg_dict)


    def check_kwargs(self, dist_fcn, kwargs):
        arg_dict = {}
        for param in self.dist_param_dict[dist_fcn]:
            if param not in kwargs.keys():
                raise ValueError('To use distribution function "%s", you must have the following arguments:\n%s' %(dist_fcn, '\n'.join(self.dist_param_dict[dist_fcn])))
            else:
                arg_dict[param] = kwargs[param]
        if dist_fcn == 'custom':
            # check if it is the correct type of function
            if 'function' not in str(type(arg_dict['pdf'])):
                raise ValueError('For parameter `pdf`, you can only pass a python function object, that returns a probably density')
            arg_dict['i'] = self.NV-1
            return self.sample_custom, arg_dict
        else:
            return getattr(np.random, dist_fcn), arg_dict


    def in_between_indx(self, cum_p, v):
        for indx, val in enumerate(cum_p):
            if indx == len(cum_p):
                return indx
            else:
                if v > val and v < cum_p[indx+1]:
                    return indx

    def sample_custom(self, pdf, i):
        x = np.linspace(self.v_min[i], self.v_max[i], 1000)
        p = pdf(x)
        tot_p = sum(p)
        p = p / tot_p
        cum_p = np.cumsum(p)
        v = np.random.uniform()
        indx = self.in_between_indx(cum_p, v)
        return x[indx]


    def is_it_in(self, value, indx):
        print(value, self.v_max[indx], self.v_min[indx])
        if value < self.v_max[indx] and value > self.v_min[indx]:
            return True
        else:
            return False


    def random(self):
        np.random.seed()
        cnt = 0
        v_new = [0] * self.NV
        for i in range(self.NV):
            v_new[i] = self.v_dist_fcn[i](**self.v_fcn_args[i])
            # do it till it's in between min and max
            if not self.is_it_in(v_new[i], i):
                while not self.is_it_in(v_new[i], i):
                    v_new[i] = self.v_dist_fcn[i](**self.v_fcn_args[i])
                    cnt += 1
                    if cnt > 100: raise ValueError('Check your distribution and see if it is valid inside your min and max range')
        return v_new

    def perturb(self, v):
        v_new = v[:]
        for i in range(self.NV):
            v_new[i] = self.v_dist_fcn[i](**self.v_fcn_args[i])
            # do it till it's in between min and max
            if not self.is_it_in(v_new[i], i):
                while not self.is_it_in(v_new[i], i):
                    v_new[i] = self.v_dist_fcn[i](**self.v_fcn_args[i])
        return v_new[i]

    def check_var(self, v):
        # I'm just here so I don't get fined
        # just to keep it consistent with Perturber
        z = 0

class latin_hypercube_sampling(Method):
    name = "Latin hypercube sampling"
    def __init__(self):
        Method.__init__(self)

    def search(self, Sampler, Fitter, workdir='./',
               n=100, record=True, report=True, pool=True, grid=False):
        self.Fitter = Fitter
        self.file_name = os.path.join(workdir, 'latin_hypercube_sampling.csv')
        self.Sampler = Sampler,
        self.n_per_gen = n
        self.grid = grid

        print_out  = "\n==========\nRunning Latin Hypercube Sampling\n==========\n" 
        try:
            metric_list = [x.name for x in Fitter.function]
        except Exception as e:
            print(e)
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
        self.s = Sampler
        self.f = Fitter

        ## generate the hypercube samples
        self.samples = []
        n_grid = int(n**(1/3))
        print('%s grid per variable' %n_grid)
        indices_list = np.zeros()
        bound_list = [np.linspace(self.lb[i], self.up[i], n_grid) for i in range(self.var_len)]
        ### do the sampling, and go

    def go(self, i):
        uniq_id = str(uuid.uuid4())
        if not self.grid:
            var_new = self.s.random()
        else:
            var_new = self.allgrid[i]
        print(var_new)
        metric_new, fitness_new = self.f.evaluate(var_new, uniq_id)
        row = [i, uniq_id] + var_new + list(metric_new)
        row = [str(x) for x in row]
        with open(self.file_name, 'a') as f:
            f.write(','.join(row))
            f.write('\n')




class random_sampling(Method):
    name = "Random sampling"
    def __init__(self):
        Method.__init__(self)

    # just for consistency, it is not actually searching for anything
    def search(self, Sampler, Fitter, workdir='./',
               n=100, record=True, report=True, pool=True, grid=False):
        self.Fitter = Fitter
        self.file_name = os.path.join(workdir, 'random_sampling.csv')
        self.Sampler = Sampler
        self.n_per_gen = n
        self.grid = grid


        print_out  = "\n==========\nRunning Random Sampling\n==========\n" 
        print_out += "  Number or iteration  : {}\n".format(n)
        print_out += "  Record search        : {}\n".format(record)

        #self.report_start(print_out, self.file_name.replace('.csv', '.report'), report, record)
        try:
            metric_list = [x.name for x in Fitter.function]
        except Exception as e:
            print(e)
            metric_list = list(range(len(self.Fitter.function)))

        input_list = Sampler.v_label
        self.iter_n = 0
        column_header = ['Sample', 'Uniqid'] + list(input_list) + list(metric_list)
        self.f = open(self.file_name, 'w')
        print(column_header)
        self.f.write(','.join(column_header))
        self.f.write('\n')
        self.f.close()

        if self.grid:
            new = []
            for indx, val in enumerate(Sampler.v_min):
                w = np.linspace(Sampler.v_min[indx], Sampler.v_max[indx], n)
                new.append(w)
            self.allgrid = list(itertools.product(*new))
            self.allgrid = [list(q) for q in self.allgrid]
            n = len(self.allgrid)

        Fitter.normalize_weight()

        self.lb = Sampler.v_min
        self.ub = Sampler.v_max

        self.var_len = len(input_list)
        self.obj_len = len(metric_list)

        # start
        self.s = Sampler
        self.f = Fitter

        if pool:
            pool = mp.Pool(mp.cpu_count())
            pool.map(self.go, list(range(n)))
            # do = [pool.apply(self.go, args=(Sampler, Fitter, i)) for i in list(range(n))]
            pool.close()
        else:
            for i in range(n):
                self.go(i)

    def go(self, i):
        uniq_id = str(uuid.uuid4())
        if not self.grid:
            var_new = self.s.random()
        else:
            var_new = self.allgrid[i]
        print(var_new)
        metric_new, fitness_new = self.f.evaluate(var_new, uniq_id)
        row = [i, uniq_id] + var_new + list(metric_new)
        row = [str(x) for x in row]
        with open(self.file_name, 'a') as f:
            f.write(','.join(row))
            f.write('\n')





