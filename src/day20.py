#%%
import numpy as np

# %%
def binary_list_to_int(ll):
    """Convert a binary list to its decimal representation"""
    return int(''.join(map(str, ll)), 2)


def flip(i, n=10):
    """Return the flipped version of the integer
    i.e. the number you get by reading backwards its binary representation"""
    return int(bin(i)[2:].zfill(n)[::-1], 2)


class Tile():
    """Tile that can be flipped and rotated
    
    The main idea is to represent a border (made of 0's and 1's) by its decimal representation
    Note that when rotations and flips are applied, the border may be reversed. Thus, its decimal
    representation is 'flipped' too. That's why to identify a border, the minimum between its
    decimal representation and its 'flipped' version is taken.
    """
    def __init__(self, idx, pattern):
        self.id = idx
        self.pattern = np.array(pattern, dtype=int)
        self.shape = pattern.shape
        
        self.borders_idx = self._borders_idx()  # borders idx
        self._update_borders()


    @property
    def borders(self):
        """Current binary representation of the borders [top, left, bottom, right]"""
        return self._borders

    def get_borders(self):
        return self.pattern[0,:], self.pattern[:,0], self.pattern[-1,:], self.pattern[:,-1]

    def _update_borders(self):
        self._borders = [binary_list_to_int(border) for border in self.get_borders()]

    def _borders_idx(self):
        """Compute the borders identifiers
        (minimum between the current decimal representation and its 'flipped' value)"""
        tt = []
        for border in self.get_borders():
            tt.append(min(binary_list_to_int(border), binary_list_to_int(border[::-1])))
        return tt
    

    def flip(self):
        """Flip the tile around the horizontal axis (top and bottom are interverted)"""
        self.pattern = self.pattern[::-1]
        self._update_borders()
        return self

    def rotate(self, i=0):
        """Rotate i times the tile (trigonometric direction, i.e. anti-clockwise)"""
        self.pattern = np.rot90(self.pattern, i)
        self._update_borders()
        return self

    def flip_rotate(self, border, pos):
        """Flip and Rotate the tile, so that the given border comes to the specified position

        Args:
            border (int): border decimal representation
            pos (int): 0: top, 1: left, 2: bottom, 3: right position
        """
        if border not in self.borders: self.rotate(2)
        assert border in self.borders, "The tile has no such border"

        current_pos = self.borders.index(border)
        self._flip_rotate_from_pos_to_top(current_pos)
        self._flip_rotate_from_top_to_pos(pos)

    def _flip_rotate_from_top_to_pos(self, pos):
        """Flip and Rotate the tile, so that the current top border comes to the specified position"""
        if pos == 1:
            self.flip().rotate(3)
        elif pos == 2:
            self.flip()
        elif pos == 3:
            self.rotate(3)
        return self

    def _flip_rotate_from_pos_to_top(self, pos):
        """Flip and Rotate the tile, so that the border in the specified position comes to the top"""
        if pos == 1:
            self.flip().rotate(3)
        elif pos == 2:
            self.flip()
        elif pos == 3:
            self.rotate(1)
        return self

    def __repr__(self):
        return f"<|{self.id}|> {tuple(self.borders)}"

#%%
def parser(filename):
    tiles = []  # list of tiles
    borders_tiles = {}  # border id -> tile

    with open(filename) as f:
        for line in f.read().split('\n\n'):
            line = line.splitlines()
            tile_id = int(line[0][5:-1])
            tile_pattern = np.array([list(k.replace('.', '0').replace('#', '1')) for k in line[1:]])

            tile = Tile(tile_id, tile_pattern)
            tiles.append(tile)
            for border in tile.borders_idx:
                borders_tiles.setdefault(border, []).append(tile)
    
    N = int(np.sqrt(len(tiles)))
    return tiles, borders_tiles, N


#%%
def find_corners_and_edges(tiles, borders_map):
    corners, edges = [], []
    for tile in tiles:
        n_edges = sum([len(borders_map[border]) == 1 for border in tile.borders_idx])
        if n_edges == 2:
            corners.append(tile)
        elif n_edges == 1:
            edges.append(tile)
    return corners, edges


#%%
def solve_puzzle(T, B, N, corner):
    """Place all the tiles in T""" 

    G = np.zeros((N, N), dtype=Tile)  # grid that will contains the tiles (instances of Tile)

    def get(n, borders=B):
        """Find the tiles that contains the given border (flipped or not)"""
        return borders.get(n, borders.get(flip(n)))


    def place_first_corner(corner, grid, borders=B):
        ## Find the two borders of the tile without neighbors
        edges = [b for b in corner.borders_idx if len(B[b]) == 1]
        assert len(edges) == 2, "This is not a corner piece"
        left, top = edges

        ## Flip and rotate the piece, so that the two edges are at the top and on the left
        corner.flip_rotate(left, 1)
        if corner.borders[0] != top and corner.borders[0] != flip(top):
            corner.flip()
        
        ## Place the corner on the grid
        grid[0, 0] = corner

    ## Place each tile row after row            
    for i in range(N):
        if i == 0:
            place_first_corner(corner, G)
        else:
            # Place the first piece in the row
            last_tile = G[i-1, 0]
            bottom = last_tile.borders[2]
            next_tile, = [tile for tile in get(bottom, B) if tile != last_tile]
            next_tile.flip_rotate(bottom, 0)
            G[i, 0] = next_tile

        for j in range(1, N):
            # Place the piece to the right of the previous one in the row
            last_tile = G[i, j-1]
            right = last_tile.borders[3]
            next_tile, = [tile for tile in get(right, B) if tile != last_tile]
            
            next_tile.flip_rotate(right, 1)
            G[i, j] = next_tile

    ## Build the resulting image by removing the borders
    m = G[0,0].shape[0] - 2  # dimension of the cropped tiles
    I = np.zeros((N * m, N * m), dtype=int)  # final image

    for i in range(N):
        for j in range(N):
            I[m*i: m*(i+1), m*j:m*(j+1)] = G[i, j].pattern[1:-1, 1:-1]

    return I

#%%
def find_monsters(I, monster):
    n, m = monster.shape
    N, M = I.shape

    n_monsters = 0
    for i in range(N - n):
        for j in range(M - m):
            zone = I[i:n+i, j:m+j]
            if np.all(monster == monster * zone):
                n_monsters += 1

    return n_monsters

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")    
    T, B, N = parser(f"{folder}/day20.txt")

    corners, edges = find_corners_and_edges(T, B)
    assert len(corners) == 4, "There aren't 4 corners"
    assert len(edges) == 4 * (N - 2), "There are not the right number of edges"
    
    print("Part 1 —", corners[0].id * corners[1].id * corners[2].id * corners[3].id)
    
    I = solve_puzzle(T, B, N, corners[0])
    monster = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
         [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]]
    )

    rotations = [lambda img: np.rot90(img, i) for i in range(1, 4)]
    for transform in [lambda img: img, *rotations, lambda img: img[::-1], *rotations]:
        I = transform(I)
        n_monsters = find_monsters(I, monster)
        if n_monsters != 0:
            break

    print("Part 2 —", I.sum() - n_monsters * monster.sum())


