# pymatica/matrix_operations.py

class MatrixOperations:
    @staticmethod
    def add(A, B):
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def subtract(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def multiply(A, B):
        n, m, p = len(A), len(A[0]), len(B[0])
        result = [[0] * p for _ in range(n)]
        for i in range(n):
            for j in range(p):
                result[i][j] = sum(A[i][k] * B[k][j] for k in range(m))
        return result

    @staticmethod
    def transpose(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    @staticmethod
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        det = 0
        for c in range(n):
            # Create submatrix for minor
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += ((-1) ** c) * matrix[0][c] * MatrixOperations.determinant(submatrix)
        return det
