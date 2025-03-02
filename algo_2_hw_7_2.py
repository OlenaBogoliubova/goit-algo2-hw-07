import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root
        
        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value
    result = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, result)
    return result

if __name__ == "__main__":
    test_values = list(range(0, 951, 50))
    lru_times = []
    splay_times = []
    
    for n in test_values:
        tree = SplayTree()
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=3) / 3
        lru_times.append(lru_time)
        splay_times.append(splay_time)
    
    print("n         LRU Cache Time (s)  Splay Tree Time (s)")
    print("--------------------------------------------------")
    for i in range(len(test_values)):
        print(f"{test_values[i]:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")
    
    plt.figure(figsize=(10, 5))
    plt.plot(test_values, lru_times, label="LRU Cache", marker="o")
    plt.plot(test_values, splay_times, label="Splay Tree", marker="x")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid()
    plt.show()
