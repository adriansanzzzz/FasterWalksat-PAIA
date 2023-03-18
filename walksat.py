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


def get_random_interpretation(n_vars):
    return [i if random.randrange(2) == 0 else -i for i in range(n_vars + 1)]
    #return {i: i if random.random() < 0.5 else -i for i in range(n_vars + 1)}


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_in_clauses, interpretation, omega=1):
    break_min = sys.maxsize
    best_literals = []
    for literal in clause:
        break_score = 0
        if interpretation[abs(literal)] < 0:
            for clause_index in lit_in_clauses[-abs(literal)]:
                if true_sat_lit[clause_index] == 1:
                    break_score += 1
                elif true_sat_lit[clause_index] == 0:
                    break_score -= 1
        else:
            for clause_index in lit_in_clauses[abs(literal)]:
                if true_sat_lit[clause_index] == 1:
                    break_score += 1
                elif true_sat_lit[clause_index] == 0:
                    break_score -= 1
        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)
    if break_min != 0 and random.random() < omega:
        return random.sample(clause, 1)[0]
    else:
        return random.sample(best_literals, 1)[0] if best_literals else None


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0] * len(clauses)
    for clause_index, clause in enumerate(clauses):
        for literal in clause:
            if interpretation[abs(literal)] == literal:
                true_sat_lit[clause_index] += 1
    return true_sat_lit


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = len(clauses) * max_flips_proportion * n_vars
    interpretation = get_random_interpretation(n_vars)
    true_sat_lit = get_true_sat_lit(clauses, interpretation)
    for i in range(max_flips):
        unsatisfied_clauses_index = [i for i, c in enumerate(clauses) if true_sat_lit[i] == 0]
        if not unsatisfied_clauses_index:
            return interpretation
        clause_index = random.sample(unsatisfied_clauses_index, 1)[0]
        unsatisfied_clause = clauses[clause_index]
        lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause, interpretation)
        if lit_to_flip is None:
            return None
        update_tsl(lit_to_flip, true_sat_lit, lit_clause)
        interpretation[abs(lit_to_flip)] = -interpretation[abs(lit_to_flip)]


if __name__ == '__main__':
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    solution = run_sat(clauses, n_vars, lit_clause)
    print('s SATISFIABLE')
    print('v ' + ' '.join(map(str, solution[1:])) + ' 0')