import time
from typing import List, Dict, Tuple

#Алгоритм 1: Расстояние Левенштейна
def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

#Алгоритм 2: Расстояние Дамерау-Левенштейна
def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
        
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                # transposition
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)
                
    return d[(lenstr1 - 1, lenstr2 - 1)]

#Функция поиска по тексту
def search_text(text: str, word: str, algorithm: str) -> Tuple[float, List[Dict]]:
    start_time = time.time()
    words = text.split()
    results = []
    
    if algorithm == "levenshtein":
        distance_func = levenshtein_distance
    elif algorithm == "damerau_levenshtein":
        distance_func = damerau_levenshtein_distance
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    #Вычисление расстояния для каждого слова
    for text_word in words:
        distance = distance_func(word.lower(), text_word.lower())
        # Добавляем в результаты только если расстояние меньше определенного порога
        # или если это точное совпадение
        if distance <= min(3, max(len(word), len(text_word)) // 2) or distance == 0:
            results.append({
                "word": text_word,
                "distance": distance
            })
    
    results.sort(key=lambda x: x["distance"])
    
    results = results[:10]
    
    execution_time = time.time() - start_time
    return execution_time, results
