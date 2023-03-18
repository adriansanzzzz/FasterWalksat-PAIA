import random
import sys

def parse(filename):
    clauses = []
    count = 0
    for line in open(filename):
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in range(n_vars * 2 + 1)]
            continue
        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause


def random_inter(n_vars):
    return [i if random.randrange(2) == 0 else -i for i in range(n_vars + 1)]


def true_literals(clauses, interpretation):
    literals = [0] * len(clauses)
    for i, clause in enumerate(clauses):
        for literal in clause:
            if interpretation[abs(literal)] == literal:
                literals[i] += 1
    return literals



def update_literals(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1



def compute_break(clause, true_sat_lit, lit_in_clauses, omega=0.15):
    best_literals = []
    break_min = sys.maxsize
    for literal in clause:
        break_score = 0
        for clause_index in lit_in_clauses[-abs(literal)]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1
        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)
    if random.random() < omega:
        return random.choice(best_literals)
    else:
        return random.choice(clause)




def sat(clauses, n_vars, lit_clause, max_flips_proportion=13):
    max_flips = max_flips_proportion * n_vars * len(clauses)
    interpretation = random_inter(n_vars)
    true_lit = true_literals(clauses, interpretation)
    for _ in range(max_flips):
        unsatisfied_clauses = [i for i, x in enumerate(true_lit) if x == 0]
        if not unsatisfied_clauses:
            return interpretation
        clause_to_fix = random.choice(unsatisfied_clauses)
        literal_to_flip = compute_break(clauses[clause_to_fix], true_lit, lit_clause)
        if literal_to_flip is None:
            return None
        interpretation[abs(literal_to_flip)] *= -1
        update_literals(literal_to_flip, true_lit, lit_clause)

    return None


if __name__ == '__main__':
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    solution = sat(clauses, n_vars, lit_clause)
    print('s SATISFIABLE')
    print('v ' + ' '.join(map(str, solution[1:])) + ' 0')