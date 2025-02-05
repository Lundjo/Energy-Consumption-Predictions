from re import VERBOSE

VERBOSE = 1

class AnnBase:
    def __init__(self, epochs, number_of_hidden_layers, neurons_first_layer, neurons_other_layers,
                 batch_size=1, cost_function='mape', optimizer='nadam', kernel_initializer='he_normal',
                 activation_function='leaky_relu'):
        self.epoch_number = epochs
        self.batch_size_number = batch_size
        self.cost_function = cost_function
        self.optimizer = optimizer
        self.kernel_initializer = kernel_initializer
        self.activation_function = activation_function
        self.number_of_hidden_layers = number_of_hidden_layers
        self.number_of_neurons_in_first_hidden_layer = neurons_first_layer
        self.number_of_neurons_in_other_hidden_layers = neurons_other_layers
        self.verbose = VERBOSE

    @property
    def epoch_number(self):
        return self._epoch_number

    @epoch_number.setter
    def epoch_number(self, value):
        self._epoch_number = value

    @property
    def batch_size_number(self):
        return self._batch_size_number

    @batch_size_number.setter
    def batch_size_number(self, value):
        self._batch_size_number = value
    
    #The purpose of loss functions is to compute the quantity that a model should seek to minimize during training.
    #mean_squared_error
    #mean_absolute_error
    #mean_absolute_percentage_error
    #mean_squared_logarithmic_error
    #cosine_similarity
    #huber_loss
    #mean_squared_logarithmic_error
    @property
    def cost_function(self):
        return self._cost_function

    @cost_function.setter
    def cost_function(self, value):
        self._cost_function = value

    #SGD
    #RMSprop
    #adam
    #adadelta
    #adagrad
    #adamax
    #nadam
    #ftrl
    @property
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, value):
        self._optimizer = value
    #Initializers define the way to set the initial random weights of Keras layers.
    #random_normal
    #normal
    #random_uniform
    #zeros
    #ones
    #glorot_normal
    #glorot_uniform
    #he_normal
    #he_uniform
    #identity
    @property
    def kernel_initializer(self):
        return self._kernel_initializer

    @kernel_initializer.setter
    def kernel_initializer(self, value):
        self._kernel_initializer = value

    @property
    def activation_function(self):
        return self._activation_function

    #relu 
    #sigmoid
    #softmax
    #softplus 
    #softsign
    #tanh 
    #selu
    #elu
    #exponential

    @activation_function.setter
    def activation_function(self, value):
        self._activation_function = value

    @property
    def output_activation_function(self):
        return self._output_activation_function

    @output_activation_function.setter
    def output_activation_function(self, value):
        self._output_activation_function = value

    @property
    def number_of_hidden_layers(self):
        return self._number_of_hidden_layers

    @number_of_hidden_layers.setter
    def number_of_hidden_layers(self, value):
        self._number_of_hidden_layers = value

    @property
    def number_of_neurons_in_first_hidden_layer(self):
        return self._number_of_neurons_in_first_hidden_layer

    @number_of_neurons_in_first_hidden_layer.setter
    def number_of_neurons_in_first_hidden_layer(self, value):
        self._number_of_neurons_in_first_hidden_layer = value

    @property
    def number_of_neurons_in_other_hidden_layers(self):
        return self._number_of_neurons_in_other_hidden_layers

    @number_of_neurons_in_other_hidden_layers.setter
    def number_of_neurons_in_other_hidden_layers(self, value):
        self._number_of_neurons_in_other_hidden_layers = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value