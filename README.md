# Rank package 

The `rank` package is on dev, but you already can use existing functional in your projects.

To install `rank` package locally clone this repo. Go to this folder and then enter command in the terminal:

```
pip install .
```

Finally, you can use this package in this way:

```
from rank import ranking, bordaranking, condorcetranking


a = ranking.Ranking()
a.load_variant_from_file(7)
a.rank_by_sum()
print(a)

b = bordaranking.BordaRanking()
b.load_variant_from_file(7)
b.rank_by_borda()
print(b)

c =  condorcetranking.CondorcetRanking()
c.load_variant_from_file(7)
c.rank_by_condorcet()
print(c)

```

## Description

The `rank` package is intended for calculations related to the ranking of alternatives.

The package so far supports only symmetric matrices(NxN) for comparing alternatives.

The package contains 8 variants with different matrix of comparison of alternatives (6x6).

You can load these variants using `load_variant_from_file(variant: int)` method.



