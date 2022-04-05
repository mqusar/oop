class Molecule:
    def __init__(self, atoms=None, bonds=None):
        self._atoms = {}  # дандер, cause мы хотим показать тем, кто будет пользоваться кодом чтобы не трогали это
        self._bonds = {}

    def add_atom(self, atom: str, map_=None):
        if atom.upper() not in ("C", "O", "N"):
            raise ValueError
        if not isinstance(map_, int):
            raise TypeError
        if map_ in self._atoms:
            raise KeyError
        if map_ is None:
            n = max(self._atoms, default=0) + 1
            self._atoms[n] = atom.upper()
            self._bonds[n] = {}
        else:
            self._atoms[map_] = atom.upper()
            self._bonds[map_] = {}
        if map_ is not None:
            return map_
        else:
            return n

    def add_bond(self, a1, a2, bt):
        n1 = self._bonds[a1]
        n2 = self._bonds[a2]
        if n1 is n2:
            raise ValueError
        elif a2 in n1:  # проверка на то, что атом уже есть во внутреннем словаре (если есть -> ошибка)
            raise KeyError
        if bt not in (1, 2, 3):
            raise ValueError
        n1[a2] = bt
        n2[a1] = bt

    def rm_atom(self, map_: int):  # нужно написать функцию, которая будет удалять атомы и все связи с этим атомом
        if not isinstance(map_, int):
            raise ValueError
        for a1, a2 in self._bonds.items():
            if map_ is a1 or map_ is a2:
                to_remove = a1
        for a in to_remove:
            del self._bonds[a]
        del self._atoms[map_]

    def get_atom(self, map_: int):
        return self._atoms[map_]

    def get_bond(self, a1, a2):
        return (a1, a2, self._bonds[a1][a2])

    def enumerate_bonds(self, spec: bool = False):  # сделать генератор связей
        seen = set()
        for a1, inner_dict in self._bonds.items():
            for a2, bt in inner_dict.items():
                if spec is False:
                    if (a1, a2, bt) not in seen:
                        seen.add((a1, a2, bt))
                        yield (a1, a2, bt, ("{}-{}".format(self._atoms[a1], self._atoms[a2])))
                else:
                    if (a1, a2, bt) not in seen and (a2, a1, bt) not in seen:
                        seen.add((a1, a2, bt))
                        seen.add((a2, a1, bt))
                        yield (a1, a2, bt, ("{}-{}".format(self._atoms[a1], self._atoms[a2])))

    def enumerate_atoms(self):  # сделать генератор атомов
        for map_, atom in self._atoms.items():
            yield (map_, atom)

    def return_brutto(self):
        brutto = {}
        for atom in self._atoms.values():
            if atom not in brutto:
                brutto.update({atom: 1})
            else:
                brutto[atom] += 1
        br = ""
        for k, v in brutto.items():
            br += k + str(v)
        return br

    def __getitem__(self, map_):
        return self._atoms[map_]

    def __iter__(self):
        return iter([(a1, a2, bt, ("{}-{}".format(self._atoms[a1], self._atoms[a2])))
                     for a1, inner_dict in self._bonds.items()
                     for a2, bt in inner_dict.items()])


a = Molecule(1, 2)

a.add_atom("C", 1)
a.add_atom("C", 2)
a.add_atom("C", 3)
a.add_atom("N", 4)
a.add_atom("C", 5)
a.add_atom("C", 6)

a.add_bond(1, 2, 1)
# a.add_bond(2,1,1)
a.add_bond(2, 3, 1)
a.add_bond(3, 4, 1)
a.add_bond(4, 5, 1)
a.add_bond(5, 6, 1)
a.add_bond(6, 1, 1)
print('===================')
print('instance dictionary:')

print(a.__dict__)
print('===================')
print('get_atom method:')

print(a.get_atom(2))
print('===================')
print('brutto structure:')

print(a.return_brutto())
print('===================')
print('bonds enumeration:')

for i in a.enumerate_bonds(spec=True):
    print(i)

print('===================')
print('atoms enumeration:')

for i in a.enumerate_atoms():
    print(i)
print('===================')
print('getitem:')
print(a[4])

print('===================')
print('iter:')
for i in a:
    print(i)
