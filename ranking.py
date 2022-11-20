class Ranking:

    def __init__(self, variant=None, experts=None, alternatives=None, ranking_matrix=None):
        self.variant = variant
        self.experts = experts 
        self.alternatives = alternatives
        self.ranking_matrix = ranking_matrix
        self.alternatives_Borda = None

    def __str__(self):
        if self.ranking_matrix:
            arr = '\n'.join('\t'.join(map(str, row)) for row in self.ranking_matrix)
        else:
            arr = None
        return f'Variant {self.variant}\n\n{arr}'

    '''
    Загрузить матрицу из тестовых вариантов из папки input_data
    '''
    @classmethod
    def load_variant(self, variant:int) -> bool:
        path = 'input_data/' + str(variant) + '/' +  str(variant) + '.txt'
        try:
            with open(path,"r") as file:
                input_data = [[int(num) for num in line.split(' ')] for line in file]
        except IOError:
            self.ranking_matrix = None
            print ("File isn't found")
            return False
        alternatives, experts = [], []
        expert_dict, alt_dict, altB_dict = {}, {}, {}
        self.variant = variant
        self.ranking_matrix = input_data
        self.ranking_length = len(input_data)
        for i in range(self.ranking_length):
            alt, exp = 'A', 'E'
            num = i+1
            alternatives.append(alt+str(num))
            experts.append(exp+str(num))
        for i in range(self.ranking_length):
            expert_dict[experts[i]] = input_data[i]
        self.experts = expert_dict
        for i in range(self.ranking_length):
            alt_dict[alternatives[i]] = [x[i] for x in input_data]
        self.alternatives = alt_dict
        for i in range(self.ranking_length):
            altB_dict[alternatives[i]] = [self.ranking_length - x[i] for x in input_data]
        self.alternatives_Borda = altB_dict
        return True
    
    @classmethod
    def get_ranking_matrix(self) -> list:
        return self.ranking_matrix

    @classmethod    
    def get_ranking_len(self) -> int:
        return self.ranking_length

    @classmethod
    def get_experts(self) -> dict:
        return self.experts
    
    @classmethod
    def get_alternatives(self) -> dict:
        return self.alternatives

    @classmethod
    def get_expert_by_index(self,index:int) -> list:
        exp_key = 'E' +str(index)
        return self.experts[exp_key]
    
    @classmethod
    def get_alternative_by_index(self, index:int) -> list:
        alt_key = 'A' + str(index)
        return self.alternatives[alt_key]

    '''
    Метод возвращает отсортированное ранжирование по сумме рангов
    '''
    @classmethod
    def rank_by_sum(self, rvrs=False) -> dict:
        ranking_sum_dict = {}
        ranking_result = {}
        for alt in self.alternatives:
            ranking_sum_dict[alt] = sum(self.alternatives[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=rvrs))      
        return ranking_result

    '''
    Метод возвращает отсортированное ранжирование по принципу Борда
    '''
    @classmethod
    def rank_by_Borda(self, rvrs=True) -> dict:
        ranking_sum_dict = {}
        ranking_result = {}
        for alt in self.alternatives_Borda:
            ranking_sum_dict[alt] = sum(self.alternatives_Borda[alt])
        ranking_result = dict(sorted(ranking_sum_dict.items(), key=lambda item: item[1], reverse=rvrs))      
        return ranking_result

    '''
   
    '''
    @classmethod
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
    @classmethod
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
