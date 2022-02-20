import numpy as np
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt

lens = 1826
X = np.linspace(0, lens-1, lens)
print(X.shape)
x = sp.symbols('x')
exp1 = 250000 * sp.exp(x/1000)
y = np.array([exp1.subs(x, xi) for xi in X])
print(y)
c = pd.DataFrame(y, columns=['data'])
f = pd.ExcelWriter("wabi.xlsx")
c.to_excel(f,"sheet1")
f.save()