from .ranking import Ranking
# TODO: add set_ranking for Borda


class BordaRanking(Ranking):
    def __init__(self):
        super().__init__()
        self.alternatives_Borda = None

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
            for i in range(self.ranking_length):
                alt_b_dict[alternatives[i]] = [self.ranking_length - x[i] for x in input_variant_data]
            self.alternatives_Borda = alt_b_dict
            return True
        else:
            return False

    def get_alternatives_borda(self) -> dict:
        return self.alternatives_Borda

    def get_alternatives_borda_by_index(self, index: int) -> list:
        alt_key = 'A' + str(index)
        return self.alternatives_Borda[alt_key]

    # The method returns a sorted rank according to the Borda principle
    def rank_by_borda(self, reverse_=True) -> dict:
        ranking_sum_dict = {}
        for alt in self.alternatives_Borda:
            ranking_sum_dict[alt] = sum(self.alternatives_Borda[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=reverse_))
        self.result_ranking = ranking_result
        return ranking_result

