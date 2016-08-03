


import numpy as np
import lasagne
import time

import sys
from print_n_plot import print_train_results,plot_learn_curve,print_val_results, plot_reconstruction
from matplotlib import pyplot as plt



#TODO: adding logging
#TODO add special way of saving run info based on run number or date or something
#TODO add getting weights over updates
def train(datasets,network,train_fn, val_fn,pred_fn=None, num_epochs=50, save_weights=False, save_plots=True, save_path='./results',
          batchsize=128, network_kwargs={}, load_path=None):
    
    """Train function

    Arguments:
        datasets (sequence): tuple or list of x_tr, y_tr, x_val, y_val, x_te, y_te
        num_epochs (int): number of epochs

    Returns:
        lasagne layers instance: The last layer of the network with trained weights

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    #todo add in detect
    x_tr, y_tr, x_val, y_val= datasets
    

    if batchsize is None or x_tr.shape[0] < batchsize:
        batchsize = x_tr.shape[0]

    print "Starting training..." 
    

    train_errs, train_accs, val_errs, val_accs = [], [], [], []
    for epoch in range(num_epochs):
        do_one_epoch(epoch,num_epochs, x_tr, y_tr, x_val, y_val,
                     batchsize, train_fn, val_fn, 
                     train_errs, train_accs, val_errs, val_accs)
        
        if epoch % 10 == 0:
            plot_learn_curve(train_errs,val_errs, 'err', save_plots=save_plots,path=save_path)
            plot_learn_curve(train_accs,val_accs, 'acc', save_plots=save_plots, path=save_path)
            if pred_fn:
                rec = pred_fn(x_tr)
                n_ims = rec.shape[0]
                
                plot_reconstruction(x_tr[:,0], rec[:,0], indx=0,save=save_plots, path=save_path)
                plot_reconstruction(x_tr[:,0], rec[:,0], indx=25,save=save_plots,  path=save_path)
                plot_reconstruction(x_tr[:,0], rec[:,0], indx=50,save=save_plots,  path=save_path)
                plot_reconstruction(x_tr[:,0], rec[:,0], indx=n_ims-1,save=save_plots,  path=save_path)
            #plot weights or updates or something 
            
            
        if save_weights and epoch % 10 == 0:
        # Optionally, you could now dump the network weights to a file like this:
            np.savez('%s.npz'%(mode), *lasagne.layers.get_all_param_values(network))
    return network
        #(train_errs[-1], train_accs[-1], val_errs[-1], val_accs[-1])



def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0,len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx: start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]

def train_one_epoch(x,y,batchsize, train_fn, val_fn):
    train_err = 0
    train_acc = 0
    train_batches = 0
    start_time = time.time()
    for batch in iterate_minibatches(x, y, batchsize, shuffle=True):
        inputs, targets = batch
        train_err += train_fn(inputs, targets)
        _, acc = val_fn(inputs, targets)
        train_acc += acc
        train_batches += 1
    return train_err, train_acc, train_batches

def val_one_epoch(x,y,batchsize, val_fn):
        val_err = 0
        val_acc = 0
        val_batches = 0
        for batch in iterate_minibatches(x,y, batchsize, shuffle=False):
            inputs, targets = batch
            err, acc = val_fn(inputs, targets)
            val_err += err
            val_acc += acc
            val_batches += 1
        return val_err, val_acc, val_batches
def do_one_epoch(epoch,num_epochs, x_train,y_train, x_val, y_val, batchsize, train_fn, val_fn,
                 train_errs, train_accs, val_errs, val_accs):
        start_time = time.time()
        tr_err, tr_acc, tr_batches = train_one_epoch(x_train, y_train,
                                                     batchsize=batchsize,
                                                     train_fn=train_fn,
                                                     val_fn=val_fn)
                
        train_errs.append(tr_err / tr_batches)
        train_accs.append(tr_acc / tr_batches)
        print_train_results(epoch, num_epochs, start_time, tr_err / tr_batches, tr_acc / tr_batches)
        

        val_err, val_acc, val_batches = val_one_epoch(x_val, y_val,
                                                     batchsize=y_val.shape[0],
                                                      val_fn=val_fn)
        val_errs.append(val_err / val_batches)
        val_accs.append(val_acc / val_batches)
        print_val_results(val_err, val_acc / val_batches)
        





