import random
import sys

def file_parser(filename):
    clauses = []
    count = 0
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            num_vars = int(line.split()[2])
            literal_clause = [[] for _ in range(num_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            literal_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, num_vars, literal_clause


def generate_rnd_interpretation(num_vars):
    return [i if random.randrange(2) == 0 else -i for i in range(num_vars + 1)]


def change_literal_value(literal_to_change, true_sat_lit, literal_clause):
    for index in literal_clause[literal_to_change]:
        true_sat_lit[index] += 1
    for index in literal_clause[-literal_to_change]:
        true_sat_lit[index] -= 1


def compute_literals_in_clause(clause, true_sat_lit, lit_in_clauses, interpretation, omega=0.4):
    break_min = sys.maxsize
    best_literals = []
    for literal in clause:
        break_score = 0
        if interpretation[abs(literal)] < 0:
            lit_in_clause = lit_in_clauses[-abs(literal)]
        else:
            lit_in_clause = lit_in_clauses[abs(literal)]

        for index in lit_in_clause:
            if true_sat_lit[index] == 1:
                break_score += 1
            elif true_sat_lit[index] == 0:
                break_score -= 1
        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]

        elif break_score == break_min:
            best_literals.append(literal)
    if break_min != 0 and random.random() < omega:
        return random.sample(clause, 1)[0]
    else:
        if best_literals:
            return random.sample(best_literals, 1)[0]
        else:
            return None

def true_literals(clauses, interpretation):
    literals = [0] * len(clauses)
    for i, clause in enumerate(clauses):
        for literal in clause:
            if -literal in clause:
                break
            if interpretation[abs(literal)] == literal:
                literals[i] += 1
    return literals

def nanosat33(clauses, num_vars, lit_clause, max_flips=5):
    max_flips = len(clauses) * max_flips * num_vars
    interpretation = generate_rnd_interpretation(num_vars)
    true_sat_lit = true_literals(clauses, interpretation)

    for i in range(max_flips):
        clause_index = next((i for i, c in enumerate(clauses) if true_sat_lit[i] == 0), None)
        if clause_index is None:
            return interpretation

        unsatisfied_clause = clauses[clause_index]
        literal_to_change = compute_literals_in_clause(unsatisfied_clause, true_sat_lit, lit_clause, interpretation)
        if literal_to_change is None:
            return None

        change_literal_value(literal_to_change, true_sat_lit, lit_clause)
        interpretation[abs(literal_to_change)] = -interpretation[abs(literal_to_change)]



if __name__ == '__main__':
    clauses, n_vars, lit_clause = file_parser(sys.argv[1])
    solution = nanosat33(clauses, n_vars, lit_clause)

    satisfiable = 's SATISFIABLE'
    interpretation = 'v ' + ' '.join(map(str, solution[1:])) + ' 0'
    print(satisfiable + "\n" + interpretation)