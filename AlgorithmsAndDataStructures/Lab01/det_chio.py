# SKOŃCZONE

class Matrix:
    def __init__(self, list_or_tuple, parameter=0):
        self.parameter = parameter

        if isinstance(list_or_tuple, tuple):     # describes situation when input matrix is tuple
            matrix = []
            for i in range(list_or_tuple[0]):
                single_row = []
                for j in range(list_or_tuple[1]):
                    single_row.append(parameter)
                matrix.append(single_row)

            self.__matrix = matrix

        else:                                   # describes situation when input matrix is tuple
            self.__matrix = list_or_tuple

    def __getitem__(self, item):
        return self.__matrix[item]

    def __setitem__(self, key, value):
        self.__matrix[key] = value

    def __add__(self, other):
        self_size_row, self_size_col = self.size()       # assign size of first matrix
        other_size_row, other_size_col = other.size()    # assign size of second matrix

        sum_matrix = Matrix(self.size())

        if self_size_row == other_size_row and self_size_col == other_size_col:    # checking sizes of added matrixes
            for i in range(self_size_row):
                for j in range(self_size_col):
                    sum_matrix[i][j] += self.__matrix[i][j] + other.__matrix[i][j]

        else:        # wrong sizes
            sum_matrix = None

        return sum_matrix

    def __mul__(self, other):
        self_size_row, self_size_col = self.size()       # assign size of first matrix
        other_size_row, other_size_col = other.size()    # assign size of second matrix

        mul_matrix = Matrix((self_size_row, other_size_col))

        if self_size_col == other_size_row:        # checking sizes of multiplication matrixes
            for i in range(self_size_row):
                # iterate through columns of other
                for j in range(other_size_col):
                    # iterate through rows of other
                    for k in range(other_size_row):
                        mul_matrix[i][j] += self.__matrix[i][k] * other.__matrix[k][j]

        else:        # wrong sizes
            mul_matrix = None

        return mul_matrix

    def __str__(self):
        string = ''
        for row in self.__matrix:   # print every row
            string += f'{row}\n'
        return string

    def size(self):
        return len(self.__matrix), len(self.__matrix[0])


def det(input_matrix: Matrix):

    def det2x2(a11, a12, a21, a22):      # operate only matrix 2x2
        return a11 * a22 - a12 * a21

    def det_inside(matrix: Matrix, factor=1):    # recursive function
        # factor parameter is coefficient by which we multiply matrix at the end
        row_size, col_size = matrix.size()

        if matrix[0][0] == 0:
            # if first element is 0 changing columns or rows between each other
            # in this case coefficient is inverse
            matrix[0], matrix[1] = matrix[1], matrix[0]
            factor *= -1

        if matrix.size() == (2, 2):
            return factor * det2x2(matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1])

        else:
            # chio algorithm
            smaller_matrix = Matrix((row_size - 1, col_size - 1))
            factor *= 1 / matrix[0][0] ** (row_size - 2)

            for i in range(row_size - 1):
                for j in range(col_size - 1):
                    smaller_matrix[i][j] = det2x2(matrix[0][0], matrix[0][j+1], matrix[i+1][0], matrix[i+1][j+1])

            return det_inside(smaller_matrix, factor)

    if input_matrix.size()[0] == input_matrix.size()[1]:    # checking if matrix is square
        return det_inside(input_matrix)

    else:
        return 'Matrix have not the same dimension'


if __name__ == '__main__':
    m1 = Matrix([[5, 1, 1, 2, 3],
                 [4, 2, 1, 7, 3],
                 [2, 1, 2, 4, 7],
                 [9, 1, 0, 7, 0],
                 [1, 4, 7, 2, 2]])

    m2 = Matrix([[0, 1, 1, 2, 3],
                 [4, 2, 1, 7, 3],
                 [2, 1, 2, 4, 7],
                 [9, 1, 0, 7, 0],
                 [1, 4, 7, 2, 2]])

    print(det(m1))
    print(det(m2))
