#!/usr/bin/env python
"""Sigmoid Function"""
# from numpy import power, e
# 
# def sigmoid(x_value):
#     """Return the sigmoid value"""
#     return 1.0/(1.0 + power(e, -x_value))
from scipy.special import expit
def sigmoid(x_value):
    return expit(x_value)

