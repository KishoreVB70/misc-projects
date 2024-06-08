import tflite_runtime.interpreter as tflite
from pyswarm import pso
import numpy as np
from os.path import dirname, join

filename = join(dirname(__file__), "ccd1.tflite")
interpreter = tflite.Interpreter(model_path=filename)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def runPSO(obj, bounds):
    bounds  = np.array(bounds)
    lower_bounds = bounds[:,0].flatten()
    upper_bounds = bounds[:,1].flatten()
    x_opt, f_opt = pso(obj, lower_bounds, upper_bounds)
    return x_opt, f_opt

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
    values, protein = runPSO(pure_obj, bounds)
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
    values, perTime = runPSO(time_obj, bounds)


    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    perTime = np.array([-perTime])
    protein = np.array(protein)
    protein = protein.reshape(1,)
    perTime = perTime.reshape(1,)

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
    values, cost = runPSO(cost_obj, bounds)

    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    cost = np.array([-cost])
    protein = np.array(protein)
    cost = cost.reshape(1,)
    protein = protein.reshape(cost.shape)
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

    values, profit = runPSO(prof_obj, bounds)

    # Predict protein
    values = np.array(values)
    input_data = values.astype(np.float32)
    input_data = input_data.reshape(1,4)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    protein = interpreter.get_tensor(output_details[0]['index'])

    profit = np.array([-profit])
    protein = np.array(protein)
    profit = profit.reshape(1,)
    protein = protein.reshape(profit.shape)
    print(protein)
    pro = np.concatenate((values, protein, profit))
    formatted_list = [format(num, '.4f') for num in pro]
    return ','.join(map(str, formatted_list))

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
    return ','.join(map(str, formatted_list))A