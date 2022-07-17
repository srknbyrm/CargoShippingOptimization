# Test
import pandas

from app.network_flow import supply_and_demand_of_nodes, generate_arc_list, generate_arc_data, generate_and_solve_model

df = pandas.read_csv('shipment_prices.csv')
shipment_company = df["shipment_company"].tolist()
from_country = df["from_country"].tolist()
to_country = df["to_country"].tolist()
cost = df["cost"].tolist()

# list of nodes
nodes = list(set(from_country))  # i.e. [Austria, Bulgaria, etc.]
node_data = supply_and_demand_of_nodes('Austria', 'Crotia', nodes)
arcs = generate_arc_list(shipment_company, from_country, to_country)
arc_data = generate_arc_data(arcs, cost)
total_cost, routes_as_list = generate_and_solve_model(node_data, arc_data)
print(total_cost, routes_as_list)