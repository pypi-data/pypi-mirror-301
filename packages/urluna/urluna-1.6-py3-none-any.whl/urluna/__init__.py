from .flex import Flex
from .operator import Operator

fill_array = Flex.fill_array
sorted_random_array = Flex.sorted_random_array
random_array = Flex.random_array
range_array = Flex.range_array
zeros_array = Flex.zeros_array
ones_array = Flex.ones_array
identity_matrix = Flex.identity_matrix
diagonal_matrix = Flex.diagonal_matrix

add_arrays = Operator.add_arrays
subtract_arrays = Operator.subtract_arrays
transpose = Operator.transpose
multiply_matrices = Operator.multiply_matrices
determinant = Operator.determinant
inverse_matrix = Operator.inverse_matrix
hadamard_product = Operator.hadamard_product
scalar_multiply = Operator.scalar_multiply
power_matrix = Operator.power_matrix
trace = Operator.trace
norm_vector = Operator.norm_vector
