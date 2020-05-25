# battleship
import sys

class Ship():
    def __init__(self, name, size, symbol):
        self.name = name
        self.size = size
        self.symbol = symbol
        self.hits = 0

    def sunk(self):
        return self.hits == self.size

class GameBoard():

    def __init__(self, player, dim=10):
        self.player = player
        self.dim = dim  # dimension
        # self.board = list([list(dim * 'e')] * dim)
        self.board = [
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
            ['e','e','e','e','e','e','e','e','e','e'],
        ]
        self.ships = []
        self.carrier = Ship('carrier', 5, 'r')
        self.ships.append(self.carrier)
        self.battleship = Ship('battleship', 4, 'b')
        self.ships.append(self.battleship)
        self.cruiser = Ship('cruiser', 3, 'c')
        self.ships.append(self.cruiser)
        self.sub = Ship('sub', 3, 's')
        self.ships.append(self.sub)
        self.pt = Ship('pt', 2, 'p')
        self.ships.append(self.pt)

    def show_board(self, shots=False):
        print(f"player {self.player}'s board.")
        for x in range(self.dim):
            for y in range(self.dim):
                if shots: # only show shots
                    if self.board[x][y] in ['*', 'O']:
                        sys.stdout.write(self.board[x][y])
                    else:
                        sys.stdout.write('_')
                else:
                    if self.board[x][y] == 'e':
                        sys.stdout.write('_')
                    else:
                        sys.stdout.write(self.board[x][y])
            sys.stdout.write('\n')

    def overlap_vert(self, row, col, ship):
        r = 0
        for l in ship.size * ship.symbol:
            if self.board[row + r][col] != 'e':
                return True
            r += 1
        return False

    def overlap_hort(self, row, col, ship):
        c = 0
        for l in ship.size * ship.symbol:
            if self.board[row][col + c] != 'e':
                return True
            c += 1
        return False

    def place_ship(self, ship):
        placing = True
        while placing:
          print(f'place {ship.name}.')
          row = int(input(f'enter row [0,{self.dim}]:'))
          col = int(input(f'enter col [0,{self.dim}]:'))
          ort = input(f'enter vert or hort [v,h]')

          if ort == 'h':
              if col + ship.size > self.dim:
                  print(f'{ship.name} out of bounds.')
                  continue
              else:
                  if self.overlap_hort(row,col,ship):
                      print(f'ship {ship.name} overlaps other ship.')
                  else:
                      c = 0
                      for l in ship.size * ship.symbol:
                          self.board[row][col + c] = l
                          c += 1
                      placing = False
          else:
              if row + ship.size > self.dim:
                  print(f'{ship.name} out of bounds.')
                  continue
              else:
                  if self.overlap_vert(row,col,ship):
                      print(f'ship {ship.name} overlaps other ship.')
                  else:
                      r = 0
                      for l in ship.size * ship.symbol:
                          self.board[row + r][col] = l
                          r += 1
                      placing = False
        self.show_board()

    def shoot(self):
        asking = True
        while asking:
            row = int(input('enter row [0,9].'))
            col = int(input('enter col [0,9].'))
            l = self.board[row][col]
            print(f'l is {l}')
            if l in ['*', 'O']:
                print('You already shot here. Try again.')
            else:
                asking = False
        hit = False
        l = self.board[row][col]
        if l == 'r':
            hit = True
            self.carrier.hits += 1
        if l == 'b':
            hit = True
            self.battleship.hits += 1
        if l == 'c':
            hit = True
            self.cruiser.hits += 1
        if l == 's':
            hit = True
            self.sub.hits += 1
        if l == 'p':
            hit = True
            self.pt.hits += 1
        if hit:
            self.board[row][col] = '*'
        else:
            self.board[row][col] = 'O'

    def gameover(self):
        ships_sunk = 0
        for ship in self.ships:
            if ship.sunk():
                ships_sunk += 1
        return ships_sunk == len(self.ships)

    def show_shoots(self):
        self.show_board(shots=True)

    def report_sunk_ships(self):
        for ship in self.ships:
            if ship.sunk():
                print(f"Player {self.player}'s {ship.name} sunk!" )

    def setup_board(self):
        self.place_ship(self.carrier)
        self.place_ship(self.battleship)
        self.place_ship(self.cruiser)
        self.place_ship(self.sub)
        self.place_ship(self.pt)


class BattleshipGame():

    def __init__(self):
        self.player_one = GameBoard(player='One', dim=10)
        self.player_two = GameBoard(player='Two', dim=10)

        print('Player one place ships!')
        self.player_one.setup_board()
        print('Player two place ships!')
        self.player_two.setup_board()

    def play(self):
        gameover = False
        while not gameover:
            self.player_one.show_board()
            print('player one to shoot!')
            self.player_two.report_sunk_ships()
            self.player_two.show_shoots()
            # player one shoots at player two's ships/board.
            self.player_two.shoot()
            if self.player_two.gameover():
                print('Player one winner!')
                self.player_one.show_board()
                self.player_two.show_board()
                gameover = True
                continue
            self.player_two.show_board()
            print('player two to shoot!')
            self.player_one.report_sunk_ships()
            self.player_one.show_shoots()
            self.player_one.shoot()
            if self.player_one.gameover():
                print('Player two winner!')
                self.player_one.show_board()
                self.player_two.show_board()
                gameover = True
                continue


def main():
    g = BattleshipGame()
    g.play()

if __name__ == "__main__":
    main()
