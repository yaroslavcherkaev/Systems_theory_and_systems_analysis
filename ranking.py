class Ranking:

    def __init__(self, variant = None, experts = None, alternatives = None, ranking_matrix = None):
        self.variant = variant
        self.experts = experts 
        self.alternatives = alternatives
        self.ranking_matrix = ranking_matrix

    '''
    Загрузить матрицу из тестовых вариантов из папки input_data
    '''
    def load_variant(self, variant:int) -> bool:
        path = 'input_data/' + str(variant) + '/' +  str(variant) + '.txt'
        try:
            alternatives = []
            experts = []
            expert_dict ={}
            alt_dict = {}
            with open(path,"r") as file:
                input_data = [[int(num) for num in line.split(' ')] for line in file]
            self.variant = variant
            self.ranking_matrix = input_data
            self.ranking_length = len(input_data)
            for i in range(self.ranking_length):
                alt = 'A'
                exp = 'E'
                num = i+1
                alternatives.append(alt+str(num))
                experts.append(exp+str(num))
            for i in range(self.ranking_length):
                expert_dict[experts[i]] = input_data[i]
            self.experts = expert_dict
            for i in range(self.ranking_length):
                alt_dict[alternatives[i]] = [x[i] for x in input_data]
            self.alternatives = alt_dict
            return True
        except IOError:
            self.ranking_matrix = None
            print ("File isn't found")
            return False

    def get_ranking_matrix(self) -> list:
        return self.ranking_matrix
    
    def get_ranking_len(self) -> int:
        return self.ranking_length

    def get_experts(self) -> dict:
        return self.experts
    
    def get_alternatives(self) -> dict:
        return self.alternatives

    def get_expert_by_index(self,index:int) -> list:
        exp_key = 'E' +str(index)
        return self.experts[exp_key]
    
    def get_alternative_by_index(self, index:int) -> list:
        alt_key = 'A' + str(index)
        return self.alternatives[alt_key]

    '''
    Метод возвращает отсортированное ранжирование по сумме рангов
    '''
    def rank_by_sum(self, rvrs = False) -> dict:
        ranking_sum_dict = {}
        ranking_result = {}
        for alt in self.alternatives:
            ranking_sum_dict[alt] = sum(self.alternatives[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse = rvrs))      
        return ranking_result

    '''
   
    '''
    def rank_by_Condorcet(self) -> dict:

        def check_pair(l,k, ranking_matrix):
            if l == k:
                return 0
            else:
                sum_of_exp = 0
                for i in range(len(ranking_matrix)):
                    if ranking_matrix[i][l] < ranking_matrix[i][k]:
                        sum_of_exp+=1
                return sum_of_exp    
                
        Slk_matrix = [[0] * self.ranking_length for i in range(self.ranking_length)]
        for i in range(self.ranking_length):
            for j in range(self.ranking_length):
                Slk_matrix[i][j] = check_pair(i, j, self.ranking_matrix)

        T_matrix = [[0] * self.ranking_length for i in range(self.ranking_length)]
        for i in range(self.ranking_length):
            for j in range(self.ranking_length):
                if Slk_matrix[i][j] >= Slk_matrix[j][i]:
                    T_matrix[i][j] = 1
                else:
                    T_matrix[i][j] = 0
        print(T_matrix)
   
    '''
    Метод статистической проверки согласованности ранжирований,
    полученных от экспертов. Рассчет коэффициентов ранговой корреляции Спирмена.
    Возвращает матрицу коэффициентов ранговой корреляции Спирмена.
    '''  
    def correlate_Spirman(self) -> list:
        def P(n,a):
            return 1 - (6/(n * (n*n - 1))) * a

        def count_pair_vectors(u:list, v:list)->int:
            result = 0
            for i in range(len(u)):
                result = result + (u[i]-v[i])*(u[i]-v[i])
            return result 

        N = self.ranking_length
        n = self.ranking_length
        matrix_of_k = [[1] * N for i in range(n)]
        for i in range(N):
            for j in range(N):
                value = P(n, count_pair_vectors(self.ranking_matrix[i], self.ranking_matrix[j]))
                matrix_of_k[i][j] = round(value, 4)
        return matrix_of_k











a = Ranking()
a.load_variant(7)
a.rank_by_Condorcet()
print(a.get_ranking_matrix())