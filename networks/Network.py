'''This module contains the base class for a generic neural net interface.

Subclassing this class allows us to stay safe against changes in NN frameworks.
'''

class AbstractNetwork(object):
    '''The base neural network class.
    
    This class defines an interface for neural network subclasses.
    '''
    def __init__(self, *args, **kwargs):
        '''set up network and other params'''
        self.network = None
        self.train_cost = None
        self.test_cost = None
        self.optimizer = None
        self.epoch_loop_hooks = []
        '''This list of functions is called after each epoch is run.
        
           The functions will be called in the order they appear in the list.
           Each function should have a signature of (**kwargs). The provided
           arguments will be included:
           
             - 'cost': the cost
             - 'epoch': the epoch number
             - 'input': the input minibatch
             - 'output': the reconstructed minibatch
        '''

    def fit(self, x_train, y_train):
        '''train network'''
        raise NotImplemented()

    def predict(self, x):
        '''get output'''
        raise NotImplemented()

    def extract_layer(self, data, layer):
        '''extract a certain layer'''
        raise NotImplemented()

    def minibatch_iterator(self, x, y):
        '''iterate over minibatches'''
        raise NotImplemented()

    def preprocess_data(self, x):
        '''get data ready to go into the network'''
        raise NotImplemented()
