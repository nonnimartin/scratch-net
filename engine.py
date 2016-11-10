import unit as u
import network as n

net = n.network(2, 2, 2, 2)

net.make_neurons()

net.spread_activation()

#net.get_connections_by_neuron(net.get_neuron(3))
print net.net_as_dict()