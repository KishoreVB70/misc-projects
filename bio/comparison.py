import time
import tflite_runtime.interpreter as tflite
from geneticalgorithm import geneticalgorithm as ga
from pyswarm import pso
import numpy as np
from os.path import dirname, join
def runPSO(obj, bounds):
    bounds  = np.array(bounds)
    lower_bounds = bounds[:,0].flatten()
    upper_bounds = bounds[:,1].flatten()
    x_opt, f_opt = pso(obj, lower_bounds, upper_bounds)
    return x_opt, f_opt

def pure1(bounds):
    def pure_obj(X):
        X = [X]
        X = np.array(X)
        input_data = X.astype(np.float32)
        input_data = input_data.reshape(1,4)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        results = interpreter.get_tensor(output_details[0]['index'])
        return -results
    values, protein = runPSO(pure_obj, bounds)
    protein = np.array([-protein])
    protein = protein.reshape(1,)
    pro = np.concatenate((values, protein))
    formatted_list = [format(num, '.4f') for num in pro]
    return np.concatenate((values, protein))


filename = join(dirname(__file__), "ccd1.tflite")
interpreter = tflite.Interpreter(model_path=filename)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def runGA(obj, bound):
    algorithm_param = {'max_num_iteration': 10, \
                       'population_size':100, \
                       'mutation_probability':0.01, \
                       'elit_ratio': 0.01, \
                       'crossover_probability': 0.9, \
                       'parents_portion': 0.3, \
                       'crossover_type':'uniform', \
                       'max_iteration_without_improv':10}

    ga_model=ga(function=obj, dimension=4,variable_type='real',variable_boundaries=bound, algorithm_parameters=algorithm_param)

    # Run the genetic algorithm
    ga_model.run()
    return ga_model.output_dict

# Function 1 -> Pure
def pure2(bounds):
    def pure_obj(X):
        X = [X]
        X = np.array(X)
        input_data = X.astype(np.float32)
        input_data = input_data.reshape(1,4)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        results = interpreter.get_tensor(output_details[0]['index'])
        return -results
    dict = runGA(pure_obj, bounds)
    protein = dict["function"]
    values = dict["variable"]
    protein = np.array([-protein])
    return np.concatenate((values, protein))

# Measure the time taken by function one
start_time_one = time.time()
result_one = pure1(np.array([[24,30], [0.012,0.082], [0.4,1], [0.4,1.8]]))
end_time_one = time.time()
time_taken_one = end_time_one - start_time_one

# Measure the time taken by function two
start_time_two = time.time()
result_two = pure2(np.array([[24,30], [0.012,0.082], [0.4,1], [0.4,1.8]]))
end_time_two = time.time()
time_taken_two = end_time_two - start_time_two

# Print the results
print(f"Time taken by Swarm Particle Optimizatoin: {time_taken_one:.5f} seconds")
print(f"Time taken by Genetic Algorithm: {time_taken_two:.5f} seconds")
print(f" Optimum found by SPO {result_one[4]}")
print(f" Optimum found by GA {result_two[4]} ")