# MOT (Metaheuristic Optimization Tool)

This tool is a suite of optimization algorithms along with a 
structure that allows users to optimize and process result.

Generally, the optimization algorithm samples an input set
from a user-defined range, runs it through `simulation`,
extracts results (scores) from `function`, and iterates
into an optimized solution.

Recently added are capabilities to do a sensitivity analysis
(only one parameter perturbed at a time), and uncertainty quantification
(parameters are randomly sampled from distribution).

For each session, the user should define three things:

1. `simulations.py`

This script is the front end of a single case for optimization.

In this script, you define the driving simulation that is to be optimized,
as a class, with a `__call__` function defined to produce the desired output.
```
class sim():
    name = "example"
    def __call__(self, var, uniqid):
        [function_to_generate_output](var)
        os.mkdir(uniqid)
        with open('./' + uniqid + '/out.txt', 'w') as f:
            f.write([output])
```
The var can be more than one variable, so it can be indexed:
```
class sim():
    name = "example"
    def __call__(self, var, uniqid):
        [function_to_generate_output](var[0], var[1])
```
The optimization algorithm runs this function, by sampling
from an input space and passing it as `var`. The `uniqid`
parameter is randomly generated, as an identifier for each run.
This uniqid can be used to either create a folder or file
that contains the results of the simulation.


2. `functions.py`

This script is the back end of a single case for optimization.
Here, the user can define a function that retrieves the result
from the `simulation`, and have a function return the value.
Each function is defined as a class, with a `__call__` function
that does the backend reading.

The following example reads the `out.txt` file generated
from `simulation` and returns the first line of the generated
file for the optimization algorithm. You must return a number.
```
class get_data():
    def __init__(self):
        self.name = 'result1'
        self.unit = 'g'
    def __call__(self, uniqid):
        with open('./simulationname_%s/out.txt' %uniqid, 'r') as f:
            data = f.readlines()[0]
            data = float(data)
        return data
```

The returned value is then sent to the optimization algorithm.
The return value should be a number.


3. `run.py`

This script is the main script, that sets the entire optimization algorithm.
The user should first import the `simulation` and `function` scripts for usage.
This script should have four things:

1. Perturber (input range)

```
# MOT should be imported from the root directory of this repo
from mot.base import Perturber
Perturber = Perturber()
Perturber.add_variable('varname1', min, max)
Perturber.add_variable('varname2', min2, max2)
...
```

or sampler can be used for uncertainty quantification (random sampling)
```
from mot.sampler import Sampler
Sampler = Sampler()
# randomly sample from a normal distribution
Sampler.add_variable('varname1', min1, max1, dist_fcn='normal', kwargs={'loc': mu, 'scale': sigma})
# randomly sample from a uniform distribution
Sampler.add_variable('varname1', min1, max1, dist_fcn='uniform')

```
other dist_fcns are:
- beta
- binomial
- gamma
- logistic
- lognormal
- poisson
- rayleigh
- standard_t
- weibull

you can also define a custom pdf.

2. Simulations (driver)

```
# this class.__call__ will be  called for every case
sim = sim_class_name()
```

3. Fitter (output)

```
from mot.base import Fitter
Fitter = Fitter()
Fitter.add_simulation(sim)
# two objective values - get_data and get_data2
# these should be defined in functions.py
# the following numbers are weight and normalization values
Fitter.add_function(get_data(), 1.0, norm_min=0, norm_max=0.005)
Fitter.add_function(get_data2(), 1.0, norm_min=0, norm_max=0.005)
```

4. Optimization run (optimization algorithm definition)
With all the values set up, you now define the optimization algorithm
to drive the whole thing:

```
opt = [optimization_method]
opt.search(Perturber, Fitter, ...)
```


## Available Optimization Methods

1. Simulated Annealing 
    - `from mot.methods.simulated_annealing import SimulatedAnnealing`
2. Adaptive Particle Swarm Optimization
    - `from mot.methods.particle_swarm import APSO`
3. Sensitivity
    - `from mot.methods.sensitivity import sensitivity`
4. Random Sampling
    - `from mot.methods.random_sampling import random_sampling`
    -  Must use Sampler as perturber
5. scipy_methods
    - `from mot.methods.scipy_methods import scipy_optimize`
    - algorithms:
        - fmin_slsqp
        - differential_evolution
        - basinhopping
        - brute
        - fmin_cobyla
6. Inspyred methods
    - `from mot.methods.inspyred_methods import inspyred_optimize`
    - algorithms:
        - PAES
        - NSGA2
        - GA
        - ES
        - SA
        - DEA
        - EDA
        - PSO
