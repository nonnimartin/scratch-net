import unit as u
import network as n
import json

net = n.network(2, 2, 2, 2)

net.make_neurons()

net.spread_activation()

#prints dictionary representation of network, can be seen better after reformatted here: https://jsonformatter.curiousconcept.com/
print net.net_as_dict()