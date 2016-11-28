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

    def derivative(self, output):
        return output * (1 - output)

    def get_output_error(self):
        net = self.network
        outputs = net.get_output_layer()
        neuron_to_output = {}
        error_values = []
        #this is test_target, and assumes two outputs
        test_target = [1, 0]
        
        #map output neurons to activation
        for key, value in outputs.iteritems():
            output = value.get_activation()
            neuron_to_output[net.get_neuron(key).get_name()] = output
        print neuron_to_output
        
        #Get index for each neuron and its activation and get error from corresponding target value (by list index)
        for unit in neuron_to_output:
            index  = list(neuron_to_output).index(unit)
            output = neuron_to_output[unit]
            error = (test_target[index] - output) * self.derivative(output)
            error_values.append(error)

    def sigmoid(self, input):
        output = 1/(1+(m.pow(2.71828, -input)))
        return output

        


