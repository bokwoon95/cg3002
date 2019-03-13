import numpy as np
a = np.array([[0,1], [10,11], [20,21], [30,31], [40,41], [50,51]])
w = np.hstack((a[:-2],a[1:-1],a[2:]))
