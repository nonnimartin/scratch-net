import math as m

class neuron(object):

    def __init__(self, name, layer, inputs):

        self.name               = name
        self.layer              = layer
        self.activation         = 0
        self.before_layer       = []
        self.before_layer_names = []
        self.connections        = []
        self.connections_names  = []

    def set_before_layer(self, layer):
        self.before_layer = layer
        for unit in layer:
            self.before_layer_names.append(unit.get_name())

    def get_name(self):
        return self.name

    def get_layer(self):
        return self.layer

    def get_activation(self):
        return self.activation

    def set_activation(self, activation):
        self.activation = activation

    def add_connection(self, connection):
        self.connections.append(connection)
        self.connections_names.append(connection.get_name())

    def get_connections(self):
        return self.connections

    def get_connections_names(self):
        return self.connections_names

    def get_before_layer(self):
        return self.before_layer

    def get_before_layer_names(self):
        return self.before_layer_names

    def sigmoid(self, input):
        output = 1/(1+(m.pow(2.71828, -input)))
        return output



