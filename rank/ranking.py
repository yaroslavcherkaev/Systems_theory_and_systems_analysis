class Ranking:
    def __init__(self):
        self.variant = None
        self.experts = None
        self.alternatives = None
        self.ranking_matrix = None
        self.ranking_length = None
        self.result_ranking = None

    def __str__(self):
        if self.ranking_matrix:
            arr = '\n'.join('\t'.join(map(str, row)) for row in self.ranking_matrix)
        else:
            arr = None
        return f'Variant {self.variant}\n\n{arr}'

    # Loading matrix from file
    def load_variant_from_file(self, variant: int) -> bool:
        def load_variant(variant_: int) -> list:
            path = 'input_data/' + str(variant_) + '.txt'
            try:
                with open(path, "r") as file:
                    input_data = [[int(num_) for num_ in line.split(' ')] for line in file]
                return input_data
            except IOError:
                print("File isn't found")

        input_variant_data = load_variant(variant)
        if input_variant_data:
            alternatives, experts = [], []
            expert_dict, alt_dict, alt_b_dict = {}, {}, {}
            self.variant = variant
            self.ranking_matrix = input_variant_data
            self.ranking_length = len(input_variant_data)
            for i in range(self.ranking_length):
                alt, exp = 'A', 'E'
                num = i + 1
                alternatives.append(alt + str(num))
                experts.append(exp + str(num))
            for i in range(self.ranking_length):
                expert_dict[experts[i]] = input_variant_data[i]
            self.experts = expert_dict
            for i in range(self.ranking_length):
                alt_dict[alternatives[i]] = [x[i] for x in input_variant_data]
            self.alternatives = alt_dict
            return True
        else:
            return False

    def set_ranking(self, ranking_matrix: list):
        self.ranking_matrix = ranking_matrix
        self.ranking_length = len(ranking_matrix)
        alternatives, experts = [], []
        expert_dict, alt_dict = {}, {}
        for i in range(self.ranking_length):
            alt, exp = 'A', 'E'
            num = i + 1
            alternatives.append(alt + str(num))
            experts.append(exp + str(num))
        for i in range(self.ranking_length):
            expert_dict[experts[i]] = ranking_matrix[i]
        self.experts = expert_dict
        for i in range(self.ranking_length):
            alt_dict[alternatives[i]] = [x[i] for x in ranking_matrix]
        self.alternatives = alt_dict
        pass
        # TODO: add try except

    def get_ranking_matrix(self) -> list:
        return self.ranking_matrix

    def get_ranking_len(self) -> int:
        return self.ranking_length

    def get_experts(self) -> dict:
        return self.experts

    def get_alternatives(self) -> dict:
        return self.alternatives

    def get_expert_by_index(self, index: int) -> list:
        exp_key = 'E' + str(index)
        return self.experts[exp_key]

    def get_alternative_by_index(self, index: int) -> list:
        alt_key = 'A' + str(index)
        return self.alternatives[alt_key]

    # The method returns a sorted rank by the sum of the ranks
    def rank_by_sum(self, reverse_=False) -> dict:
        ranking_sum_dict = {}
        for alt in self.alternatives:
            ranking_sum_dict[alt] = sum(self.alternatives[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=reverse_))
        self.result_ranking = ranking_result
        return ranking_result

    '''
    The method of statistical consistency checking of the rankings,
    obtained from the experts. Calculation of Spearman rank correlation coefficients.
    Returns the matrix of Spearman rank correlation coefficients.
    '''
    def correlate_spirman(self) -> list:

        def p(ranking_len, pair_):
            return 1 - (6 / (ranking_len * (ranking_len * ranking_len - 1))) * pair_

        def count_pair_vectors(u: list, v: list) -> int:
            result = 0
            for i in range(len(u)):
                result = result + (u[i] - v[i]) * (u[i] - v[i])
            return result

        num_of_alts = self.ranking_length
        n = self.ranking_length
        matrix_of_k = [[1] * num_of_alts for i in range(n)]
        for i in range(num_of_alts):
            for j in range(num_of_alts):
                pair = count_pair_vectors(self.ranking_matrix[i], self.ranking_matrix[j])
                value = p(n, pair)
                matrix_of_k[i][j] = round(value, 4)
        return matrix_of_k

