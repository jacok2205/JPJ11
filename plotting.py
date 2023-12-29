from AntennaDesign.filing import Filing
from AntennaDesign.__init__ import *


if __name__ == '__main__':
    filing = Filing(Debugging=True)
    data = filing.Read(Filename='\\SSO\\Test\\Explored')
    print(len(data))
    max_alpha = 0
    for __i__ in data:
        plt.plot(__i__[1][1][0], __i__[1][1][1], alpha=max_alpha / len(data))
        max_alpha += 1
    plt.grid()
    plt.xlabel('Frequency (GHz)')
    plt.show()
    print(random.choice(np.arange(0, 10.1, 0.1)))
