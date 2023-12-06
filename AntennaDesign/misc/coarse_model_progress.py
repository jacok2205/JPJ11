import matplotlib.pyplot as plt
from coarse_model.MicrostripTransmissionLine import get_microstrip_transmission_dimensions
from coarse_model.RectangularMicrostripPatch import get_rmsp_dimensions

__course_model_path__ = '../AntennaDesign/file_system/coarse_model/Generation Fitness Results\\'
__index__ = 0
__data__ = []

if __name__ == '__main__':

    get_microstrip_transmission_dimensions(2.4e9, 3.55, 0.5e-3, 50)
    get_rmsp_dimensions(2.4e9, 0.5e-3, 3.55)

    while True:

        try:

            file = open(__course_model_path__ + f'fitness_generation_{__index__}', 'r')
            __string__ = file.readlines()
            __raw__ = []

            __deliminator__ = ' '

            for __i__ in __string__:
                __pass_character__ = True
                __temp__ = ''

                for __j__ in __i__:
                    if (__j__.isdigit() or __j__ == '.') and not __pass_character__:
                        __temp__ += __j__

                    if __j__ == __deliminator__:
                        __pass_character__ = False

                __raw__.append(float(__temp__))
            __data__.append(sum(__raw__) / len(__raw__))

            file.close()
            __index__ += 1

        except Exception as __error__:

            plt.semilogy(range(len(__data__)), __data__)
            plt.title('Pi-shape slotted Generation Fitness')
            plt.xlabel('Generation')
            plt.ylabel('Average Generation Fitness')
            plt.grid()
            plt.show()

            print(__error__)

            break
