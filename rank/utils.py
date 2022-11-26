import importlib.resources


def load_variant(variant_: int) -> list:
    path = str(variant_) + '.txt'
    try:
        with importlib.resources.open_text('rank.input_data', path) as file:
            input_data = [[int(num_) for num_ in line.split(' ')] for line in file]
        return input_data
    except IOError:
        print("File isn't found")


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



