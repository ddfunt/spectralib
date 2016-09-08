
proton = 1.00727647
neutron = 1.008664

class Atom:


    @property
    def atomic_mass(self):
        mass = 0
        for m, a in self.isotopes:
            p = self.num
            n = m-p
            print(p, n)
            mass += ((p*proton) + n*neutron) *a
        return mass


class Hydrogen(Atom):
    valene = 1
    radius = 0.25
    num = 1
    mass = 1
    isotopes = [(1, .999885), (2, 0.000115)]

class Helium(Atom):
    valence = 0
    radius = 31
    num = 2
    mass = 4
    isotopes = [(3, 0.00000134), (4, 0.99999866)]


class Carbon(Atom):
    valence = 4
    radius = 0.7
    num = 6
    mass = 12
    isotopes = [(12, 0.9893), (13, 0.0107)]



if __name__ == '__main__':
    c = Carbon()

    h = Hydrogen()
    print(h.isotopes)
    print( h.atomic_mass)
    print(c.atomic_mass)