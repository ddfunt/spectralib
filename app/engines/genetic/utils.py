import numpy as np


coords = np.array([[12, 1, 2, 5],
                  [12, 2, 3, 4]])

class Atom:

    def __init__(self, xyz, mass):
        self._x = xyz[0]
        self._y = xyz[1]
        self._z = xyz[2]
        self._mass = mass
        self.vector = [self.mass, self.x, self.y, self.z]

    def __getitem__(self, item):
        return self.vector[item]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.vector[1] = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.vector[2] = value

    @property
    def z(self):
        return self._x

    @z.setter
    def z(self, value):
        self._z = value
        self.vector[2] = value

    @property
    def mass(self):
        return self._x
    @mass.setter
    def mass(self, value):
        self._mass = value
        self.vector[0] = value

    def __repr__(self):
        return '[%s, %s, %s, %s]' % (self.mass, self.x, self.y, self.z)



class Molecule:
    _constants = None
    _tensor = None

    def __init__(self, coords):
        self.coords = coords

    @property
    def tensor(self):
        if not self._tensor:
            coords = self.coords
            matrix = np.array([[0,0,0],
                      [0,0,0],
                      [0,0,0]])
            for atom in coords:

                matrix[0, 0] += atom[0] * (atom[2]**2 + atom[3]**2)
                matrix[1, 1] += atom[0] * (atom[1]**2 + atom[3]**2)
                matrix[2, 2] += atom[0] * (atom[1]**2 + atom[2]**2)
                ab = - atom[0] * (atom[1] * atom[2])
                ac = - atom[0] * (atom[1] * atom[3])
                bc = - atom[0] * (atom[3] * atom[2])
                matrix[0, 1] += ab
                matrix[1, 0] += ab
                matrix[0, 2] += ac
                matrix[2, 0] += ac
                matrix[1, 2] += bc
                matrix[2, 1] += bc
            self._tensor = matrix

        return self._tensor

    @property
    def constants(self, ):
        if not self._constants:
            self._constants = sorted(np.linalg.eig(self.tensor)[0], reverse=True)
        return self._constants


if __name__ == '__main__':


    x = [Atom((1,2,3), 12),
         Atom((2,3,4), 1)]
    print(Molecule(x).constants)
