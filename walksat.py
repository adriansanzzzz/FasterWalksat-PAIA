import random
import sys

def parse(filename):
    with open(filename) as f:
        lines = f.readlines()

    comment_lines = [line for line in lines if line.startswith('c')]
    header_line = next(line for line in lines if line.startswith('p'))
    n_vars = int(header_line.split()[2])
    lit_clause = [[] for _ in range(n_vars * 2 + 1)]

    clauses = []
    for line in lines[len(comment_lines)+1:]:
        clause = [int(literal) for literal in line.split()[:-1]]
        clauses.append(clause)
        for literal in clause:
            lit_clause[literal].append(len(clauses)-1)

    return clauses, n_vars, lit_clause


def random_interpretation(n_vars):
    return [i if random.randrange(2) == 0 else -i for i in range(n_vars + 1)]


def update_literal(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_in_clauses, interpretation, omega=0.4):
    break_min = float('inf')
    best_literals = []
    for literal in clause:
        break_score = 0
        if interpretation[abs(literal)] < 0:
            lit_in_clause = lit_in_clauses[-abs(literal)]
        else:
            lit_in_clause = lit_in_clauses[abs(literal)]
        for clause_index in lit_in_clause:
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

def true_sat_literals(clauses, interpretation):
    literals = [0] * len(clauses)
    for i, clause in enumerate(clauses):
        for literal in clause:
            if -literal in clause:
                break
            if interpretation[abs(literal)] == literal:
                literals[i] += 1
    return literals

def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = len(clauses) * max_flips_proportion * n_vars
    interpretation = random_interpretation(n_vars)
    true_sat_lit = true_sat_literals(clauses, interpretation)
    for i in range(max_flips):
        clause_index = next((i for i, c in enumerate(clauses) if true_sat_lit[i] == 0), None)
        if clause_index is None:
            return interpretation
        unsatisfied_clause = clauses[clause_index]
        lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause, interpretation)
        if lit_to_flip is None:
            return None
        update_literal(lit_to_flip, true_sat_lit, lit_clause)
        interpretation[abs(lit_to_flip)] = -interpretation[abs(lit_to_flip)]

if __name__ == '__main__':
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    solution = run_sat(clauses, n_vars, lit_clause)
    print("s SATISFIABLE \n" + 'v ' + ' '.join(map(str, solution[1:])) + ' 0')