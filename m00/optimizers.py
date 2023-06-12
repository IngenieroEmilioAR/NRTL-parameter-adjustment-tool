import random
import numpy as np
import math
import time

# -- PSO

def pso(lb, ub, dim, PopSize, iters, fobj):
    # PSO parameters
    mejor_ruta = []
    Vmax = 6
    wMax = 0.9
    wMin = 0.2
    c1 = 2
    c2 = 2

    vel = np.zeros((PopSize, dim))
    pBestScore = np.zeros(PopSize)
    pBestScore.fill(float("inf"))
    pBest = np.zeros((PopSize, dim))
    gBest = np.zeros(dim)
    gBestScore = float("inf")

    pos = np.random.uniform(0, 1, (PopSize, dim)) * (ub - lb) + lb
    tiempo_inicial = time.time()
    for l in range(0, iters):
        for i in range(0, PopSize):
            pos[i, :] = np.clip(pos[i, :], lb, ub)
            # Calculate objective function for each particle
            fitness = fobj(pos[i, :])
            
            if(pBestScore[i] > fitness):
                pBestScore[i] = fitness
                pBest[i, :] = pos[i, :]

            if(gBestScore > fitness):
                gBestScore = fitness
                gBest = pos[i, :]

        # Update the W of PSO
        w = wMax - l * ((wMax - wMin) / iters)

        for i in range(0, PopSize):
            for j in range(0, dim):
                r1 = random.random()
                r2 = random.random()
                vel[i, j] = w * vel[i, j] + c1 * r1 * \
                    (pBest[i, j] - pos[i, j]) + c2 * r2 * (gBest[j] - pos[i, j])

                if(vel[i, j] > Vmax):
                    vel[i, j] = Vmax

                if(vel[i, j] < -Vmax):
                    vel[i, j] = -Vmax

                pos[i, j] = pos[i, j] + vel[i, j]
        mejor_ruta.append(gBestScore)
    mejor_eval = gBestScore
    tiempo = time.time() - tiempo_inicial
    return mejor_eval, mejor_ruta, gBest, tiempo

def pso_mod(lb, ub, dim, PopSize, iters, fobj):
    # PSO parameters
    mejor_ruta = []
    Vmax = 6
    wMax = 0.9
    wMin = 0.2
    c1 = 2
    c2 = 2

    vel = np.zeros((PopSize, dim))
    pBestScore = np.zeros(PopSize)
    pBestScore.fill(float("inf"))
    pBest = np.zeros((PopSize, dim))
    gBest = np.zeros(dim)
    gBestScore = float("inf")

    pos = np.random.uniform(0, 1, (PopSize, dim)) * (ub - lb) + lb
    tiempo_inicial = time.time()
    for l in range(0, iters):
        for i in range(0, PopSize):
            pos[i, :] = np.clip(pos[i, :], lb, ub)
            # Calculate objective function for each particle
            fitness = fobj(pos[i, :])

            if(pBestScore[i] > fitness):
                pBestScore[i] = fitness
                pBest[i, :] = pos[i, :]

            if(gBestScore > fitness):
                gBestScore = fitness
                gBest = pos[i, :]

        # Update the W of PSO
        w = wMax - l * ((wMax - wMin) / iters)

        for i in range(0, PopSize):
            for j in range(0, dim):
                r1 = random.random()
                r2 = random.random()
                vel[i, j] = w * vel[i, j] + c1 * r1 * \
                    (pBest[i, j] - pos[i, j]) + c2 * r2 * (gBest[j] - pos[i, j])

                if(vel[i, j] > Vmax):
                    vel[i, j] = Vmax

                if(vel[i, j] < -Vmax):
                    vel[i, j] = -Vmax

                pos[i, j] = pos[i, j] + vel[i, j]
        mejor_ruta.append(gBestScore)
    mejor_eval = gBestScore
    tiempo = time.time() - tiempo_inicial
    return mejor_eval, mejor_ruta, gBest, tiempo

# - DE


def de(lb, ub, dim, PopSize, iters, fobj):
    valorMejor = []
    mutation_factor = 0.5
    crossover_ratio = 0.7
    stopping_func = None
    best = float('inf')

    # initialize population
    population = []

    population_fitness = np.array([float("inf") for _ in range(PopSize)])

    for p in range(PopSize):
        sol = []
        for d in range(dim):
            d_val = random.uniform(lb[d], ub[d])
            sol.append(d_val)

        population.append(sol)

    population = np.array(population)

    # calculate fitness for all the population
    for i in range(PopSize):
        fitness = fobj(population[i, :])
        population_fitness[p] = fitness

        # is leader ?
        if fitness < best:
            best = fitness
            leader_solution = population[i, :]

    # start work

    t = 0
    tiempo_inicial = time.time()
    while t < iters:
        # should i stop
        if stopping_func is not None and stopping_func(best, leader_solution, t):
            break

        # loop through population
        for i in range(PopSize):
            # 1. Mutation

            # select 3 random solution except current solution
            ids_except_current = [_ for _ in range(PopSize) if _ != i]
            id_1, id_2, id_3 = random.sample(ids_except_current, 3)

            mutant_sol = []
            for d in range(dim):
                d_val = population[id_1, d] + mutation_factor * (
                    population[id_2, d] - population[id_3, d]
                )

                # 2. Recombination
                rn = random.uniform(0, 1)
                if rn > crossover_ratio:
                    d_val = population[i, d]

                # add dimension value to the mutant solution
                mutant_sol.append(d_val)

            # 3. Replacement / Evaluation

            # clip new solution (mutant)
            mutant_sol = np.clip(mutant_sol, lb, ub)

            # calc fitness
            mutant_fitness = fobj(mutant_sol)
            # s.func_evals += 1

            # replace if mutant_fitness is better
            if mutant_fitness < population_fitness[i]:
                population[i, :] = mutant_sol
                population_fitness[i] = mutant_fitness

                # update leader
                if mutant_fitness < best:
                    best = mutant_fitness
                    leader_solution = mutant_sol

        # increase iterations
        t = t + 1

        valorMejor.append(best)

    # return solution
    tiempo = time.time() - tiempo_inicial
    return best, valorMejor, leader_solution, tiempo

# - CS


def get_cuckoos(nest, best, lb, ub, n, dim):

    # perform Levy flights
    tempnest = np.zeros((n, dim))
    tempnest = np.array(nest)
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) /
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)

    s = np.zeros(dim)
    for j in range(0, n):
        s = nest[j, :]
        u = np.random.randn(len(s)) * sigma
        v = np.random.randn(len(s))
        step = u / abs(v)**(1 / beta)

        stepsize = 0.01 * (step * (s - best))

        s = s + stepsize * np.random.randn(len(s))

        for k in range(dim):
            tempnest[j, k] = np.clip(s[k], lb[k], ub[k])

    return tempnest


def get_best_nest(nest, newnest, fitness, n, dim, objf):
    # Evaluating all new solutions
    tempnest = np.zeros((n, dim))
    tempnest = np.copy(nest)

    for j in range(0, n):
        # for j=1:size(nest,1),
        fnew = objf(newnest[j, :])
        if fnew <= fitness[j]:
            fitness[j] = fnew
            tempnest[j, :] = newnest[j, :]

    # Find the current best

    fmin = min(fitness)
    K = np.argmin(fitness)
    bestlocal = tempnest[K, :]

    return fmin, bestlocal, tempnest, fitness
# Replace some nests by constructing new solutions/nests


def empty_nests(nest, pa, n, dim):

    # Discovered or not
    tempnest = np.zeros((n, dim))

    K = np.random.uniform(0, 1, (n, dim)) > pa

    stepsize = random.random() * (nest[np.random.permutation(n),
                                       :] - nest[np.random.permutation(n), :])

    tempnest = nest + stepsize * K

    return tempnest
##########################################################################


def cs(lb, ub, dim, n, N_IterTotal, objf):
    valorMejor = []

    # Discovery rate of alien eggs/solutions
    pa = 0.25

    nd = dim
    # RInitialize nests randomely
    nest = np.zeros((n, dim))
    for i in range(dim):
        nest[:, i] = np.random.uniform(0, 1, n) * (ub[i] - lb[i]) + lb[i]

    new_nest = np.zeros((n, dim))
    new_nest = np.copy(nest)

    bestnest = [0] * dim

    fitness = np.zeros(n)
    fitness.fill(float("inf"))

    fmin, bestnest, nest, fitness = get_best_nest(nest, new_nest, fitness, n, dim, objf)
    convergence = []
    # Main loop counter
    tiempo_inicial = time.time()
    for iter in range(0, N_IterTotal):
        # Generate new solutions (but keep the current best)

        new_nest = get_cuckoos(nest, bestnest, lb, ub, n, dim)

        # Evaluate new solutions and find best
        fnew, best, nest, fitness = get_best_nest(nest, new_nest, fitness, n, dim, objf)

        new_nest = empty_nests(new_nest, pa, n, dim)

        # Evaluate new solutions and find best
        fnew, best, nest, fitness = get_best_nest(nest, new_nest, fitness, n, dim, objf)

        if fnew < fmin:
            fmin = fnew
            bestnest = best

        valorMejor.append(fmin)
    tiempo = time.time() - tiempo_inicial
    return fmin, valorMejor, bestnest, tiempo

# - GWO


def gwo(lb, ub, dim, SearchAgents_no, Max_iter, fobj):
    valorMejor = []
    # initialize alpha, beta, and delta_pos
    Alpha_pos = np.zeros(dim)
    Alpha_score = float("inf")

    Beta_pos = np.zeros(dim)
    Beta_score = float("inf")

    Delta_pos = np.zeros(dim)
    Delta_score = float("inf")

    # Initialize the positions of search agents
    Positions = np.random.uniform(0, 1, (SearchAgents_no, dim)) * (ub - lb) + lb

    # Main loop
    tiempo_inicial = time.time()
    for l in range(0, Max_iter):
        for i in range(0, SearchAgents_no):

            # Return back the search agents that go beyond the boundaries of the search space
            Positions[i, :] = np.clip(Positions[i, :], lb, ub)

            # Calculate objective function for each search agent
            fitness = fobj(Positions[i, :])

            # Update Alpha, Beta, and Delta
            if fitness < Alpha_score:
                Alpha_score = fitness  # Update alpha
                Alpha_pos = Positions[i, :].copy()

            if (fitness > Alpha_score and fitness < Beta_score):
                Beta_score = fitness  # Update beta
                Beta_pos = Positions[i, :].copy()

            if (fitness > Alpha_score and fitness > Beta_score and fitness < Delta_score):
                Delta_score = fitness  # Update delta
                Delta_pos = Positions[i, :].copy()

        a = 2 - l * ((2) / Max_iter)  # a decreases linearly fron 2 to 0

        # Update the Position of search agents including omegas
        for i in range(0, SearchAgents_no):
            for j in range(0, dim):

                r1 = random.random()
                r2 = random.random()

                A1 = 2 * a * r1 - a
                C1 = 2 * r2

                D_alpha = abs(C1 * Alpha_pos[j] - Positions[i, j])
                X1 = Alpha_pos[j] - A1 * D_alpha

                r1 = random.random()
                r2 = random.random()

                A2 = 2 * a * r1 - a
                C2 = 2 * r2

                D_beta = abs(C2 * Beta_pos[j] - Positions[i, j])
                X2 = Beta_pos[j] - A2 * D_beta

                r1 = random.random()
                r2 = random.random()

                A3 = 2 * a * r1 - a
                C3 = 2 * r2

                D_delta = abs(C3 * Delta_pos[j] - Positions[i, j])
                X3 = Delta_pos[j] - A3 * D_delta

                Positions[i, j] = (X1 + X2 + X3) / 3
        valorMejor.append(Alpha_score)
    tiempo = time.time() - tiempo_inicial
    return Alpha_score, valorMejor, Alpha_pos, tiempo

# - JAYA


def jaya(lb, ub, dim, SearchAgents_no, Max_iter, fobj):

    valorMejor = []
    # Best and Worst position initialization
    Best_pos = np.zeros(dim)
    Best_score = float("inf")

    Worst_pos = np.zeros(dim)
    Worst_score = float(0)

    fitness_matrix = np.zeros((SearchAgents_no))

    # Initialize the positions of search agents

    Positions = np.random.uniform(0, 1, (SearchAgents_no, dim)) * (ub - lb) + lb

    tiempo_inicial = time.time()
    for i in range(0, SearchAgents_no):

        # Return back the search agents that go beyond the boundaries of the search space
        for j in range(dim):
            Positions[i, j] = np.clip(Positions[i, j], lb[j], ub[j])

        # Calculate objective function for each search agent
        fitness = fobj(Positions[i])
        fitness_matrix[i] = fitness

        if fitness < Best_score:
            Best_score = fitness  # Update Best_Score
            Best_pos = Positions[i]

        if fitness > Worst_score:
            Worst_score = fitness  # Update Worst_Score
            Worst_pos = Positions[i]

    # Main loop

    for l in range(0, Max_iter):

         # Update the Position of search agents
        for i in range(0, SearchAgents_no):
            New_Position = np.zeros(dim)
            for j in range(0, dim):

                # Update r1, r2
                r1 = random.random()
                r2 = random.random()

                # JAYA Equation
                New_Position[j] = Positions[i][j] + r1 * (Best_pos[j] - abs(Positions[i, j])) - \
                    r2 * (Worst_pos[j] - abs(Positions[i, j]))

                # checking if New_Position[j] lies in search space
                if New_Position[j] > ub[j]:
                    New_Position[j] = ub[j]
                if New_Position[j] < lb[j]:
                    New_Position[j] = lb[j]

            new_fitness = fobj(New_Position)
            current_fit = fitness_matrix[i]

            # replacing current element with new element if it has better fitness
            if new_fitness < current_fit:
                Positions[i] = New_Position
                fitness_matrix[i] = new_fitness

        # finding the best and worst element
        for i in range(SearchAgents_no):
            if fitness_matrix[i] < Best_score:
                Best_score = fitness_matrix[i]
                Best_pos = Positions[i, :].copy()

            if fitness_matrix[i] > Worst_score:
                Worst_score = fitness_matrix[i]
                Worst_pos = Positions[i, :].copy()
        valorMejor.append(Best_score)

    mejorPos = Best_pos
    mejorRun = Best_score
    tiempo = time.time() - tiempo_inicial
    return mejorRun, valorMejor, Best_pos, tiempo

# - TLBO


def tlbo(lb, ub, dim, ind, iter, fobj):
    valorMejor = []
    # 1 Inicializando la población
    pos = lb + np.random.uniform(0, 1, size=(ind, dim)) * (ub - lb)
    pos_new = np.zeros((ind, dim))
    pos_eval = np.zeros(ind)
    mejor_pos = np.zeros(dim)
    mejor_pos_eval = float('inf')

    tiempo_inicial = time.time()
    for k in range(iter):
        for i in range(ind):
            pos_eval[i] = fobj(pos[i, :])

            if pos_eval[i] <= mejor_pos_eval:
                mejor_pos_eval = pos_eval[i]
                mejor_pos = pos[i, :]

        mean = np.mean(pos, axis=0)
        Tf = round(1 + random.random())
        for i in range(ind):
            pos_new[i, :] = pos[i, :] + np.random.uniform(0, 1, size=dim) * (mejor_pos - Tf * mean)
            pos_new[i, :] = np.clip(pos_new[i, :], lb, ub)

            pos_new_eval = fobj(pos_new[i, :])

            if pos_new_eval < pos_eval[i]:
                pos_eval[i] = pos_new_eval
                pos[i, :] = pos_new[i, :]

        for i in range(ind):
            index1 = random.randint(0, ind - 1)
            if index1 == i:
                while index1 == i:
                    index1 = random.randint(0, ind - 1)

            eval_p = fobj(pos[index1, :])
            if pos_eval[i] < eval_p:
                pos_new[i, :] = pos[i, :] + \
                    np.random.uniform(0, 1, size=dim) * (pos[i, :] - pos[index1, :])

            else:
                pos_new[i, :] = pos[i, :] + np.random.uniform(0, 1) * (pos[index1, :] - pos[i, :])

            pos_new[i, :] = np.clip(pos[i, :], lb, ub)

            eval_n = fobj(pos_new[i, :])

            if eval_n < pos_eval[i]:
                pos_eval[i] = eval_n
                pos[i, :] = pos_new[i, :]
        valorMejor.append(mejor_pos_eval)
    tiempo = time.time() - tiempo_inicial
    return mejor_pos_eval, valorMejor, mejor_pos, tiempo

# - UMDA


def umda(lb, ub, dim, ind, itera, fobj, tau=0.5, evalPerD=2):
    curva = []
    # inicializando la población
    # Cada submatriz es un individuo con sus repeticiones
    pos = np.zeros((ind, evalPerD, dim))
    # print(pos)
    # Inicialización de la selección
    sel = np.zeros((ind, int(evalPerD * tau), dim))
    # print('sel', sel)
    # Inicialización de función objetivo evaluada
    evalPos = np.zeros((ind, evalPerD, 1))
    # print(pos)
    # Evaluación en mejor posición general
    mejorEval = float('inf')
    # Mejor posición general
    mejorPos = np.zeros(dim)

    # Generación de posiciones aleatorias
    tiempo_inicial = time.time()
    for i in range(ind):
        for j in range(evalPerD):
            for k in range(dim):
                pos[i, j, k] = lb[k] + (ub[k] - lb[k]) * random.uniform(0, 1)

    for l in range(itera):
        # Mantener posiciones dentro de los límites
        for i in range(ind):
            for j in range(evalPerD):
                for k in range(dim):
                    pos[i, j, k] = np.clip(pos[i, j, k], lb[k], ub[k])
        # Evaluación de la función objetivo
        # Cada fila son las repeticiones de cada individuo
        for i in range(ind):
            for j in range(evalPerD):
                evalPos[i, j, 0] = fobj(pos[i, j, :])
                if evalPos[i, j, 0] < mejorEval:
                    mejorEval = evalPos[i, j, 0]
                    mejorPos = pos[i, j, :].copy()

        # Selección de individuos
        # Encontrar mejor repetición de cada individuo
        for i in range(ind):
            selIdx = evalPos[i, :, 0].argsort()[:int(tau * evalPerD)]
            # print('selIdx',selIdx)
            selInd = pos[i, selIdx, :]
            # print('selInd',selInd)
            sel[i, :, :] = selInd

        datosSel = sel.reshape(ind * int(evalPerD * tau), dim)
        for i in range(dim):
            mu = np.mean(datosSel[:, i])
            sigma = np.std(datosSel[:, i])
            # Generar nueva población en vector tridimensional
            pos[:, :, i] = sigma * np.random.randn(ind, evalPerD) + mu
        curva.append(mejorEval)
    tiempo = time.time() - tiempo_inicial
    return mejorEval, curva, mejorPos, tiempo

# - WOA


def woa(lb, ub, dim, SearchAgents_no, Max_iter, fobj):
    valorMejor = []

    # initialize position vector and score for the leader
    Leader_pos = np.zeros(dim)
    Leader_score = float("inf")  # change this to -inf for maximization problems

    # Initialize the positions of search agents
    Positions = np.random.uniform(0, 1, size=(SearchAgents_no, dim)) * (ub - lb) + lb

    t = 0  # Loop counter

    # Main loop
    tiempo_inicial = time.time()
    while t < Max_iter:
        for i in range(0, SearchAgents_no):

            # Return back the search agents that go beyond the boundaries of the search space

            # Positions[i,:]=checkBounds(Positions[i,:],lb,ub)
            for j in range(dim):
                Positions[i, j] = np.clip(Positions[i, j], lb[j], ub[j])

            # Calculate objective function for each search agent
            fitness = fobj(Positions[i, :])

            # Update the leader
            if fitness < Leader_score:  # Change this to > for maximization problem
                Leader_score = fitness
                # Update alpha
                Leader_pos = Positions[i, :].copy()  # copy current whale position into the leader position

        a = 2 - t * ((2) / Max_iter)

        a2 = -1 + t * ((-1) / Max_iter)

        # Update the Position of search agents
        for i in range(0, SearchAgents_no):
            r1 = random.random()
            r2 = random.random()

            A = 2 * a * r1 - a
            C = 2 * r2

            b = 1
            l = (a2 - 1) * random.random() + 1

            p = random.random()

            for j in range(0, dim):

                if p < 0.5:
                    if abs(A) >= 1:
                        rand_leader_index = math.floor(
                            SearchAgents_no * random.random()
                        )
                        X_rand = Positions[rand_leader_index, :]
                        D_X_rand = abs(C * X_rand[j] - Positions[i, j])
                        Positions[i, j] = X_rand[j] - A * D_X_rand

                    elif abs(A) < 1:
                        D_Leader = abs(C * Leader_pos[j] - Positions[i, j])
                        Positions[i, j] = Leader_pos[j] - A * D_Leader

                elif p >= 0.5:

                    distance2Leader = abs(Leader_pos[j] - Positions[i, j])
                    # Eq. (2.5)
                    Positions[i, j] = (
                        distance2Leader * math.exp(b * l) * math.cos(l * 2 * math.pi)
                        + Leader_pos[j]
                    )

        t = t + 1

        valorMejor.append(Leader_score)
    tiempo = time.time() - tiempo_inicial
    return Leader_score, valorMejor, Leader_pos, tiempo


def find_nearest(array, value):
    # Find near solution
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def ade(lb, ub, dim, num_ind, num_iter, fobj):
    p_cop_1 = 0.8
    p_cop_2 = 0.55
    valorMejor = []
    best_eval_dum = float("inf")
    # Creating the initial solutions
    pos = lb + (ub - lb) * np.random.uniform(0, 1, size=(num_ind, dim))
    save_eval = np.zeros(num_ind)

    primer_pos = np.zeros(dim)
    primer_pos_eval = float("inf")

    segunda_pos = np.zeros(dim)
    segunda_pos_eval = float("inf")

    tercer_pos = np.zeros(dim)
    tercer_pos_eval = float("inf")

    # Main loop
    tiempo_inicial = time.time()
    for h in range(num_iter):
        # Evaluating the solutions
        pos = np.clip(pos, lb, ub)
        for i in range(num_ind):
            feval = fobj(pos[i, :])
            save_eval[i] = feval

            # Encontrando mejores tres soluciones
            if feval < primer_pos_eval:
                primer_pos_eval = feval  # Update alpha
                primer_pos = pos[i, :].copy()

            if (feval > primer_pos_eval and feval < segunda_pos_eval):
                segunda_pos_eval = feval  # Update beta
                segunda_pos = pos[i, :].copy()

            if (feval > primer_pos_eval and feval > segunda_pos_eval and feval < tercer_pos_eval):
                tercer_pos_eval = feval  # Update delta
                tercer_pos = pos[i, :].copy()

        # Select the best 3 solutions

        # idx_ranked = np.argsort(save_eval)
        best_eval = primer_pos_eval
        if best_eval < best_eval_dum:
            valorMejor.append(best_eval)
        else:
            valorMejor.append(best_eval_dum)

        best_pos = primer_pos.copy()
        best_three_pos = np.array([primer_pos,
                                   segunda_pos,
                                   tercer_pos])

        # best_three_pos = np.array([pos[idx_ranked[0]],
        #                            pos[idx_ranked[1]],
        #                            pos[idx_ranked[2]]])

        # Creating the population A
        list_ind_B = []
        idx_list_indB = []

        for i in range(int(0.5 * num_ind)):
            ind1 = random.randrange(num_ind)
            ind2 = random.randrange(num_ind)

            idx_tour = np.array([ind1, ind2])
            min_idx = np.argmin(save_eval[idx_tour])
            list_ind_B.append(idx_tour[min_idx])
            idx_list_indB.append(min_idx)

        # order_eval = save_eval[idx_ranked]
        mean_eval = np.average(list_ind_B)
        near_mean_pos, idx_mean = find_nearest(list_ind_B, mean_eval)

        d = 1 - (1 / num_iter) * h
        d2 = 1 - (h**2 / num_iter**2)
        for i in range(num_ind):
            if random.random() < p_cop_1:

                G = np.zeros(dim)
                for j in range(dim):
                    idx_random = random.randint(0, 2)
                    r1, r2 = random.random(), random.random()
                    G[j] = best_three_pos[0, j] + d2 * (2 * r1 - 1) * np.abs((2 * r2) * (best_three_pos[idx_random, j] -
                                                                                         pos[i, j]))
                G = np.clip(G, lb, ub)
                if fobj(G) < save_eval[i]:
                    pos[i, :] = G
            else:
                if random.random() < p_cop_2:
                    idx_random = np.random.choice(list(list_ind_B))
                    for j in range(dim):
                        r1, r2 = random.random(), random.random()
                        pos[i, j] = pos[i, j] + d * (2 * r1 - 1) * np.abs((2 * r2) *
                                                                          pos[random.choice(idx_list_indB), j] - pos[i, j])
                else:
                    for j in range(dim):
                        r1, r2 = random.random(), random.random()
                        pos[i, j] = pos[i, j] + d * (2 * r1 - 1) * np.abs((2 * r2) * pos[idx_mean, j] - pos[i, j])

                pos[i, :] = np.clip(pos[i, :], lb, ub)
        best_eval_dum = best_eval

    tiempo = time.time() - tiempo_inicial
    return best_eval, valorMejor, best_pos, tiempo
