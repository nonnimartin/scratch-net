class training(object):

    def __init__(self, network, target_out):

        self.network               = network
        self.target_out            = target_out
        self.final_layer_to_target = {}
        self.outputs_to_error      = {}


    def backpropagate_error(self):

        #assign errors first to output layer, and then to earlier layers

        all_neurons              = self.network.get_all_layers()
        #Start from highest neuron name and descend 
        current_counter          = len(all_neurons) - 1
        output_layer_num         = self.network.get_network_width() - 1
        local_target_values      = self.target_out

        for neuron in all_neurons:
            current_neuron           = all_neurons[current_counter]
            current_counter         -= 1
            current_neuron_layer     = current_neuron.get_layer()

            if current_neuron_layer == output_layer_num:
                target_value = local_target_values[0]
                output       = current_neuron.get_activation()
                error        = target_value - output
                current_neuron.set_error(error)
                print "error = " + str(error)
            else:
                pass

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

    def main(self):
        self.map_final_layer_to_target()
        self.map_outputs_to_error()
        self.backpropagate_error()


if __name__ == "__main__":
    training().main()





