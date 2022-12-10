from utils import load_variant, matrix_to_str, create_rel_mat, count_q_matrix
from utils import p_spearman, count_pair_vectors, create_borda_matrix


class Ranking:
    def __init__(self, variant: int):
        self.variant = variant
        self.experts = None
        self.alternatives = None
        self.ranking_matrix = None
        self.ranking_length = None
        self.__set_ranking(variant)

    def __str__(self):
        return f'Variant {self.variant}\nInput data:\n{matrix_to_str(self.ranking_matrix)}'

    # Loading matrix from file
    def __set_ranking(self, variant: int, type_='default') -> bool:
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
                expert_dict[experts[i]] = self.ranking_matrix[i]
            self.experts = expert_dict
            for i in range(self.ranking_length):
                alt_dict[alternatives[i]] = [x[i] for x in self.ranking_matrix]
            self.alternatives = alt_dict
            return True
        else:
            return False

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
        ranking_sum_dict: dict = {}
        for alt in self.alternatives:
            ranking_sum_dict[alt] = sum(self.alternatives[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=reverse_))
        return ranking_result

    def rank_by_borda(self, reverse_=True) -> dict:
        ranking_sum_dict: dict = {}
        for alt in self.alternatives:
            borda_sum = 0
            for i in range(self.ranking_length):
                borda_sum += self.ranking_length - self.alternatives[alt][i]
            ranking_sum_dict[alt] = borda_sum
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=reverse_))
        return ranking_result

    def count_relation_matrices(self):
        relations_matrices = {}
        i = 1
        for key in self.experts.keys():
            m_key = 'P' + str(i)
            relations_matrices[m_key] = create_rel_mat(self.experts[key])
            i += 1
        return relations_matrices

    def count_loss_matrix(self):
        relations_matrices = self.count_relation_matrices()
        loss_matrix = count_q_matrix(relations_matrices)
        return loss_matrix

    '''
    The method of statistical consistency checking of the rankings,
    obtained from the experts. Calculation of Spearman rank correlation coefficients.
    Returns the matrix of Spearman rank correlation coefficients.
    '''
    def correlate_spearman(self) -> list:
        num_of_alts = self.ranking_length
        n = self.ranking_length
        matrix_of_k = [[1] * num_of_alts for i in range(n)]
        for i in range(num_of_alts):
            for j in range(num_of_alts):
                pair = count_pair_vectors(self.ranking_matrix[i], self.ranking_matrix[j])
                value = p_spearman(n, pair)
                matrix_of_k[i][j] = round(value, 4)
        return matrix_of_k
    def count_kemeni_median(self):
        pass


a = Ranking(7)
print(a.rank_by_borda())

