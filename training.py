import math as m

class training(object):

    def __init__(self, network, target_out):

        self.network               = network
        self.target_out            = target_out
        self.final_layer_to_target = {}
        self.outputs_to_error      = {}
        self.current_weights_map   = {}

    def backpropagate_error(self):
        
        net                   = self.network
        targets_list          = self.target_out
        #assign errors first to output layer, and then to earlier layers
        connections           = net.get_connections()
        #Start from highest layer and descend 
        current_layer         = net.get_network_width() - 1
        #Get final layer and map each neuron to the target output
        final_layer           = net.get_neurons_by_layer(net.get_network_width() - 1)
        final_layer_number    = net.get_network_width() - 1
        map_layer_to_targets  = {}
        #map neurons to future (post-all-calculation) error results
        new_error_map         = {}
        current_weights_map   = {}

        #map to preserve order in targets and output layer
        for neuron in final_layer:
            target_value = targets_list[0]
            map_layer_to_targets[neuron.get_name()] = target_value
            targets_list.pop(0)

        #set error on final layer directly with target - output
        for output_neuron in final_layer:
            output_neuron_name = output_neuron.get_name()
            error              = output_neuron.get_activation() - map_layer_to_targets[output_neuron_name]
            output_neuron.set_error(error)
        
        #for each layer from the end layer compute and set earlier unit errors
        while current_layer >= 0:
            layer_neurons = net.get_neurons_by_layer(current_layer)

            for after_neuron in layer_neurons:
                
                after_neuron_name = after_neuron.get_name()
                #For each connection, take the later error and compute the prior error
                before_layer      = after_neuron.get_before_layer()
                #get all the weights in the before layer and compute the sum of this weight/(the sum of the weights)
                for before_neuron in before_layer:
                    after_error        = after_neuron.get_error()
                    after_neuron_name  = after_neuron.get_name()
                    before_neuron_name = before_neuron.get_name()
                    current_tuple      = (before_neuron, after_neuron)
                    current_weight     = net.get_connection_weight(current_tuple)

                    loop_weights_list = []
                #loop again through weight tuples to store the weights for each calculation of prior error
                    for sum_before in before_layer:
                        loop_tuple     = (sum_before, after_neuron)
                        loop_weight    = net.get_connection_weight(loop_tuple)
                        loop_weights_list.append(loop_weight)
                        #take current weight and divide by sum error of all other current layer weights
                        #this ends up causing problems if the sum = 0
                        weights_sum           = sum(loop_weights_list)
                        divided_weight        = current_weight/weights_sum
                        #multiply divided weight by after_neuron's error
                        computed_before_error = after_error * divided_weight
                        #map before neuron to its future error value for later use
                    current_weights_map[before_neuron.get_name()] = weights_sum
                    new_error_map[before_neuron.get_name()]       = computed_before_error
                    before_neuron.set_error(computed_before_error)

            current_layer -= 1
        #Set current error map for use in weight adjustment (see adjust weights)
        self.current_weights_map = current_weights_map

    def adjust_weights(self):
        #adjust connection weights after backpropagation in each learning epoch
        
        net                            = self.network
        #Learning rate will have to be adjusted/adjustable to avoid over-correction on learning
        learning_rate                  = 0.1
        #get network connections as tuple pairs
        connections                    = net.get_connections()
        map_connections_to_adjustments = {}

        for connection in connections:
            before_neuron          = connection[0]
            before_name            = before_neuron.get_name()
            after_neuron           = connection[1]
            after_name             = after_neuron.get_name()
            current_weights_map    = self.current_weights_map
            #current sum of all weights in the layer sum (see backpropagation)
            current_before_weights = current_weights_map[before_name]
            before_activation      = before_neuron.get_activation()
            sig_weights            = self.sigmoid(current_before_weights)
            
            adjustment_value       = -(sig_weights * (1 - sig_weights) * before_activation)
            #print "adjustment for " + str(before_name) + "-" + str(after_name) + " = " + str(adjustment_value)

            #map connections tuples to adjustment values
            map_connections_to_adjustments[connection] = adjustment_value
        
        #adjust values from map to avoid altering during calculation
        for key, value in map_connections_to_adjustments.iteritems():
            before_neuron                  = key[0]
            after_neuron                   = key[1]
            current_connection_weight      = net.get_connection_weight(key)
            updated_weight                 = current_connection_weight + value
            net.set_connection_weight(before_neuron, after_neuron, updated_weight)
                
    def get_output_layer(self):

        outputs = self.network.get_output_layer()
        return outputs

    def map_outputs_to_error(self):

        outputs = self.get_output_layer()
        
        for neuron_name, neuron in outputs.iteritems():
            out_activation = neuron.get_activation()
            neuron_name    = neuron.get_name()
            target         = self.final_layer_to_target[neuron_name]
            error          = target - out_activation
            self.outputs_to_error[neuron_name] = error
            
    def map_final_layer_to_target(self):

        outputs      = self.get_output_layer()
        ordered_name_list = []
        targets = self.target_out

        if len(self.target_out) != len(outputs):
            print "Target output is not the same size as the output layer"
            exit()
        else:
            for neuron_name in sorted(outputs.iterkeys(), reverse=True):
                ordered_name_list.append(neuron_name)

            for target in range(len(targets)):
                self.final_layer_to_target[ordered_name_list[target]] = targets[target]

    def sigmoid(self, input):
        output = 1/(1+(m.pow(2.71828, -input)))
        return output

    def main(self):
        self.map_final_layer_to_target()
        self.map_outputs_to_error()
        self.backpropagate_error()
        self.adjust_weights()


if __name__ == "__main__":
    training().main()





