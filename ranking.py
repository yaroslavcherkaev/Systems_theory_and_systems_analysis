
class Ranking:

    def __init__(self, variant = None, experts = None, alternatives = None, ranking_matrix = None):
        self.variant = variant
        self.experts = experts 
        self.alternatives = alternatives
        self.ranking_matrix = ranking_matrix
    

    '''
    Загрузить матрицу из тестовых вариантов из папки input_data
    '''
    def load_variant(self, variant:int):
        path = 'input_data/' + str(variant) + '/' +  str(variant) + '.txt'
        try:
            with open(path,"r") as file:
                input_data = [[int(num) for num in line.split(' ')] for line in file]
            self.ranking_matrix = input_data
            self.ranking_length = len(input_data)
        except IOError:
            self.ranking_matrix = None
            print ("File isn't found")

    def get_ranking_matrix(self) -> list:
        return self.ranking_matrix
    
    def get_ranking_len(self) -> int:
        return self.ranking_length

    def get_expert_ranking(self, expert_index: int) -> list:
        if (expert_index >= 0 ) and (expert_index <= self.ranking_length - 1):
            return self.ranking_matrix[expert_index]
        else:
            print('In get_expert_ranking(expert_index: int): expert index out of the range')
            return None


    '''
    Функция статистической проверка согласованности ранжирований,
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













        