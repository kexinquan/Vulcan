"""Define utility functions used by models."""
import torch
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from collections import OrderedDict as odict


def round_list(raw_list, decimals=4):
    """
    Return the same list with each item rounded off.

    Parameters
    ----------
    raw_list : float list
        float list to round.
    decimals : int
        How many decimal points to round to.

    Returns
    -------
    rounded_list : float list
        The rounded list in the same shape as raw_list.

    """
    return [round(item, decimals) for item in raw_list]


def get_confusion_matrix(predictions, targets):
    """
    Calculate the confusion matrix for classification network predictions.

    Parameters
    ----------
    predictions : numpy.ndarray
        The classes predicted by the network. Does not take one hot vectors.
    targets : numpy.ndarray
        the classes of the ground truth. Does not take one hot vectors.

    Returns
    -------
    confusion_matrix : numpy.ndarray
        The confusion matrix.

    """
    if len(predictions.shape) == 2:
        predictions = predictions[:, 0]
    if len(targets.shape) == 2:
        targets = targets[:, 0]
    return confusion_matrix(y_true=targets,
                            y_pred=predictions)


def get_one_hot(in_matrix):
    """
    Reformat truth matrix to same size as the output of the dense network.

    Parameters
    ----------
    in_matrix : numpy.ndarray
        The categorized 1D matrix

    Returns
    -------
    one_hot : numpy.ndarray
        A one-hot matrix representing the categorized matrix

    """
    if in_matrix.dtype.name == 'category':
        custom_array = in_matrix.cat.codes

    elif isinstance(in_matrix, np.ndarray):
        custom_array = in_matrix

    else:
        raise ValueError("Input matrix cannot be converted.")

    lb = LabelBinarizer()
    return np.array(lb.fit_transform(custom_array), dtype='float32')

def get_size(summary_dict, output):
    """
    Helper function for the BaseNetwork's get_output_shapes
    """
    if isinstance(output, tuple):
        for i in range(len(output)):
            summary_dict[i] = odict()
            summary_dict[i] = get_size(summary_dict[i], output[i])
    else:
        summary_dict['output_shape'] = list(output.size())
    return summary_dict

def cast_spatial_dim_as(tensor, cast_shape):
    # TODO: https://github.com/pytorch/pytorch/issues/9410
    # Ignore batch for incoming tensor
    n_unsqueezes = len(cast_shape) - len(tensor.shape[2:])
    # For each missing dim, add dims until it
    # is equivalient to the max dim
    for _ in range(n_unsqueezes):
        tensor = tensor.unsqueeze(dim=2)
    # return tensor[(None,) * n_unsqueezes]
    return tensor
