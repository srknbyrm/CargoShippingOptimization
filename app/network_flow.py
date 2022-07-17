from pulp import *


def supply_and_demand_of_nodes(start_point, end_point, all_nodes):
    '''
    :param start_point:
    :param end_point:
    :return: Dictionary Country names are keys values are list which has 2 items first one represents supply second
            one represent demand. In our case, starting point supply part equals to 1, end point demand part equals to 1
            {'Node1': [1, 0],
              'Node2': [0, 0],
              'Node3': [0, 0],
              'Node4': [0, 0],
              'Node5': [0, 0],
              'Node6': [0, 1],
              }
    '''
    node_data = dict()
    for node in all_nodes:
        if start_point == node:
            node_data[node] = [1, 0]
        elif end_point == node:
            node_data[node] = [0, 1]
        else:
            node_data[node] = [0, 0]
    return node_data


def generate_arc_list(shipment_node, from_node, to_node):
    '''
    :param shipment_node:
    :param from_node:
    :param to_node:
    :return: Returns each possible direction as a list that contains tuples.
            (k, i, j) k -> company index i -> start point j -> destination
    [(1, 1, 2), (1, 1, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4),
    (2, 1, 2), (2, 1, 3), (2, 2, 3), (2, 2, 4), (2, 3, 4)]
    '''
    arcs = list()
    for index in range(len(from_node)):
        arcs.append((shipment_node[index], from_node[index], to_node[index]))
    return arcs


def generate_arc_data(arcs, cost):
    '''
    :param arcs:
    :param cost:
    :return:  (cost, min_flow, max_flow)
              {(1, 1, 2): [2, 0, 1], (1, 1, 3): [2, 0, 1], (1, 2, 3): [1, 0, 1],
              (1, 2, 4): [3, 0, 1], (1, 3, 4): [1, 0, 1], (2, 1, 2): [2, 0, 1],
              (2, 1, 3): [2, 0, 1], (2, 2, 3): [2, 0, 1], (2, 2, 4): [2, 0, 1], (2, 3, 4): [2, 0, 1] }
    '''
    arc_data = dict()
    for index in range(len(cost)):
        arc_data[arcs[index]] = [cost[index], 0, 1]
    return arc_data


def generate_and_solve_model(node_data, arc_data):

    arcs = list(arc_data.keys())
    nodes = list(node_data.keys())

    # Splits the dictionaries to be more understandable
    (supply, demand) = splitDict(node_data)
    (costs, mins, maxs) = splitDict(arc_data)

    # Creates Variables as Binary
    variables = LpVariable.dicts("Route", arcs, None, None, LpBinary)

    # Creates the 'prob' variable to contain the problem data
    prob = LpProblem("Minimum Cost Flow Problem Sample", LpMinimize)

    # Creates the objective function
    prob += lpSum([variables[a] * costs[a] for a in arcs]), "Total Cost of Transport"

    # Creates all problem constraints - this ensures the amount going into each node is
    # at least equal to the amount leaving
    for n in nodes:
        prob += (supply[n] + lpSum([variables[(k, i, j)] for (k, i, j) in arcs if j == n]) >=
                 demand[n] + lpSum([variables[(k, i, j)] for (k, i, j) in arcs if i == n])), \
                "Flow Conservation in Node %s" % n

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The optimised objective function value is printed to the screen
    print("Total Cost of Transportation = ", value(prob.objective))

    result = []
    for i in variables:
        if variables[i].varValue:
            print(i, '-->', variables[i].varValue)
            result.append(i)
    return value(prob.objective), result


