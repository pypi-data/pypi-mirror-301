import math
import sympy
from .utilities import decompose_dict, factor_check

class pump:

    def __init__(
        self,
        file,
        dia,
        time=0,
    ):
        self.file = file
        self.dia = dia
        if self.dia < 0.1 or self.dia > 50.0:
            raise Exception('Diameter is invalid. Must be between 0.1 - 50.0 mm')
        self.time = time
        self.loop = []
        self.rate = 0
        if self.dia > 14.0:
            self.vol_units = 'mcL'
        else:
            self.vol_units = 'mL'
        # self.vol_inf=0
        # self.vol_wdr=0
        self.dir = ''
        self.rat = 0


    def init(*args):
        for self in args:
            self.file.write(f"dia {self.dia}\nal 1\nbp 1\nPF 0\n")

    def rate(self, rate: int, vol: int, dir: str):
        self.file.write(f"\nphase\nfun rat\nrat {self.rat} mm\nvol {vol}\ndir {self.dir}\n")
        self.dir = dir
        self.rat = rate
        self.time += vol / rate * 60 * self.getloop()
    
    # def fill(fill, rate:int = self.rat, dir = 0):
    #     self.rat = rate
    #     self.file.write(f"\nphase\nfun fil\nrat {self.rat} mm\ndir {self.dir}\n")
    #     if dir == 0:
    #         if self.dir == 'inf':
    #             self.dir = 'wdr'
    #             self.time += self.vol_inf / rate * 60 * self.getloop()
    #             self.vol_wdr -= 
    #         elif self.dir == 'wdr':
    #             self.dir == 'inf'
    #             self.time += self.vol_wdr / rate * 60 * self.getloop()
    #         else:
    #             raise Exception(f'Error in {self}.dir={self.dir}')
    #     else:
    #         self.dir = dir
    #         if self.dir == 'inf':
    #             self.time += self.vol_inf / rate * 60 * self.getloop()
    #         elif self.dir == 'wdr':
    #             self.time += self.vol_wdr / rate * 60 * self.getloop()
    #         else:
    #             raise Exception(f'Error in {self}.dir={self.dir}')

    # increment

    # decrement

    def beep(self):
        self.file.write(f'\nphase\nfun bep\n')

    def pause(self, length: int):
        if length <= 99:
            self.file.write(f"\nphase\nfun pas {length}\n")
            self.time += length * self.getloop()

        elif length <= 99 * 3:
            self.pas(99)
            self.pas(length - 99)
        else:
            multiples = factor_check(decompose_dict(sympy.factorint(length)))
            if multiples != (0, 0) and len(multiples) <= 3:
                for i in range(len(multiples) - 1):
                    self.loopstart(multiples[1 + i])
                self.pas(multiples[0])
                for i in range(len(multiples) - 1):
                    self.loopend()
            else:
                self.pas(length % 50, self.getloop())
                length -= length % 50
                self.pas(length, self.getloop())

    def loopstart(self, count):
        self.loop.append(count)
        if len(self.loop) > 3:
            raise Exception("Up to three nested loops, you have too many")
        self.file.write(f"\nphase\nfun lps\n")

    def loopend(self):
        self.file.write(f"\nphase\nfun lop {self.loop.pop()}\n")

    def getloop(self):
        if len(self.loop) >= 1:
            return self.loop[-1]
        else:
            return sympy.prod(self.loop)

    def stop(*args):
        for self in args:
            self.file.write(f"\nphase\nfun stp\n")

    def sync(*args):
        max_time = 0
        for arg in args:
            if arg.time > max_time:
                max_time = arg.time
        for arg in args:
            time_diff = max_time - arg.time
            if time_diff > 0:
                arg.pas(math.ceil(time_diff))

