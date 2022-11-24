from .ranking import Ranking


class CondorcetRanking(Ranking):
    def __init__(self):
        super().__init__()
        self.s_matrix = None
        self.t_matrix = None

    def rank_by_condorcet(self) -> dict:

        def check_pair(left, right, ranking_matrix):
            if left == right:
                return 0
            else:
                sum_of_exp = 0
                for i in range(len(ranking_matrix)):
                    if ranking_matrix[i][left] < ranking_matrix[i][right]:
                        sum_of_exp += 1
                return sum_of_exp

        def get_condorcet_alternative(alternatives_: list, t_matrix_: list):
            n = len(t_matrix_)
            for i in range(n):
                if sum(t_matrix_[i]) == n:
                    return alternatives_[i]
        # s_matrix[l][k] is the number of experts, who consider alternative l more preferable than k.
        ranking_result = {}
        s_matrix = [[0] * self.ranking_length for i in range(self.ranking_length)]
        for i in range(self.ranking_length):
            for j in range(self.ranking_length):
                s_matrix[i][j] = check_pair(i, j, self.ranking_matrix)
        self.s_matrix = s_matrix
        t_matrix = [[0] * self.ranking_length for i in range(self.ranking_length)]
        for i in range(self.ranking_length):
            for j in range(self.ranking_length):
                if s_matrix[i][j] >= s_matrix[j][i]:
                    t_matrix[i][j] = 1
                else:
                    t_matrix[i][j] = 0
        self.t_matrix = t_matrix
        # The resulting rank is constructed by sequentially eliminating the next Condorcet alternative from t_matrix
        # and searching for the next such alternative among the remaining alternatives.
        alternatives = list(self.alternatives.keys())
        round_n = 0
        while round_n != self.ranking_length:
            alt_c = get_condorcet_alternative(alternatives, t_matrix)
            ranking_result[str(round_n + 1)] = (alt_c, t_matrix.copy())
            index = alternatives.index(alt_c)
            alternatives.remove(alt_c)
            del t_matrix[index]
            for i in range(len(t_matrix)):
                for j in range(len(t_matrix) + 1):
                    if j == index:
                        del t_matrix[i][j]
            round_n += 1
        self.result_ranking = ranking_result
        return ranking_result
