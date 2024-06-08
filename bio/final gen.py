import tflite_runtime.interpreter as tflite
from geneticalgorithm import geneticalgorithm as ga
import numpy as np
from os.path import dirname, join

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
def pure(bounds):
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


def profit(working_cost, mgP, gluP, naP,product_value, bounds):
    def prof_obj(X):
        time = X[0]
        mg = X[1]
        glu = X[2]
        na = X[3]
        X = [X]
        X = np.array(X)
        input_data = X.astype(np.float32)
        input_data = input_data.reshape(1,4)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        protein = interpreter.get_tensor(output_details[0]['index'])
        price = (time * working_cost) + (mg*mgP) + (glu*gluP) + (na*naP)
        selling = protein * product_value
        result = selling - price
        return -result
    dict = runGA(prof_obj, bounds)
    profit = dict["function"]
    values = dict["variable"]
    return str(-profit)

def cost(mgP, gluP, naP, working_cost, bounds):
    def cost_obj(X):
        time = X[0]
        mg = X[1]
        glu = X[2]
        na = X[3]
        X = [X]
        X = np.array(X)
        input_data = X.astype(np.float32)
        input_data = input_data.reshape(1,4)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        protein = interpreter.get_tensor(output_details[0]['index'])
        price  = mg*mgP + glu*gluP + na*naP + time* working_cost
        result = protein/price
        return -result
    dict = runGA(cost_obj, bounds)
    cost = dict["function"]
    values = dict["variable"]
    # protein = model.predict(values)
    return str(-cost)

def time(bounds):
    def time_obj(X):
        time = X[0]
        X = [X]
        X = np.array(X)
        input_data = X.astype(np.float32)
        input_data = input_data.reshape(1,4)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        protein = interpreter.get_tensor(output_details[0]['index'])
        result = protein/time
        return -result
    dict =  runGA(time_obj, bounds)
    perTime = dict["function"]
    values = dict["variable"]
    # protein = model.predict(values)
    return str(-perTime)

def npy():
    # working_cost = float(str(working_cost))
    # mgP = float(str(mgP))
    # gluP = float(str(gluP))
    # naP = float(str(naP))
    # product_value = float(str(product_value))

    bbd = np.array([[24,30], [0.012,0.082], [0.4,1], [0.4,1.8]])
    # pro = cost(working_cost, mgP, gluP, naP, bbd)
    pro = pure(bbd)
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))

