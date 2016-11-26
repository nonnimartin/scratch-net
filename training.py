class training(object):

    def __init__(self, network):

    	self.network = network

    def get_output_activations(self):
    	outputs = self.network.get_output_layer()
    	return outputs

    def calculate_error(self, activation, target):
    	#calculates an individual neuron's activation error
    	error = .5 * pow((target - activation), 2)
    	return error

    def sum_error(self, target):
    	#for each output neuron, calculate individual error and then adds all together
    	outputs = self.get_output_activations()
    	total = 0
    	for unit in outputs:
    		total += self.calculate_error(outputs[unit].get_activation(), target)
    	return total


