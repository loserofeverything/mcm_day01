import numpy as np
import matplotlib.pyplot as plt


def bar_anal(bitcoin):
    plt.xticks(())
    plt.yticks(())
    bar_cnt = np.arange(7)
    dic = ['mean', 'std', 'var', 'min', 'max', 'argmin', 'argmax']
    Y = np.array([np.mean(bitcoin), np.std(bitcoin), np.var(bitcoin), np.min(bitcoin), np.max(bitcoin), np.argmin(bitcoin), np.argmax(bitcoin)])
    plt.bar(bar_cnt, Y, facecolor = '#9999ff', edgecolor = 'white')
    for x, y in zip(bar_cnt, Y):
        plt.text(x + 0.4, y +0.05, '%s : %.2f' %(dic[x] ,y), ha = 'center', va = 'bottom')
    plt.show()

