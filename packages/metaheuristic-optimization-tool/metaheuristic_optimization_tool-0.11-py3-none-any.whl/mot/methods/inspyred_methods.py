from .method import Method
# from tabulate import tabulate
import multiprocessing as mp
from functools import partial
import signal
import numpy as np
import sys
from time import time
from random import Random
import random
import os
# import uuid
import inspyred
from inspyred import ec
from inspyred.ec import emo
#import multiprocessing
#from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool

"""
class inspyred_method
leverages the python package inspyred
to optimize the objective function
"""

class inspyred_optimize(Method):
    name = 'Inspyred optimiaztion'

    def __init__(self, is_mpi=False):
        self.is_mpi = is_mpi
        Method.__init__(self)


    def write_header(self, input_list, metric_list):
        column_header = ['Generation', 'Iteration', 'Uniqid'] + list(input_list) + list(metric_list)
        with open(self.file_name, 'w') as f:
            f.write(','.join(column_header))
            f.write('\n')
            f.close()


    def write_appdx(self, input_list, metric_list):
        column_header = ['Uniqid'] + list(input_list) + list(metric_list)
        with open(self.appdx_name, 'w') as f:
            f.write(','.join(column_header))
            f.write('\n')
            f.close()

    def write_apdx_line(self, uniqid, input_list, metric_list):
        with open(self.appdx_name, 'a') as f:
            row = [uniqid] + list(input_list) + list(metric_list[0])
            row = [str(q) for q in row]
            f.write(','.join(row))
            f.write('\n')
            f.close()


    def get_uniqid_from_appdx(self, input_list, metric_list):
        s = open(self.appdx_name, 'r').readlines()
        in_ = list(input_list) + list(metric_list)
        in_ = [str(q) for q in in_]
        in_ = ','.join(in_)
        s = [q for q in s if in_ in q]
        # assert(len(s) == 1)
        return s[0].split(',')[0]

    def write_result_line(self, gen, pop, input_list, metric_list):
        uniqid = self.get_uniqid_from_appdx(input_list, metric_list)
        with open(self.file_name, 'a') as f:
            row = [gen, pop, uniqid] + list(input_list) + list(metric_list)
            row = [str(q) for q in row]
            f.write(','.join(row))
            f.write('\n')
            f.close()


    def my_selector(self, random, population, args):
        selected = []
        for pop in population:
            kill = False
            for k,v in self.kill_dict.items():
                if 'max' in v.keys():
                    if pop.fitness[k] > v['max']: kill = True
                if 'min' in v.keys():
                    if pop.fitness[k] < v['min']: kill = True
            if not kill:
                selected.append(pop)
        for i in range(len(population) - len(selected)):
            selected.append(selected[i])

        return selected


    def int_bounder(self, candidate, args):

        r = []
        assert(len(candidate) == len(self.is_int))
        for indx, val in enumerate(candidate):
            print(np.ceil(self.lb[indx]))
            print(np.floor(self.ub[indx]))
            if self.is_int[indx]:
                l = list(range(int(np.ceil(self.lb[indx])), int(np.floor(self.ub[indx]))+1))
                x = inspyred.ec.DiscreteBounder(l)
                r.append(x([candidate[indx]], args)[0])
            else:
                x = inspyred.ec.Bounder(self.lb[indx], self.ub[indx])
                r.append(x([candidate[indx]], args)[0])
        return r


    def search(self, Perturber, Fitter, algorithm='', workdir='./',
               n=100, maxiter=100, maximize=False, kill_dict={}, is_int=False, **kwargs):
        self.Fitter = Fitter
        self.file_name = os.path.join(workdir, algorithm+'.csv')
        self.appdx_name = os.path.join(workdir, 'temp_'+algorithm+'.csv')
        self.Perturber = Perturber
        self.n_per_gen = n
        if type(is_int) == list:
            self.is_int = is_int
        else:
            self.is_int = [is_int] * len(Perturber.v_min)

        self.rand = Random()
        self.rand.seed(time())

        try:
            metric_list = [x.name for x in Fitter.function]
        except:
            metric_list = [str(q) for q in list(range(len(self.Fitter.function)))]

        input_list = Perturber.v_label
        self.iter_n = 0
        self.write_header(input_list, metric_list)
        self.write_appdx(input_list, metric_list)

        Fitter.normalize_weight()

        self.lb = Perturber.v_min
        self.ub = Perturber.v_max

        self.kill_dict = {}
        for k,v in kill_dict:
            if k not in metric_list: raise ValueError('Kill dict metrics should match metric')
            self.kill_dict[metric_list.index(k)] = v

        # define the problem
        self.var_len = len(input_list)
        self.obj_len = len(metric_list)
        # problem_ = problem(self)

        """
        multiobjective optimization
        PAES: Pareto Archived Evolution Strategy
        NSGA2: Nondominated Sorting Genetic Algorithm 


        GA: Genetic Algorithm
        ES: Evolution Strategy
        SA: Simulated Annealing
        DEA: Differential Evolution Algorithm
        EDA: Estimation of Distribution
        PSO: Particle Swarm Optimization
        """
        algorithms = {'PAES': inspyred.ec.emo.PAES,
                      'NSGA2': inspyred.ec.emo.NSGA2,
                      'GA': inspyred.ec.GA,
                      'ES': inspyred.ec.ES,
                      'SA': inspyred.ec.SA,
                      'DEA': inspyred.ec.DEA,
                      'EDA': inspyred.ec.EDA,
                      'PSO': inspyred.swarm.PSO
                      }

        if algorithm not in algorithms.keys():
            print('Parameter algorithm has to be one of these:\n')
            print('\n'.join(list(algorithms.keys())))
            raise ValueError()
        else:
            self.n = 0
            ea = algorithms[algorithm](self.rand)
            ea.variator = [inspyred.ec.variators.blend_crossover,
                           inspyred.ec.variators.gaussian_mutation]
            # ea.selector = self.my_selector
            ea.terminator = inspyred.ec.terminators.evaluation_termination
            print('Running optimization algorithm:', algorithm)
            print('Running on %s cores' %mp.cpu_count())

            bounder = ec.Bounder(self.lb, self.ub)
            if is_int:
                bounder = self.int_bounder

            ea.observer = self.observe_
            if self.is_mpi:
                print('This is running in MPI mode')
                final = ea.evolve(generator=self.generate_,
                                  evaluator=inspyred.ec.evaluators.parallel_evaluation_pp,
                                  pp_evaluator=self.evaluate_,
                                  pop_size=self.n_per_gen,
                                  bounder=bounder,
                                  maximize=maximize,
                                  num_inputs=self.var_len,
                                  max_evaluations=maxiter*self.n_per_gen,
                                  **kwargs
                                  )

                                  
            if not self.is_mpi:
                final = ea.evolve(generator=self.generate_,
                                  evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                                  mp_evaluator=self.evaluate_,
                                  mp_num_cpus=mp.cpu_count(),
                                  pop_size=self.n_per_gen,
                                  bounder=bounder,
                                  maximize=maximize,
                                  num_inputs=self.var_len,
                                  max_evaluations=maxiter*self.n_per_gen,
                                  **kwargs
                                  )
            final.sort(reverse=True)
            print(final[0])
            os.remove(self.appdx_name)


    def generate_(self, random, args):
        pops = [random.uniform(self.lb[i], self.ub[i]) for i in range(args['num_inputs'])]
        return pops

    def evaluate_(self, candidates, args):
        print('evaluating')
        print(candidates)
        fitness = []
        result_list = []
        for cs in candidates:
            import uuid
            uniqid = str(uuid.uuid4())
            for sim in self.Fitter.simulation:
                sim(cs, uniqid)
            for indx, val in enumerate(self.Fitter.function):
                result_list.append(val(uniqid))
            if self.obj_len > 1:
                fitness.append(emo.Pareto(result_list))
            else:
                fitness.append(result_list)

            self.write_apdx_line(uniqid, cs, fitness)
        return fitness


    def observe_(self, population, num_generations, num_evaluations, args):
        for indx, pop in enumerate(population):
            d = pop.__dict__
            candidate = d['_candidate']
            fitness = d['fitness']
            self.write_result_line(num_generations, indx, candidate, fitness)

