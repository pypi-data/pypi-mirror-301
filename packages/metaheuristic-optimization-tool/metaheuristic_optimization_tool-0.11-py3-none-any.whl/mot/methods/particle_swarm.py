import numpy as np
from .method import Method
from mot.core import Particle
import math
import uuid
import multiprocessing as mp
from functools import partial

#==============================================================================
# METHOD: Adaptive Particle Swarm Optimization
#==============================================================================


def evaluate_particle(P,Fitter):
    uniq_id = str(uuid.uuid4())
    P.metric,P.fitness = Fitter.evaluate(P.loc[:], uniq_id)
    return P


class APSO(Method):
    name = "APSO"
    populational = True

    # Default parameters:
    c1_0    = 2.0  # Initial cognitive acceleration
    c2_0    = 2.0  # Initial social acceleration
    sig_max = 1.0  # Max standard deviation for ELS
    sig_min = 0.1  # Min

    # Parameter records
    f            = []
    w            = []
    c1           = []
    c2           = []
    
    def __init__(self):
        Method.__init__(self)

    def evaluate_generation(self,Pbank,P_best,Fitter):
        P_worst = Pbank[0]
        for P in Pbank:
            # Personal best?
            if P.fitness >= P.fitness_best:
                P.loc_best     = P.loc[:]
                P.metric_best   = P.metric[:]
                P.fitness_best = P.fitness
                # Global best? Make the leader
                if P.fitness_best >= P_best.fitness_best:
                    P_best = P
            # Current worst?
            if P.fitness <= P_worst.fitness:
                P_worst = P
        return P_best, P_worst

    def search(self,Perturber,Fitter,NP,Ngen,record=False,file_name="APSO.csv",
               report=True, plot_parameters=False, Nproc=1, store=False):

        #=======================================================================
        # Preparation
        #=======================================================================

        # Setting up pool
        Nproc = mp.cpu_count()
        pool = mp.Pool(processes=Nproc)

        # Normalize weight
        Fitter.normalize_weight()

        #=======================================================================
        # Initialization
        #=======================================================================

        # Set up initial parameters
        w        = self.w
        c1       = self.c1_0
        c2       = self.c2_0
        sig_max  = self.sig_max
        sig_min  = self.sig_min
        f        = None         # Evolutionary factor
        S        = None         # Evolutionary strategy
        d        = [None]*NP    # Particle mean distance to all other particles
        P_best   = None         # Pointer to the global best particle (leader)
        P_worst  = None         # Pointer to the current worst particle

        # Initialize particle generation
        Pbank = [] # Particle bank
        for i in range(NP):
            # Random location
            loc = 0
            loc = Perturber.random()
            # Zero velocity
            vel = [0.0]*Perturber.NV
            Pbank.append(Particle(loc,vel))
            Pbank[-1].ID = i
        P_best = Pbank[0]

        # Evaluate initial particles
        Pbank = pool.map(partial(evaluate_particle, Fitter=Fitter),Pbank)

        # write header
        with open(file_name, 'w') as f:
            try:
                metric_list = [x.name for x in Fitter.function]
            except:
                metric_list = list(range(len(self.Fitter.function)))
            input_list = Perturber.v_label

            column_header = ['generation'] + list(input_list) + list(metric_list) + ['fitness']
            f.write(','.join(column_header))
            f.write('\n')

        # Evaluate initial generation
        P_best, P_worst = self.evaluate_generation(Pbank,P_best,Fitter)
        # Record
        if record: self.record(0,Pbank,file_name,Perturber,Fitter)
        if store: self.store(Pbank)

        #======================================================================
        # Start generation
        #======================================================================
        for g in range(Ngen):
            #==================================================================
            # Evolutionary State Estimation
            #==================================================================

            # Particle mean distance
            for i in range(NP):
                d[i] = 0
                for j in range(NP):
                    s = 0
                    for k in range(len(Pbank[i].loc)):
                        s = s + (Pbank[i].loc[k]-Pbank[j].loc[k])**2
                    d[i] = d[i] + np.sqrt(s)
                d[i] = d[i] / (NP-1)

            # Evolutionary factor
            d_min = min(d)
            d_max = max(d)
            if d_max == d_min: f = 1.0
            else:              f = (d[P_best.ID]-d_min)/(d_max-d_min)

            # Set evolutionary strategy
            S = None
            if f <= 0.2:
                S = 1
            elif f <= 0.3:
                p1 = 1.5 - 5*f
                p2 = 10*f - 2.0
                if np.random.uniform() < p1/(p1+p2):
                    S = 1
                else:
                    S = 2
            elif f <= 0.4:
                S = 2
            elif f <= 0.6:
                p2 = 3.0 - 5*f
                p3 = 5*f - 2.0
                if np.random.uniform() < p2/(p2+p3):
                    S = 2
                else:
                    S = 3
            elif f <= 0.7:
                S = 3
            elif f <= 0.8:
                p3 = 8.0 - 10*f
                p4 = 5*f - 3.5
                if np.random.uniform() < p3/(p3+p4):
                    S = 3
                else:
                    S = 4
            else:
                 S = 4

            #==================================================================
            # Adaptive parametres
            #==================================================================

            # Update inertia weight
            w = 1.0 / (1.0+1.5*np.e**(-2.6*f))

            # Update cognitive and social acceleration
            # Convergence
            if S == 1:
                c1 = c1 + 0.05*(1.0 + np.random.uniform()) * 0.5
                c2 = c2 + 0.05*(1.0 + np.random.uniform()) * 0.5
            # Exploitation
            if S == 2:
                c1 = c1 + 0.05*(1.0 + np.random.uniform()) * 0.5
                c2 = c2 - 0.05*(1.0 + np.random.uniform()) * 0.5
            # Exploration
            if S == 3:
                c1 = c1 + 0.05*(1.0 + np.random.uniform())
                c2 = c2 - 0.05*(1.0 + np.random.uniform())
            # Jumping-out
            if S == 4:
                c1 = c1 - 0.05*(1.0 + np.random.uniform())
                c2 = c2 + 0.05*(1.0 + np.random.uniform())
           
            # Clamp c1 and c2?
            c1 = max(1.5,c1)
            c2 = max(1.5,c2)
            c1 = min(2.5,c1)
            c2 = min(2.5,c2)

            # Scale down c1 and c2?
            if c1+c2 > 4.0:
                scale = 4.0/(c1+c2)
                c1 = c1 * scale
                c2 = c2 * scale

            # Record search parameters
            self.f.append(f)
            self.w.append(w)
            self.c1.append(c1)
            self.c2.append(c2)
            
            #==================================================================
            # Advance particles
            #==================================================================

            # Update velocities and advance particles
            for P in Pbank:
                for i in range(Perturber.NV):
                    vel_cognitive = c1*np.random.uniform()*(P.loc_best[i]-P.loc[i])
                    vel_social    = c2*np.random.uniform()*(P_best.loc_best[i]-P.loc[i])
                    P.vel[i]      = w*P.vel[i] + vel_cognitive + vel_social
                    P.loc[i]      = P.loc[i] + P.vel[i]
                Perturber.check_var(P.loc)

            # Evaluate new particles
            Pbank = pool.map(partial(evaluate_particle,Fitter=Fitter),Pbank)

            # Evaluate new generation
            P_best, P_worst = self.evaluate_generation(Pbank,P_best,Fitter)

            #==================================================================
            # Elitist Learning System
            #==================================================================

            # Update perturbation standard deviation
            sig = sig_max - (sig_max - sig_min)*g/(Ngen-1)

            # Mutated location
            loc_mutate = P_best.loc_best[:]
            
            # Choose dimension to mutate
            dim = int(math.floor(np.random.uniform()*Perturber.NV))

            # Mutate
            loc_mutate[dim] = loc_mutate[dim] \
                              + (Perturber.v_max[dim]-Perturber.v_min[dim]) \
                                * np.random.normal(0.0,sig)
            Perturber.check_var(loc_mutate)

            # Better?
            self.uniq_id = str(uuid.uuid4())
            metric_mutate, fitness_mutate = Fitter.evaluate(loc_mutate[:], self.uniq_id)
            if fitness_mutate >= P_best.fitness_best:
                P_best.loc          = loc_mutate[:]
                P_best.metric        = metric_mutate[:]
                P_best.fitness      = fitness_mutate
                P_best.loc_best     = loc_mutate[:]
                P_best.metric_best   = metric_mutate[:]
                P_best.fitness_best = fitness_mutate           
            else:
                P_worst.loc          = loc_mutate[:]
                P_worst.metric        = metric_mutate[:]
                P_worst.fitness      = fitness_mutate
                P_worst.loc_best     = loc_mutate[:]
                P_worst.metric_best   = metric_mutate[:]
                P_worst.fitness_best = fitness_mutate

            # Record
            if record: self.record(g+1,Pbank,file_name,Perturber,Fitter)
            if store: self.store(Pbank)

        # Pool closeout
        pool.close()
        pool.join()

        # Record final result
        self.var_best     = P_best.loc_best[:]
        self.metric_best   = P_best.metric_best[:]
        self.fitness_best = P_best.fitness_best


        # Search parameter plot
        if plot_parameters:
            ax1 = plt.subplot(212)
            plt.plot(self.f,'-g',label="f")
            plt.xlabel("generation#")
            plt.legend()
            ax2 = plt.subplot(211, sharex=ax1)
            plt.plot(self.c1,'-b',label=r"$c_1$")
            plt.plot(self.c2,'-r',label=r"$c_2$")
            plt.setp(ax2.get_xticklabels(), visible=False)
            plt.legend()
            plt.title("APSO Evolutionary Parameters")
            plt.savefig(file_name+".png")