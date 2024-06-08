import tflite_runtime.interpreter as tflite
from geneticalgorithm import geneticalgorithm as ga
import numpy as np
from os.path import dirname, join

filename = join(dirname(__file__), "ccd1.tflite")
interpreter = tflite.Interpreter(model_path=filename)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


from geneticalgorithm import geneticalgorithm as ga
def runGA(obj, bound):
    algorithm_param = {'max_num_iteration': 10, \
                       'population_size':100, \
                       'mutation_probability':0.01, \
                       'elit_ratio': 0.01, \
                       'crossover_probability': 0.9, \
                       'parents_portion': 0.3, \
                       'crossover_type':'uniform', \
                       'max_iteration_without_improv':8}

    ga_model=ga(function=obj, dimension=4,variable_type='real',
                variable_boundaries=bound, algorithm_parameters=algorithm_param)

    ga_model.run()
    return ga_model.output_dict


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
    bounds  = np.array(bounds)
    print(bounds)
    dict = runGA(pure_obj, bounds)
    protein = dict["function"]
    values = dict["variable"]
    protein = np.array([-protein])
    protein = protein.reshape(1,)
    pro = np.concatenate((values, protein))
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))



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
    bounds = np.array(bounds)
    dict =  runGA(time_obj, bounds)
    perTime = dict["function"]
    values = dict["variable"]

    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    perTime = np.array([-perTime])
    protein = np.array(protein)
    protein = protein.reshape(perTime.shape)
    print(protein)
    pro = np.concatenate((values, protein, perTime))
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))

def cost(mgP, gluP, naP, working_cost, bounds):
    working_cost = float(str(working_cost))
    mgP = float(str(mgP))
    gluP = float(str(gluP))
    naP = float(str(naP))

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

    bounds = np.array(bounds)
    dict = runGA(cost_obj, bounds)
    cost = dict["function"]
    values = dict["variable"]

    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    cost = np.array([-cost])
    protein = np.array(protein)
    protein = protein.reshape(cost.shape)
    print(protein)
    pro = np.concatenate((values, protein, cost))
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))

def profit(working_cost, mgP, gluP, naP,product_value, bounds):
    # Manipulation of inputs
    working_cost = float(str(working_cost))
    mgP = float(str(mgP))
    gluP = float(str(gluP))
    naP = float(str(naP))
    product_value = float(str(product_value))
    bounds = np.array(bounds)

    # Objective function
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
    
    # Run the genetic algorithm
    dict = runGA(prof_obj, bounds)
    profit = dict["function"]
    values = dict["variable"]

    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    profit = np.array([-profit])
    protein = np.array(protein)
    protein = protein.reshape(profit.shape)
    pro = np.concatenate((values, protein, profit))
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))


bbd = np.array([[24,30], [0.012,0.082], [0.4,1], [0.4,1.8]])

result = profit(1,2,3,4,5,bbd)
print(result)