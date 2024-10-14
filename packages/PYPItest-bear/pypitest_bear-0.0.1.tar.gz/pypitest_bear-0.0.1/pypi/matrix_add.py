import numpy as np

def add(matrix1, matrix2):
    # 将输入列表转换为numpy数组
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)

    # 检查输入矩阵的大小是否为3x3
    if matrix1.shape != (3, 3) or matrix2.shape != (3, 3):
        raise ValueError("输入的矩阵必须是3x3的大小")

    # 计算矩阵和
    result = matrix1 + matrix2
    return result