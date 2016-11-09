import unit as u
import network as n

net = n.network(2, 2, 2, 2)

net.make_neurons()

net.spread_activation()

print net.net_as_dict()