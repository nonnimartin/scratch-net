import math as m

class neuron(object):

    def __init__(self, name, layer, inputs):

        self.name           = name
        self.layer          = layer
        self.activation     = 0
        self.before_layer   = []


    def set_before_layer(self, layer):
        self.before_layer = layer 

    def get_name(self):
        return self.name

    def get_layer(self):
        return self.layer

    def get_activation(self):
        return self.activation

    def set_activation(self, activation):
        self.activation = activation

    def get_before_layer(self):
        return self.before_layer

    def sigmoid(self, input):
        output = 1/(1+(m.pow(2.71828, -input)))
        return output



