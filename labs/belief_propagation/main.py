import numpy as np
from copy import deepcopy

# number of variables in a factor graph
n_vars = 10

# all variables
variables = ['x' + str(i) for i in range(n_vars)]

# number of factors in a factor graph
n_funcs = 5

# variable space
var_space = [1., -1., 25., -25.]

# some function examples
f0 = lambda x : x['x0'] + x['x1']
f1 = lambda x : x['x1']
f2 = lambda x : x['x2']
f3 = lambda x : x['x3'] + x['x0']
f4 = lambda x : x['x4']

# list of all functions
funcs = {'f0': f0, 'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4}

# list of argument numbers required for each functions
deps = {'f0': ['x0','x1'], 'f1': ['x1'], 'f2': ['x2'], 'f3': ['x0','x3'], 'f4': ['x4']}

# sanity check
assert(len(deps) == n_funcs)
assert(len(funcs) == n_funcs)

# list of all nodes
nodes = list(funcs.keys()) + variables

# sanity check
assert(len(nodes) == n_vars + n_funcs)

# brute force marginalization
def brute_marginalize1(sum_over, assignments):
    if len(sum_over) == 0:
        assert(len(assignments) == n_vars)
        res = lambda x : 1.
        for f in funcs: res = lambda x : res(x) * f(x)
        return res
    var = sum_over[0]
    result = lambda x : 0.
    new_assignments = deepcopy(assignments)
    for value in var_space:
        new_assignments[var] = value
        result = lambda x : brute_marginalize(sum_over[1:], new_assignments)(x) + result(x)
    return result

def brute_marginalize(variable):
    sum_over = deepcopy(variables)
    sum_over.remove(variable)
    return brute_marginalize1(sum_over, {})

print(brute_marginalize('x0')(0))

# get siblings of a node in the factor graph
def get_siblings(node):
    if node[0] == 'f':
        return deps[node]
    elif node[0] == 'x':
        return [key for key, value in items if node in items]
# array with all of the messages
messages = [[None] * len(nodes)] * len(nodes)

print(get_siblings('x0'))