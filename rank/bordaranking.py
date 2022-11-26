from ranking import Ranking
from utils import load_variant, dict_to_str
# TODO: add set_ranking for Borda


class BordaRanking(Ranking):
    def __init__(self):
        super().__init__()
        self.borda_matrix = None
        self.alternatives_borda = None

    def __str__(self):
        if self.ranking_matrix:
            rnk_matrix = '\n'.join('\t'.join(map(str, row)) for row in self.ranking_matrix)
        else:
            rnk_matrix = None
        if self.borda_matrix:
            brd_matrix = '\n'.join('\t'.join(map(str, row)) for row in self.borda_matrix)
        else:
            brd_matrix = None
        if self.result_ranking:
            rnk_result = dict_to_str(self.result_ranking)
        else:
            rnk_result = None
        return f'Variant {self.variant}\n\n{rnk_matrix}\n\nBorda matrix:\n{brd_matrix}\n\nResult ranking:\n{rnk_result}'

    # Loading matrix from file
    def load_variant_from_file(self, variant: int) -> bool:
        input_variant_data = load_variant(variant)
        if input_variant_data:
            alternatives, experts = [], []
            expert_dict, alt_dict, alt_b_dict = {}, {}, {}
            self.variant = variant
            self.ranking_matrix = input_variant_data
            self.ranking_length = len(input_variant_data)
            borda_matrix = [row[:] for row in input_variant_data]
            for i in range(self.ranking_length):
                for j in range(self.ranking_length):
                    borda_matrix[i][j] = self.ranking_length - borda_matrix[i][j]
            self.borda_matrix = borda_matrix
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
            for i in range(self.ranking_length):
                alt_b_dict[alternatives[i]] = [self.ranking_length - x[i] for x in input_variant_data]
            self.alternatives_borda = alt_b_dict
            return True
        else:
            return False

    def get_alternatives_borda(self) -> dict:
        return self.alternatives_borda

    def get_alternatives_borda_by_index(self, index: int) -> list:
        alt_key = 'A' + str(index)
        return self.alternatives_borda[alt_key]

    # The method returns a sorted rank according to the Borda principle
    def rank_by_borda(self, reverse_=True) -> dict:
        ranking_sum_dict = {}
        for alt in self.alternatives_borda:
            ranking_sum_dict[alt] = sum(self.alternatives_borda[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=reverse_))
        self.result_ranking = ranking_result
        return ranking_result
