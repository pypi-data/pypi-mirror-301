import numpy as np
import uuid

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
                print(row)
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
