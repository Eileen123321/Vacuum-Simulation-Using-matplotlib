import matplotlib.pyplot as plt
import matplotlib.image as mpimg
 # 1 dirty 0 clean
grid = [
    [1, 1, 0, 1, 0],
    [0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
]

rows, cols = len(grid), len(grid[0])
r, c = 0, 4

sprite_img = mpimg.imread(r"C:/Users/j9cha/OneDrive/Desktop/vacuumSprite.png")

#define surrounding cells
def in_bound_cells(rr, cc):
    return 0 <= rr < rows and 0 <= cc < cols

#check surrounding cells
def neighbors(rr, cc):    
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        r2, c2 = rr + dr, cc + dc
        if in_bound_cells(r2, c2):
            yield (r2, c2)

#to check and see if the block is dirty, if it is clean then return
def dirty(g):
    return any(1 in row for row in g)

def find_nearest_dirty(rr, cc):
    targets = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 1]
    if not targets:
        return None
    return min(targets, key=lambda p: abs(p[0] - rr) + abs(p[1] - cc))


# size of each cells within the grid
def cell_extent(rr, cc):
    return [cc - 0.5, cc + 0.5, rr - 0.5, rr + 0.5]


# size of sprite
plt.ion()
fig, ax = plt.subplots(figsize=(4, 4))


plotted_grid = ax.imshow(grid, cmap="Greys", interpolation="nearest", origin="upper", zorder=1)
ax.set_title("Vacuum — black:dirt white:clean")


sprite = ax.imshow(sprite_img, extent=cell_extent(r, c), origin="upper", zorder=3)


ax.set_xlim(-0.5, cols - 0.5)
ax.set_ylim(rows - 0.5, -0.5)   
ax.set_xticks(range(cols)); ax.set_yticks(range(rows))
ax.set_aspect('equal')

def step():
    global r, c, grid

    #  Clean current cell if dirty
    if grid[r][c] == 1:
        grid[r][c] = 0
        plotted_grid.set_data(grid)
        return

    
    for rr, cc in neighbors(r, c):
        if grid[rr][cc] == 1:
            r, c = rr, cc
            return

    # Look for any dirty cells adjacent, if there are none, sprite will be prompted to move forward
    # If surrounded by white, sprite will head one step toward nearest dirty cell
    target = find_nearest_dirty(r, c)
    if target:
        tr, tc = target
        if r < tr: r += 1
        elif r > tr: r -= 1
        elif c < tc: c += 1
        elif c > tc: c -= 1
        return
    

# Run until all dirt is gone
steps = 0
MAX_STEPS = 1000
while dirty(grid) and steps < MAX_STEPS:
    step()
    sprite.set_extent(cell_extent(r, c))
    plt.pause(0.2)
    steps += 1

plt.ioff()
plt.show()
