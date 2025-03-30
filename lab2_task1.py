from itertools import combinations_with_replacement
from math import factorial
# N = n!/(k1!*k2!*...*km!)
#ЧЕРЕСПОЛОСИЦА
letter_counts = {
    'Ч': 1, 'Е': 2, 'Р': 1, 'С': 2, 'П': 1,
    'О': 2, 'Л': 1, 'И': 2, 'Ц': 1, 'А': 1
}

unique_letters = list(letter_counts.keys())

valid_combinations = []

for combo in combinations_with_replacement(unique_letters, 6):
    combo_counts = {letter: combo.count(letter) for letter in set(combo)}

    if all(combo_counts[letter] <= letter_counts[letter] for letter in combo_counts):
        numerator = factorial(6)
        denominator = 1
        for count in combo_counts.values():
            denominator *= factorial(count)
        valid_combinations.append(numerator // denominator)

total_unique_words = sum(valid_combinations)
print(total_unique_words)
