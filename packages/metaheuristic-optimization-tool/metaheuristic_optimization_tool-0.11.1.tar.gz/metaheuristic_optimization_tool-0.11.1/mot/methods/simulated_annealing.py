import numpy as np
from .method import Method
import uuid

class SimulatedAnnealing(Method):
    name         = "SA"
    populational = False

    # Initial parameters
    T0           = 1.0 # Initial temperature (or acceptance level)
    alpha        = 1.0 #   decay parameter
    frac0        = 1.0 # Perturbation fraction
    beta         = 1.0 #   decay parameter
    
    def __init__(self,T0,alpha,frac0,beta):
        Method.__init__(self)
        self.T0     = T0
        self.alpha  = alpha
        self.frac0  = frac0
        self.beta   = beta

    def search(self,Perturber,Fitter,Niter,var_init=0,record=False,
               file_name="SA.csv",report=True,store=False):

        #=======================================================================
        # Preparation
        #=======================================================================
        # Normalize weight
        Fitter.normalize_weight()
        
        #======================================================================
        # Initialize
        #======================================================================

        # Annealing parameters
        T     = self.T0
        frac  = self.frac0
        alpha = self.alpha
        beta  = self.beta

        # The search variable
        var = []
        # Random
        if var_init == 0:
            var = Perturber.random()
        # User defined
        else:
             var = var_init
        # Evaluate
        self.uniq_id = str(uuid.uuid4())
        metric, fitness = Fitter.evaluate(var, self.uniq_id)

        var_best     = var[:]
        metric_best   = metric[:]
        fitness_best = fitness

        # write header

        with open(file_name, 'w') as f:
            try:
                metric_list = [x.name for x in Fitter.function]
            except:
                metric_list = list(range(len(self.Fitter.function)))

            input_list = Perturber.v_label

            column_header = ['Iteration'] + list(input_list) + list(metric_list) + ['fitness']
            f.write(','.join(column_header))
            f.write('\n')

        if record or store:
            P         = Particle(var[:],var[:])
            P.metric   = metric[:]
            P.fitness = fitness
        if record: self.record(0,P,file_name,Perturber,Fitter)
        if store: self.store(P)

        #======================================================================
        # Start!
        #======================================================================
        
        for iteration in range(Niter):
            # Perturb and evaluate fitness
            self.uniq_id = str(uuid.uuid4())
            var_new     = Perturber.perturb(var, frac)
            metric_new, fitness_new = Fitter.evaluate(var_new, self.uniq_id)

            # Fitness difference
            DeltaE = fitness_new - fitness

            # Better fitness?
            if DeltaE >= 0:
                var     = var_new[:]
                metric   = metric_new[:]
                fitness = fitness_new

            # Accept worse fitness?
            elif np.random.uniform() <= np.e**(DeltaE/T):
                var     = var_new[:]
                metric   = metric_new[:]
                fitness = fitness_new

            # Update acceptance parametres
            T    = T * alpha
            frac = frac * beta

            # Update best fitness and solution
            if fitness >= fitness_best:
                fitness_best = fitness
                var_best     = var[:]
                metric_best   = metric[:]

            # Record
            if record or store:
                P.loc     = var_new[:]
                P.metric   = metric[:]
                P.fitness = fitness
            if record: self.record(iteration,P,file_name,Perturber,Fitter)
            if store: self.store(P)

        self.var_best     = var_best
        self.metric_best   = metric_best
        self.fitness_best = fitness_best

