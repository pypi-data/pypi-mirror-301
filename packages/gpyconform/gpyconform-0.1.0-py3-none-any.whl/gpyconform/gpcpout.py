#!/usr/bin/env python3

import torch
import warnings

class gpcpout:
    r"""
    Class containing the returned Conformal Prediction Intervals and providing functionality for 
    their retrieveal and evaluation.

    
    Parameters
    ----------
    conf_levels : torch.Tensor
        Confidence levels of the Prediction Intervals
    out : torch.Tensor
        Prediction Intervals for each confidence level in conf_levels
        (out[i, :, :] corresponds to the Prediction Intervals for conf_levels[i])
    """
    
    def __init__(self, conf_levels, out):
        self.conf_levels = conf_levels
        self.out = out
    
    def __call__(self, conf_level):
        r"""
        Returns the Prediction Intervals for a given confidence level.
        
        Parameters
        ----------
        conf_level : float
            Confidence level for which to return the corresponding Prediction Intervals

        Raises
        ------
        ValueError
            If 'conf_level' is not in the existing confidence levels

        Returns
        -------
        torch.Tensor
            Prediction Intervals for conf_level

        """

        indices = torch.nonzero(self.conf_levels == conf_level, as_tuple=True)[0]
        if indices.numel() > 0:
            return self.out[indices[0], :, :]
        else:
            raise ValueError(f"Confidence level {conf_level} not found. Available levels are: {self.conf_levels.numpy()}")
        
    def evaluate(self, conf_level, metrics=['mean_width', 'median_width', 'error'], y=None):
        r"""
        Evaluate the Prediction Intervals for a given confidence level.

        Parameters
        ----------
        conf_level : float
            Confidence level the Prediction Intervals of which will be evaluated
        metrics : a string or a list of strings, default=['mean_width', 'median_width', 'error']
            List of evaluation metrics to be calculated. Possible metrics include:
            - 'mean_width': the average width of the Prediction Intervals
            - 'median_width': the median width of the Prediction Intervals
            - 'error': percentage of Prediction Intervals not including the true target value
        y : torch.Tensor, default=None
            True target values. If not provided, the 'error' metric will not be calculated.

        Raises
        ------
        ValueError
            If 'conf_level' is not in the existing confidence levels
        RuntimeWarning
            If 'error' is in 'metrics' but 'y' is None, since error calculation requires true target values 
        RuntimeWarning
            If there are strings in `metrics` that do not correspond to any of the defined metrics

        Returns
        -------
        results : dict
            A dictionary where each key corresponds to a metric from `metrics` and each value is the 
            calculated result for that metric. For example, {'mean_width': 0.5, 'error': 0.05}.
        """
        
        unobserved_functions = {
             'mean_width': self.mean_pi_width,
             'median_width': self.median_pi_width
        }
    
        if isinstance(metrics, str):
            metrics = [metrics]
    
        results = {}

        indices = torch.nonzero(self.conf_levels == conf_level, as_tuple=True)[0]
        if indices.numel() > 0:
            conf_index = indices[0]
        else:
            raise ValueError(f"Confidence level {conf_level} not found. Available levels are: {self.conf_levels.numpy()}")
        
        # Check if any metrics require pi_widths before calculating
        pi_widths_required = any(metric in unobserved_functions for metric in metrics)
        if pi_widths_required:
            pi_widths = self.out[conf_index,:,1] - self.out[conf_index,:,0]

        for name in metrics:
            if name == 'error':
                if y is None:
                    warnings.warn("True labels 'y' not provided for error calculation - skipping 'error' metric.", RuntimeWarning)
                else:
                    results['error'] = self.error_percentage(conf_index, y)
            elif name in unobserved_functions:
                result = unobserved_functions[name](conf_index, pi_widths)
                results[name] = result
            else:
                warnings.warn(f"'{name}' is not a recognized metric.", RuntimeWarning)
    
        return results

    def error_percentage(self, conf_index, y):
        r"""
        Return the percentage of errors for a given confidence level.

        Parameters
        ----------
        conf_index : int
            index of the confidence level in conf_levels
        y : torch.Tensor
            True target values

        Returns
        -------
        float
            Percentage of errors (true target value not in Prediction Interval)

        """
        errors = (y < self.out[conf_index,:,0]) | (y > self.out[conf_index,:,1])

        num_errors = torch.sum(errors, dtype=torch.float32)
        total = errors.numel()
        prc_errors = num_errors / total

        return prc_errors.item()

    def mean_pi_width(self, conf_index, pi_widths):
        return pi_widths.mean().item()
    
    def median_pi_width(self, conf_index, pi_widths):
        return pi_widths.median().item()
        