import tensorflow as tf
import numpy as np
from geneticalgorithm import geneticalgorithm as ga


model = tf.keras.saving.load_model("/content/drive/MyDrive/models/ccd_trial")

def runGA(obj, bound):

  algorithm_param = {'max_num_iteration': 10,\
                    'population_size':100,\
                    'mutation_probability':0.01,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.9,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv':5}

  # Create a genetic algorithm model using the specified parameters
  ga_model=ga(function=obj, dimension=4,variable_type='real',variable_boundaries=bound, algorithm_parameters=algorithm_param)

  # Run the genetic algorithm
  ga_model.run()
  return ga_model.output_dict

# Function 1 -> Pure
def pure(bounds):
    def pure_obj(X):
      X = [X]
      results = model.predict(X)
      return -results
    dict = runGA(pure_obj, bounds)
    protein = dict["function"]
    values = dict["variable"]
    return protein, values


# Function 2 -> Cost
def cost(mgP, gluP, naP, working_cost, bounds):
    def cost_obj(X):
        time = X[0]
        mg = X[1]
        glu = X[2]
        na = X[3]

        X = [X]
        protien = model.predict(X)
        price  = mg*mgP + glu*gluP + na*naP + time* working_cost
        result = protien/price
        return -result
    dict = runGA(cost_obj, bounds)

    cost = dict["function"]
    values = dict["variable"]
    protein = model.predict(values)
    return protein, values, cost

# Function 3 -> profit
def profit(mgP, gluP, naP, working_cost, product_value, bounds):
    def prof_obj():
        time = X[0]
        mg = X[1]
        glu = X[2]
        na = X[3]
        X = [X]

        protien = model.predict(X)

        price  = mg*mgP + glu*gluP, na*naP, time* working_cost
        selling = protien * product_value
        result = selling - price
        return -result
    dict = runGA(prof_obj, bounds)
    profit = dict["function"]
    values = dict["variable"]
    protein = model.predict(values)
    return protein, values, profit

# Function 4 -> Time
def time(bounds):
    def time_obj(X):
        [time] = X[0]
        X = [X]
        protien = model.predict(X)
        result = protien/time
        return -result
    dict =  runGA(time_obj, bounds)
    perTime = dict["function"]
    values = dict["variable"]
    protein = model.predict(values)
    return protein, values, perTime
   