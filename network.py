import unit as u
import random
import json

class network(object):

    def __init__(self, input_depth, hidden_depth, hidden_width, output_depth):

        '''
        Example of network with:
            input depth =3,
            hidden depth = 4,
            hidden width = 1,
            output depth = 3

             o
           /   \
         o---o---o
         o---o---o
         o---o---o
           \   /
             o

        '''

        self.input_depth  = input_depth
        self.hidden_depth = hidden_depth
        self.hidden_width = hidden_width
        self.output_depth = output_depth
        self.all_layers    = {}
        self.input_layer   = {}
        self.hidden_units  = {}
        self.output_layer  = {}
        self.out_afferents = {}
        self.connections   = {}
        self.by_layer      = {}


    def make_neurons(self):

        #these should probably be refactored into discrete methods, but bear in mind the counter

        counter       = 0
        #make input layer
        for neuron in range(self.input_depth):
            self.input_layer[counter] = u.neuron(counter, 0, [])
            counter += 1
        #make hidden units
        for layer in range(self.hidden_width):
            for neuron in range(self.hidden_depth):
                self.hidden_units[counter] = u.neuron(counter, layer + 1, self.input_layer)
                counter += 1
        #Total count of input and hidden units
        input_plus_hidden = len(self.input_layer) + len(self.hidden_units)
        #Get output afferents (i.e. the last x that constitute the layer before the output)
        rev_count = input_plus_hidden
        for unit in range(self.hidden_depth):
            self.out_afferents[rev_count-1] = self.hidden_units[rev_count-1]
            rev_count -= 1
        #make output layer
        for neuron in range(self.output_depth):
            self.output_layer[counter] = u.neuron(counter, self.hidden_width + 1, self.out_afferents)
            counter += 1
        #merge dictionaries into an all_layers dictionary
        self.all_layers.update(self.input_layer)
        self.all_layers.update(self.hidden_units)
        self.all_layers.update(self.output_layer)
        #Add input layer to each neuron
        self.set_all_before_layers()
        #create weights
        self.create_weights()

        return self


        
    def get_all_layers(self):
         return self.all_layers

    def set_by_layers(self):
        #maps neurons to layers in the following format {layer0: [neuron0, neuron1, neuron2], layer1: [etc...]}
        layers_map = {}
        neurons_list = []
        for neuron in self.all_layers:
            layer = self.all_layers[neuron].get_layer()
            if layer not in layers_map:
                layers_map[layer] = []
                layers_map[layer].append(self.all_layers[neuron])
            else:
                layers_map[layer].append(self.all_layers[neuron])
            
        self.by_layer = layers_map

    def get_connections(self):
        return self.connections

    def get_input_layer(self):
         return self.input_layer

    def get_output_layer(self):
         return self.output_layer

    def set_connection_weight(self, before_unit, current_unit, weight):
        self.connections[before_unit, current_unit] = value

    def initialize_weights(self):
        for key, weight in self.connections.iteritems():
            self.connections[key] = random.random()

    def get_connection_weight(self, pair):
        #Gets connection weight from tuple of (before_unit, current_unit)
        return self.connections[pair]

    def get_neuron(self, name):
        return self.all_layers[name]

    def get_neurons_by_layer(self, layer):
        this_layer = []
        for neuron in self.all_layers:
            if self.all_layers[neuron].get_layer() == layer:
                this_layer.append(self.all_layers[neuron])
        return this_layer

    def create_weights(self):
        for neuron in self.all_layers:
            if self.all_layers[neuron].get_layer() > 0:
                layer         = self.all_layers[neuron].get_layer()
                current_layer = self.get_neurons_by_layer(layer)
                inputs        = self.get_neurons_by_layer(layer - 1)

            #iterate through before layer and create connections
                for before_unit in inputs:
                    self.connections[before_unit, self.all_layers[neuron]] = random.random()
            #add connections to unit property
                    self.all_layers[neuron].add_connection(before_unit)

    def spread_activation(self):
        #Go through network and sum inputs on each neuron
        network = self.all_layers
        #Get inputs for each neuron
        for neuron in network:
            if network[neuron].get_layer() > 0:
                current_unit = network[neuron]
                self.sum_inputs(current_unit)

    def set_all_before_layers(self):
        #sets before layer value for every layer after layer 0
        for neuron in self.all_layers:
            if self.all_layers[neuron].get_layer() > 0:
                layer         = self.all_layers[neuron].get_layer()
                current_layer = self.get_neurons_by_layer(layer)
                inputs        = self.get_neurons_by_layer(layer - 1)
                self.all_layers[neuron].set_before_layer(inputs)

    def test_layers(self):
        network = self.all_layers
        sameness = 0
        for unit in network:
            unit_before = network[unit].get_before_layer()
            unit_by_layer = self.get_neurons_by_layer(network[unit].get_layer() - 1)
            print "======"
            print "Current unit = " + str(network[unit])
            print "Unit before = " + str(unit_before)
            print "Unit by layer = " + str(unit_by_layer)
            print ""
            if unit_before == unit_by_layer:
                print "Layers are the same"
                sameness += 1
            print ""
            print "Sameness = " + str(sameness)

    def test_set_input_activation(self):
        #get input layer
        input_layer = self.get_neurons_by_layer(0)
        for neuron in input_layer:
            activation = random.random()
            neuron.set_activation(activation)
            print "test activation = " + str(activation)

    def sum_inputs(self, neuron):
        #Get inputs
        total_activation = 0
        inputs = neuron.get_before_layer()
        #Add all inputs, multiplied by their connection weighting
        for unit in inputs:
            for connection in inputs:
                total_activation += (unit.get_activation() * self.get_connection_weight((unit, neuron)))
        output = neuron.sigmoid(total_activation)
        neuron.set_activation(output)

    def sum_inputs_test(self, neuron):
        #Get inputs
        total_activation = 0
        inputs = neuron.get_before_layer()
        print str(neuron) + "'s " + "inputs = " + str(inputs)
        #Add all inputs, multiplied by their connection weighting
        for unit in inputs:
            print "incoming unit = " + str(unit.get_name())
            print "Before activation = " + str(unit.get_activation())
            print "Before weight from input: " + str(unit.get_name()) + " = " + str(self.get_connection_weight((unit, neuron)))
            for connection in inputs:
                total_activation += (unit.get_activation() * self.get_connection_weight((unit, neuron)))
        print "x sum = " + str(total_activation)
        output = neuron.sigmoid(total_activation)
        neuron.set_activation(output)
        print "After activation = " + str(neuron.get_activation())
        print "=============="
        print ""

    def get_connections_by_neuron(self, neuron):
        print neuron.get_before_layer()

    def net_as_json(self):
        dic = {}
        dic['hidden_units'] = {}
        dic['input_units']  = {}
        dic['output_units'] = {}
        dic['connections']  = {}
        
        #convert connections tuples into neuron names and maps neurons with connection weights
        for neuron in self.all_layers:
            name = self.all_layers[neuron].get_name()
            before = self.all_layers[neuron].get_before_layer()
            temp_list = []
            map_list  = []

            for unit in before:
                #make tuple from current and before neuron
                pair = [unit,self.all_layers[neuron]]
                tupe_pair = tuple(pair)
                #place dictionaries here for later appending to single key
                temp = {str(name) : {str(unit.get_name()) : str(self.get_connection_weight(tupe_pair))} }
                temp_list.append(temp)
            
            for mapping in temp_list:
                map_list.append(mapping)
            
            dic['connections'][str(name)] = map_list

        for neuron in self.hidden_units:
            name = self.hidden_units[neuron].get_name()
            dic['hidden_units'][str(name)] = str(self.hidden_units[neuron].get_activation())

        for neuron in self.input_layer:
            name = self.input_layer[neuron].get_name()
            dic['input_units'][str(name)] = str(self.input_layer[neuron].get_activation())

        for neuron in self.output_layer:
            name = self.output_layer[neuron].get_name()
            dic['output_units'][str(name)] = str(self.output_layer[neuron].get_activation())

        string_dic = str(dic)
        json_from_dic = string_dic.replace("'", '"')
        return json_from_dic





