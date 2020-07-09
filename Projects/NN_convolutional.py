# -*- coding: utf-8 -*-
"""
Basic convolution layer for neural netwoks

features to add (eventually)
1d support (text)
3d support (colored images)
varied step size

"""


import numpy as np
inp = np.random.rand(10,10)*255 #input image (also work for 1d and 3d- later)

# kernel
k1 = np.random.rand(3,3)

new_image = forward(inp, k1)



def max_pool(arr, shape):
    """
    Parameters
    ----------
    arr : numpy array
        array to pool on
    shape : tuple or list
        region shape to pool over.

    Returns
    -------
    new_image : numpy array
        reduced image.

    """
    
    
    new_image = np.zeros((len(arr[:,0])-shape[0], len(arr[0,:])-shape[1]))

    for i in range(len(arr[:,0]) - shape[0]): # 1s, 2s, and 3s defined by kernel size
        for j in range(len(arr[0,:]) - shape[1]):
            sub_array = np.array(inp_padded[i:i+1+shape[0], j:j+1+shape[0]])

            new_image[i,j] = np.max(sub_array)
            
    return new_image



def forward(inp, k1):
    """
    create a new image by applying a convolutional kernel to an existing one

    Parameters
    ----------
    inp : numpy array
        input image
    k1 : numpy array
        kernel to apply
    k1_border : int
        size of the border

    Returns
    -------
    new_image : numpy array
        image resulting from convolution, keeps padding

    """
    k1_border = ((len(k1[:,0])-1)//2, (len(k1[0,:])-1)//2)

    # input padding
    inp_padded = np.pad(inp, k1_border[0], 'constant')

    new_image = np.zeros(inp_padded.shape)
    for i in range(k1_border[0], len(inp_padded[:,0]) - k1_border[0]): # 1s, 2s, and 3s defined by kernel size
        for j in range(k1_border[1], len(inp_padded[0,:]) - k1_border[1]):

            sub_array = np.array(inp_padded[i-k1_border[0]:i+1+k1_border[0], j-k1_border[1]:j+1+k1_border[1]])
            
            new_image[i,j] = np.sum(np.multiply(k1, sub_array))

    return new_image


