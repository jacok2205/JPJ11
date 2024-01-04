from AntennaDesign.filing import Filing
from AntennaDesign.__init__ import *

__use_alpha__ = False

if __name__ == '__main__':
    filing = Filing(Debugging=True)
    data = filing.Read(Filename='\\Surrogate\\lhs')
    max_alpha = 0
    for __i__ in data:
        if __use_alpha__:
            plt.plot(__i__[1][0][0], __i__[1][0][1], alpha=max_alpha / len(data))
        else:
            plt.plot(__i__[1][0][0], __i__[1][0][1])
        max_alpha += 1
    plt.grid()
    plt.xlabel('Frequency (GHz)')
    plt.show()
