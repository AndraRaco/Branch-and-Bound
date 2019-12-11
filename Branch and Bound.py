# Implementaţi un algoritm bazat pe metoda Branch and Bound
# pentru rezolvarea problemei rucsacului - varianta discretă sau pentru determinarea unui circuit
# hamiltonian minim TSP(v. curs)


import heapq


class Nod:
    def __init__(self, indice, traseu, mat_redusa, cost, nr):
        self.indice = indice  # ce valoare e rep din matrice
        self.traseu = traseu  # vector de perechi p(nr,cost)
        self.mat_redusa = mat_redusa
        self.cost = cost
        self.nr = nr  # nr la care s-a ajuns in arbore

    def __eq__(self, other):
        return (self.cost == other.cost)

    def __lt__(self, other):
        return (self.cost < other.cost)

    def __gt__(self, other):
        return (self.cost > other.cost)

# functie pentru a adauga un nod (i,j) //de la i la j


def new_nod(parent_M, traseu, nr, i, j):

    # Cream mat_redusa si punem pe linia i si coloana j INF
    # mat_redusa = np.copy(parent_M)  # copiez frumos incet
    mat_redusa = []
    for l in range(n):
        aux = []
        for k in range(n):
            aux.append(parent_M[l][k])
        mat_redusa.append(aux)

    for k in range(n):
        if nr == 0:
            break
        mat_redusa[i][k] = 'INF'

        mat_redusa[k][j] = 'INF'
    if nr != 0:
        mat_redusa[j][i] = 'INF'
    cost = 0  # nu a fost calculat inca
    t = []
    for l in traseu:
        t.append(l)
    nod = Nod(j, t, mat_redusa, cost, nr)
    return nod


# functii pentru a reduce matricea a.i. sa fie un 0 pe fiecare linie
def linie_reducere(M, n):
    v = ['INF'] * n  # in v punem valoarea minima din fiecare linie

    # formam v-ul
    for i in range(n):
        for j in range(n):
            if v[i] == 'INF':
                v[i] = M[i][j]
            if M[i][j] == 'INF':
                continue
            elif v[i] > M[i][j]:
                v[i] = M[i][j]

    # scadem valorile minime
    for i in range(n):
        for j in range(n):
            if v[i] == 'INF':
                continue
            if M[i][j] == 'INF':
                continue
            M[i][j] -= v[i]
    return v

# functii pentru a reduce matricea a.i. sa fie un 0 pe fiecare coloana


def coloana_reducere(M, n):
    v = ['INF'] * n  # in v punem valoarea minima din fiecare coloana

    # formam v-ul
    for i in range(n):
        for j in range(n):
            if v[j] == 'INF':
                v[j] = M[i][j]
            if M[i][j] == 'INF':
                continue
            elif v[j] > M[i][j]:
                v[j] = M[i][j]

    # scadem valorile minime
    for i in range(n):
        for j in range(n):
            if v[j] == 'INF':
                continue
            if M[i][j] == 'INF':
                continue
            M[i][j] -= v[j]
    return v

# Functie de calculat cost minim


def calc_Cost(M, n):
    cost = 0
    # reducem matricea
    l = linie_reducere(M, n)
    c = coloana_reducere(M, n)

    for i in range(n):
        if l[i] != 'INF':
            cost += l[i]
        if c[i] != 'INF':
            cost += c[i]
    return cost


def TSP(costM, n):
    # folosim coada de prioritati ca sa retinem ce noduri sunt acum in arbore
    h = []
    heapq.heapify(h)
    traseu = []
    # cream radacina si ii calculam costul, incepem din 0
    mat_redusa = []
    for i in range(n):
        aux = []
        for j in range(n):
            aux.append(costM[i][j])
        mat_redusa.append(aux)
    root = new_nod(mat_redusa, traseu, 0, -1, 0)
    root.cost = calc_Cost(root.mat_redusa, n)
    # Aduagam radacina la lista cu noduri active
    heapq.heappush(h, (root.cost, root))

    # Gaseste un nod activ cu cost minim
    # Adauga copii lui la lista de noduri active
    # Si dupa il stergem din lista
    while h:
        min = heapq.heappop(h)
        # Dupa ce scot min, sterg tot ce era in heap  si actualizez traseul
        h = []  # suprasciu h-ul
        heapq.heapify(h)
        if min[1].indice != 0:
            if len(min[1].traseu) == 0:
                min[1].traseu.append((0, min[1].indice))
            else:
                min[1].traseu.append(
                    (min[1].traseu[len(traseu)-1][1], min[1].indice))
        i = min[1].indice  # nr pe actual
        if min[1].nr == n - 1:  # daca toate orasele sunt visitate
            # ne intoarcem la inceput
            min[1].traseu.append((i, 0))
            # Afisam Traseul si costul
            print("Traseul este: ")
            print(min[1].traseu)
            print("Costul traseului %d" % min[1].cost)

        # facem pt fiecare copil al minimului
        # (i,j) muchie in arbore
        for j in range(n):
            if min[1].mat_redusa[i][j] != 'INF':
                # cream un nod si ii calculam costul
                copil = new_nod(min[1].mat_redusa,
                                min[1].traseu, min[1].nr + 1, i, j)
                copil.cost = min[1].cost + int(min[1].mat_redusa[i][j]) + \
                    calc_Cost(copil.mat_redusa, n)
                # Adugam copiul in lista cu noduri active
                heapq.heappush(h, (copil.cost, copil))
                # traseu.append(min[1].indice)


# n = 4  # nr linii si coloane
# Mat = [
#     ['INF', 5,   4,   3],
#     [3,   'INF', 8,   2],
#     [5,   3,   'INF', 9],
#     [6,   4,   3,   'INF']
# ]  # cost 12

# n = 5
# Mat =\
#     [
#         ['INF', 10,  8,   9,   7],
#         [10,  'INF', 10,  5,   6],
#         [8,   10,  'INF', 8,   9],
#         [9,   5,   8,   'INF', 6],
#         [7,   6,   9,   6,   'INF']
#     ]
# # cost 34

n = 4
Mat =\
    [
        ['INF', 2,   1,   'INF'],
        [2,   'INF', 4,   3],
        [1,   4,   'INF', 2],
        ['INF', 3,   2,   'INF']
    ]
# cost 8

# n = 5
# Mat =\
#     [
#         ['INF', 3,   1,   5,   8],
#         [3,   'INF', 6,   7,   9],
#         [1,   6,   'INF', 4,   2],
#         [5,   7,   4,   'INF', 3],
#         [8,   9,   2,   3,   'INF']
#     ]
# # cost 16

TSP(Mat, n)
