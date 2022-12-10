import importlib.resources


def load_variant(variant_: int) -> list:
    path = str(variant_) + '.txt'
    try:
        with importlib.resources.open_text('rank.input_data', path) as file:
            input_data = [[int(num_) for num_ in line.split(' ')] for line in file]
        return input_data
    except IOError:
        print("File isn't found")


def matrix_to_str(matrix: list) -> str:
    result = '\n'.join('\t'.join(map(str, row)) for row in matrix)
    return result


def dict_to_str(ranking_dict: dict) -> str:
    first_row = ' '
    second_row = ' '
    for key in ranking_dict.keys():
        first_row += key + '    '
        second_row += str(ranking_dict[key]) + '    '
    result = first_row + '\n' + second_row
    return result


def condorcet_to_str(condorcet_ranking: dict) -> str:
    result = ''
    ranking = ''
    for i, key in enumerate(condorcet_ranking.keys()):
        arr = '\n'.join('\t'.join(map(str, row)) for row in condorcet_ranking[key])
        result += str(i+1) + ' round:\n' + arr + '\nPicked as the best: ' + key + '\n\n'
        ranking += key + '  '
    result += '\nResult ranking: ' + ranking
    return result


def create_borda_matrix(ranking_matrix: list) -> list:
    n = len(ranking_matrix)
    for i in range(n):
        for j in range(n):
            ranking_matrix[i][j] = n - ranking_matrix[i][j]
    return ranking_matrix


def create_rel_mat(expert_list: list) -> list:
    n = len(expert_list)
    p = [[0] * n for j in range(n)]
    for i in range(n):
        for j in range(n):
            if expert_list[i] > expert_list[j]:
                p[i][j] = -1
            elif expert_list[i] == expert_list[j]:
                p[i][j] = 0
            else:
                p[i][j] = 1
    return p


def count_q_matrix(relations: dict) -> list:
    n = len(relations.keys())
    q = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            for p_key in relations.keys():
                if relations[p_key][i][j] == 0:
                    q[i][j] += 1
                elif relations[p_key][i][j] == 1:
                    q[i][j] += 0
                else:
                    q[i][j] += 2
    return q


def count_pair_vectors(u: list, v: list) -> int:
    result = 0
    for i in range(len(u)):
        result = result + (u[i] - v[i]) * (u[i] - v[i])
    return result


def p_spearman(ranking_len: int, pair: int):
    return 1 - (6 / (ranking_len * (ranking_len * ranking_len - 1))) * pair



'''
Function to print to the console the result ranking.
---
Parameters:
result_ranking:dict
should be like {'A1':10,'A2':15,'A3':20} (alternative: value)
---
Returns nothing

def printrr(result_ranking: dict):
    digits = ['~', '>', '<']
    result_ranking_string = ''
    alts = result_ranking.keys()
    left, right = 0, 1
    n = len(alts) # 6 left 4 right 5
    while left<= n-2 and right<=n-1:
'''