__author__ = 'racah'
import numpy as np
import os
import pickle
import sys
import h5py
import matplotlib
from sklearn.manifold import TSNE
import numpy as np
matplotlib.use('agg')
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from vis.viz import Viz
from util.helper_fxns import adjust_train_val_test_sizes
from util.data_loaders import load_ibd_pairs
from util.data_loaders import load_dayabay_conv
from LasagneConv import IBDPairConvAe
import logging



# 1) Primary AD           10000 or 1
# 2) Delayed AD response  01000 or 2
# 3) Muon decay           00100 or 3
# 4) Flasher              00010 or 4
# 5) Other (background noise) 00001 or 5


# In[118]:

if __name__ == "__main__":

    #class for networks architecture
    cae = IBDPairConvAe()
    
    h5file = "../dayabay-data-conversion/extract_ibd/ibd_yasu_0_9999.h5"
    #load data from hdf5, preprocess and split into train and test
    preprocess = True
    train, val, test = load_ibd_pairs(h5file, preprocess=preprocess)

    train, _, val, _, test, _  = adjust_train_val_test_sizes(cae.minibatch_size,
        train, train, val, val, test, test)

    #uses scikit-learn interface (so this trains on X_train)
    cae.fit(train)

    #extract the hidden layer outputs when running x_val thru autoencoder
    feat = cae.extract_layer(val, 'bottleneck')[:, :, 0, 0]
    logging.debug('feat.shape = %s', str(feat.shape))
    gr_truth = np.ones(val.shape[0])

    v = Viz(gr_truth)

    # take first two principal components of features, so we can plot easily
    #normally we would do t-SNE (but takes too long for quick demo)
    x_pc = v.get_pca(feat)

    #plot the 2D-projection of the features
    v.plot_features(x_pc,save=True)
