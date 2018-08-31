import numpy as np
from deap import creator, base, tools, algorithms


class Optimisation:

    def __init__(self, p_m, p_m2, p_c):
        self.p_m = p_m
        self.p_m2 = p_m2
        self.p_c = p_c

        self.n_room = 10

    def eval(self, ind): # TODO taking into account user and museum preferences
        s = 0
        for r in ind:
            s += sum(r[1])
        return len(ind), s

    def crossover(self, ind1, ind2):
        r_ind1 = [p[0] for p in ind1]
        r_ind2 = [p[0] for p in ind2]
        i_ind1 = [p[1] for p in ind1]
        i_ind2 = [p[1] for p in ind2]

        x, y = np.sort(np.random.choice(range(len(r_ind1)), 2))
        first_part = r_ind1[x:y]
        second_part = list(filter(lambda x: x not in first_part, r_ind2))
        r_child = first_part + second_part

        i_child = [0 for k in range(len(r_child))]
        for i, r in enumerate(r_child):
            if (r in r_ind1) and (r in r_ind2):
                i_ind = i_ind1[r_ind1.index(r)]
                x = np.random.choice(range(len(i_ind)))
                i_child[i] = i_ind1[r_ind1.index(r)][:x] + i_ind2[r_ind2.index(r)][x:]
            elif r in r_ind1:
                i_child[i] = i_ind1[r_ind1.index(r)]
            else:
                i_child[i] = i_ind2[r_ind2.index(r)]

        return creator.Individual(list(zip(r_child, i_child)))

    def mate(self, ind1, ind2):
        return self.crossover(ind1, ind2), self.crossover(ind2, ind1)

    def mutate(self, ind):
        n = len(ind)
        x, y = np.sort(np.random.choice(range(n), 2))
        ind[x], ind[y] = ind[y], ind[x]
        z = np.random.choice(range(n))
        for i,j in enumerate(ind[z][1]):
            ind[z][1][i] = np.abs(j - 1) if np.random.random() < self.p_m2 else j

        return creator.Individual(ind),

    def init_pop(self, n_ind=10):
        pop = []
        for i in range(n_ind):
            n_r = np.random.choice(range(self.n_room))
            rooms = np.random.choice(range(self.n_room), n_r + 1, replace=False)
            items = [np.random.randint(2, size=5).tolist() for _ in range(n_r)]
            pop.append(list(zip(rooms, items)))

        return pop

    def make_ind(self):
        n_r = np.random.choice(range(self.n_room))
        rooms = np.random.choice(range(self.n_room), n_r + 1, replace=False)
        items = [np.random.permutation(5).tolist() for _ in range(n_r + 1)]
        return creator.Individual(list(zip(rooms, items)))

    def make_path(self, n_gen, n_ind):

        creator.create("FitnessMulti", base.Fitness, weights = (-1.0, 1.0))
        creator.create("Individual", list, fitness = creator.FitnessMulti)

        toolbox = base.Toolbox()
        toolbox.register("individual", self.make_ind)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=n_ind)
        toolbox.register("evaluate", self.eval)
        toolbox.register("mate", self.mate)
        toolbox.register("mutate", self.mutate)
        toolbox.register("select", tools.selNSGA2)

        pop = toolbox.population()
        fits = toolbox.map(toolbox.evaluate, pop)
        for fit, ind in zip(fits, pop):
            ind.fitness.value = fit

        for gen in range(n_gen):
            offspring = algorithms.varOr(pop, toolbox, n_ind, self.p_c, self.p_m)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.value = fit
            pop = toolbox.select(offspring + pop, k=n_ind)

        return [(p, self.eval(p)) for p in pop]
