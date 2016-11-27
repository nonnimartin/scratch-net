import math as m

class training(object):

    def __init__(self, network):

        self.network = network

    def get_output_activations(self):
        outputs = self.network.get_output_layer()
        return outputs

    def calculate_output_error(self, activation, target):
        #calculates an individual neuron's activation error
        error = .5 * pow((target - activation), 2)
        return error

    def sum_total_error(self, target):
        #for each output neuron, calculate individual error and then adds all together
        outputs = self.get_output_activations()
        total = 0
        for unit in outputs:
            total += self.calculate_output_error(outputs[unit].get_activation(), target)
        return total

    def get_hidden_w_error(self):
        net = self.network
        weight_and_input = {}
        error_slopes     = {}
        summed           = 0
        test_neuron      = self.network.get_neuron(5)
        #TEST ERROR - ultimately this will come from calculate_output_error
        test_error       = 1.5

        connections = test_neuron.get_connections()
        #TEST_INPUTS 
        print "connections = " + str(connections)
        test_inputs      = []

        #for each connection neuron, map => {neuron : [input_activation, weight]}
        for neuron in connections:
            weight_and_input[neuron] = [neuron.get_activation(), net.get_connection_weight((neuron, test_neuron))]

        #sum inputs * weights
        for connection in weight_and_input:
            total = weight_and_input[connection][0] * weight_and_input[connection][1]
            summed += total
            error_slopes[connection] = -(test_error) * (self.sigmoid(total) * (1 - self.sigmoid(total))) * weight_and_input[connection][0]
        
        print "error slope = " + str(error_slopes)

    def sigmoid(self, input):
        output = 1/(1+(m.pow(2.71828, -input)))
        return output

        #see network
        #print self.network.get_neurons_by_layer(3)

        #connections = test_neuron.get_connections()
        # connections = self.network.get_connections()
     #    for i in connections:
     #        print (list(i)[0].get_name(), list(i)[1].get_name())
        


