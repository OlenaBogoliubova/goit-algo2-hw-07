import random
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value
    
    def invalidate(self, index):
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]


# Без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# З кешем
cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)

if __name__ == "__main__":
    N = 100000
    Q = 50000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = [("Range", random.randint(0, N-1), random.randint(0, N-1)) if random.random() < 0.7 else
               ("Update", random.randint(0, N-1), random.randint(1, 100)) for _ in range(Q)]
    
    # Тест без кешу
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, min(query[1], query[2]), max(query[1], query[2]))
        else:
            update_no_cache(array, query[1], query[2])
    no_cache_time = time.time() - start_time
    
    # Тест з кешем
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array, min(query[1], query[2]), max(query[1], query[2]))
        else:
            update_with_cache(array, query[1], query[2])
    cache_time = time.time() - start_time
    
    # Вивід результатів
    print("\nРезультати тестування:")
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")
