# Rank package 

The `rank` package is on dev, but you already can use existing functional in your projects.

To install `rank` package locally clone this repo. Go to this folder and then enter command in the terminal:

```
pip install .
```

Finally, you can use this package in this way:

```
from rank import ranking, utils

my_ranking = ranking.Ranking('ranking.txt')
print(my_ranking)

borda = my_ranking.rank_by_borda()
print(borda)

rank_sum = my_ranking.rank_by_sum()
print(rank_sum)

condorcet = my_ranking.rank_by_condorcet()
print(utils.condorcet_to_str(condorcet))


```

## Description

The `rank` package is intended for calculations related to the ranking of alternatives.

The package so far supports only symmetric matrices(NxN) for comparing alternatives.



