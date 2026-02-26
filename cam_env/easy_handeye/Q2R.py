import numpy as np

def quaternion_to_rotation_matrix(q):
    """
    q: [x, y, z, w]
    return: 3x3 rotation matrix
    """
    x, y, z, w = q

    # 归一化（非常重要）
    norm = np.sqrt(x*x + y*y + z*z + w*w)
    x /= norm
    y /= norm
    z /= norm
    w /= norm

    R = np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w),     2*(x*z + y*w)],
        [2*(x*y + z*w),     1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w),     2*(y*z + x*w),     1 - 2*(x*x + y*y)]
    ])

    return R


# 示例
# q = [0.005, 0.003, -0.399, 0.917]
q = [0.002, 0.000, -0.381, 0.925]
R = quaternion_to_rotation_matrix(q)

print(R)
for row in R:
    print("{:.6f} {:.6f} {:.6f}".format(*row))