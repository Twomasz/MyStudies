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


def transpose(matrix: Matrix) -> Matrix:
    change_matrix = Matrix((matrix.size()[1], matrix.size()[0]))

    for i in range(matrix.size()[1]):
        for j in range(matrix.size()[0]):
            change_matrix[i][j] = matrix[j][i]
    return change_matrix


if __name__ == '__main__':
    m1 = Matrix([[1, 0, 2], [-1, 3, 1]])
    m2 = Matrix((2, 3), 1)
    m3 = Matrix([[3, 1], [2, 1], [1, 0]])

    print('Macierz m1 wygląda tak:\n', m1)
    print('Transpozycja macierzy m1 wygląda tak:\n', transpose(m1))
    print('Przykład dodawania macierzy:\n', m1 + m2)
    print('Przykład mnożenia macierzy:\n', m1 * m3)
