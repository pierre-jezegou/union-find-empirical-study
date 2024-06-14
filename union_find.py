from enum import Enum
from math import floor
import sys

# Define an enum for the types
class PathCompressionType(Enum):
    """Compression types"""
    NC = 1 # No compression
    FC = 2 # Full compression
    PS = 3 # Path splitting
    PH = 4 # Path halving

class Measure:
    def __init__(self, tpl, tpu):
        self.tpl = tpl
        self.tpu = tpu

class UnionFind:
    """Union-find data structure."""
    def __init__(self):
        self.parents = []
        self.n_blocks = 0
        self.path_compression_type = PathCompressionType.NC

    def find(self, i: int) -> int:
        """Find the representative of the class to which i belongs."""

        if self.parents[i] == i or self.parents[i] < 0:
            return i

        # no compression
        if self.path_compression_type == PathCompressionType.NC:
            return self.find(self.parents[i])

        # Full path compression:
        # Update each node to directly point to its representative.
        elif self.path_compression_type == PathCompressionType.FC:
            self.parents[i] = self.find(self.parents[i])
            return self.parents[i]

        # Path splitting:
        # Update each node to point to its grandparent
        # (unless it is the root or a direct child of the root).
        elif self.path_compression_type == PathCompressionType.PS:
            child = -1
            grandchild = -1
            while not (self.parents[i] == i or self.parents[i] < 0):
                if grandchild != -1:
                    self.parents[grandchild] = i
                grandchild = child
                child = i
                i = self.parents[i]
            return i

        # Path halving: Update every other node in the path to point to its grandparent
        # (unless it is the root or a direct child of the root).
        elif self.path_compression_type == PathCompressionType.PH:
            distance = 0  # Distance from the root
            grandchild = i
            while not (self.parents[i] == i or self.parents[i] < 0):
                if distance == 2:
                    self.parents[grandchild] = i
                    distance = 0
                    grandchild = i
                distance += 1
                i = self.parents[i]
            return i
        else:
            sys.stderr.write("Invalid path compression path_compression_type\n")
            return -1

    def merge(self, i: int, j: int):
        """Performs the union of the classes with representatives ri and rj."""
        raise NotImplementedError("Merge function not implemented")

    def nr_blocks(self):
        """Returns the number of blocks in the union-find set."""
        return self.n_blocks

    def get_parents(self):
        """Returns the parents of the nodes."""
        return self.parents

    def depth(self, i: int) -> int:
        """Calculate the depth from node i to its root."""
        length = 0
        while not (self.parents[i] == i or self.parents[i] < 0):
            length += 1
            i = self.parents[i]
        return length

    def tpl(self) -> int:
        """Calculate the Total Path Length (TPL)."""
        total_path_length = 0
        for i in range(len(self.parents)):
            total_path_length += self.depth(i)
        return total_path_length

    def tpu(self) -> int:
        """Calculate the Total Path Updates (TPU)."""
        total_path_updates = 0
        for i in range(len(self.parents)):
            path_length = self.depth(i)
            path_updates = 0
            # no compression
            if self.path_compression_type == PathCompressionType.NC:
                path_updates = 0
            # full path compression or path splitting
            elif self.path_compression_type in (PathCompressionType.FC, PathCompressionType.PS):
                path_updates = path_length - 1 if path_length > 0 else 0
            # path halving
            elif self.path_compression_type == PathCompressionType.PH:
                path_updates = floor(path_length / 2)
            else:
                sys.stderr.write("Invalid path compression path_compression_type\n")
            total_path_updates += path_updates
        return total_path_updates

    def print(self):
        """Print the parents of the nodes."""
        print("[", end=" ")
        for num in self.parents:
            print(num, end=" ")
        print("];")

class QuickUnion(UnionFind):
    """Quick-union data structure."""
    def __init__(self, n: int, path_compression_type) -> None:
        super().__init__()
        self.parents = list(range(n))
        self.n_blocks = n
        self.path_compression_type = path_compression_type

    def merge(self, i, j) -> None:
        ri = self.find(i)
        rj = self.find(j)
        if ri != rj:
            self.parents[ri] = rj
            self.n_blocks -= 1

class UnionWeight(UnionFind):
    """Union-weight data structure."""
    def __init__(self, n: int, path_compression_type):
        super().__init__()
        self.parents = [-1] * n
        self.n_blocks = n
        self.path_compression_type = path_compression_type

    def merge(self, i: int, j: int) -> None:
        ri = self.find(i)
        rj = self.find(j)
        if ri == rj:
            return
        if self.parents[ri] >= self.parents[rj]:
            self.parents[rj] += self.parents[ri]
            self.parents[ri] = rj
        else:
            self.parents[ri] += self.parents[rj]
            self.parents[rj] = ri
        self.n_blocks -= 1

class UnionRank(UnionFind):
    """Union-rank data structure."""
    def __init__(self, n: int, path_compression_type):
        super().__init__()
        self.parents = [-1] * n
        self.n_blocks = n
        self.path_compression_type = path_compression_type

    def merge(self, i: int, j: int) -> None:
        ri = self.find(i)
        rj = self.find(j)
        if ri == rj:
            return
        if self.parents[ri] >= self.parents[rj]:
            self.parents[rj] = min(self.parents[rj], self.parents[ri] - 1)
            self.parents[ri] = rj
        else:
            self.parents[ri] = min(self.parents[ri], self.parents[rj] - 1)
            self.parents[rj] = ri
        self.n_blocks -= 1

if __name__ == "__main__":
    N = 10
    path_compression_type = PathCompressionType.FC

    print("Testing QuickUnion:")
    qu = QuickUnion(N, path_compression_type)
    qu.merge(1, 2)
    qu.merge(3, 4)
    qu.merge(1, 4)
    qu.print()
    print(f"TPL: {qu.tpl()}, TPU: {qu.tpu()}")

    print("\nTesting UnionWeight:")
    uw = UnionWeight(N, path_compression_type)
    uw.merge(1, 2)
    uw.merge(3, 4)
    uw.merge(1, 4)
    uw.print()
    print(f"TPL: {uw.tpl()}, TPU: {uw.tpu()}")

    print("\nTesting UnionRank:")
    ur = UnionRank(N, path_compression_type)
    ur.merge(1, 2)
    ur.merge(3, 4)
    ur.merge(1, 4)
    ur.print()
    print(f"TPL: {ur.tpl()}, TPU: {ur.tpu()}")
