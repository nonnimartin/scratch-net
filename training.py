class training(object):

    def __init__(self, network, target_out):

        self.network               = network
        self.target_out            = target_out
        self.final_layer_to_target = {}
        self.outputs_to_error      = {}

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
        print self.outputs_to_error
            
    def map_final_layer_to_target(self):

        outputs      = self.get_output_layer()
        ordered_name_list = []
        targets = self.target_out

        if len(self.target_out) != len(outputs):
            print "Target output is not the same size as the output layer"
            return
        else:
            for neuron_name in sorted(outputs.iterkeys(), reverse=True):
                ordered_name_list.append(neuron_name)

            for target in range(len(targets)):
                self.final_layer_to_target[ordered_name_list[target]] = targets[target]

    def main(self):
        self.map_final_layer_to_target()
        self.map_outputs_to_error()


if __name__ == "__main__":
    training().main()





