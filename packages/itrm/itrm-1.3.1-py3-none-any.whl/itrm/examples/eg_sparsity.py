import numpy as np
import itrm

N = 50
M = np.random.randn(N, N)
M = M.T @ M
M = (M > 3)
itrm.spy(M, uni=False)
itrm.spy(M, uni=True)
