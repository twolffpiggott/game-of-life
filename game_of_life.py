import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def neighbours(cell):
    row, col = cell
    yield row - 1, col - 1 
    yield row - 1, col
    yield row - 1, col + 1
    yield row, col - 1
    yield row, col + 1
    yield row + 1, col - 1
    yield row + 1, col
    yield row + 1, col + 1

class Game:

    def __init__(self, board, name, bounds=(100, 100)):
        self.name = name
        self.bounds = bounds
        if isinstance(board, set):
            temp_board = board
        elif isinstance(board, np.ndarray):
            temp_board = {c for c in zip(np.nonzero(board)[0], np.nonzero(board)[1])} 
        else:
            raise TypeError('Initlialise Game with either a set or numpy array')
        self.minrow = min(temp_board, key=lambda x: x[0])[0]
        self.maxrow = max(temp_board, key=lambda x: x[0])[0]
        self.mincol = min(temp_board, key=lambda x: x[1])[1]
        self.maxcol = max(temp_board, key=lambda x: x[1])[1]
        row_increment = (bounds[0] - (self.maxrow - self.minrow + 1)) // 2
        col_increment = (bounds[1] - (self.maxcol - self.mincol + 1)) // 2
        self.board = set((c[0] - self.minrow + row_increment, c[1] - self.mincol + col_increment) for c in temp_board)

    def next_generation(self):
        new_board = set([])
        candidates = self.board | set(n for c in self.board for n in neighbours(c))
        for cell in candidates:
            count = sum((n in self.board) for n in neighbours(cell))
            if (count == 3) or (count == 2 and cell in self.board):
                new_board.add(cell)
        self.board = new_board
        return self.board
        
    def to_array(self):
        X = np.zeros(self.bounds)
        X[np.array([c[0] for c in self.board]), np.array([c[1] for c in self.board])] = 1
        return X

    def animate(self, dpi=600, frames=10, interval=300):
        X = self.to_array()
        X_blank = np.zeros_like(X)
        figsize = (X.shape[1] * 1. / dpi, X.shape[0] * 1. / dpi)
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        im = ax.imshow(X, cmap=plt.cm.binary)
        
        def init():
            im.set_data(X_blank)
            return (im,)

        def animate(frame):
            im.set_data(animate.X)      
            self.next_generation()
            animate.X = self.to_array()
            return (im,)
        
        animate.X = X

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frames, interval=interval)
        anim.save(f'{self.name.replace(" ", "_").lower()}.gif', writer='imagemagick', fps=frames//5)
        

