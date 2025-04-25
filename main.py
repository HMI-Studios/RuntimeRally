import sys


class Bot:
    def __init__(self, id, x, y, d):
        self.id = id
        self.x, self.y, self.d = x, y, d
        self.next_x, self.next_y, self.next_d = self.x, self.y, self.d
        self.inputs = None

    def move(self, speed):
        if self.d == 0:
            self.next_x += 0
            self.next_y -= speed
        elif self.d == 1:
            self.next_x += speed
            self.next_y += 0
        elif self.d == 2:
            self.next_x += 0
            self.next_y += speed
        elif self.d == 3:
            self.next_x -= speed
            self.next_y += 0

    def turn(self, direction):
        self.next_d = (self.next_d + direction) % 4

    def step(self):
        moved = self.x != self.next_x or self.y != self.next_y
        rotated = self.d != self.next_d

        self.x = self.next_x
        self.y = self.next_y
        self.d = self.next_d

        updates = []
        if moved:
            updates.append(f"MOVE {self.id} {self.x} {self.y}")
        if rotated:
            updates.append(f"ROTATE {self.id} {self.d}")

        return updates

class Tile:
    pass

class Wall(Tile):
    pass

class Floor(Tile):
    pass

class Board:
    def __init__(self, width, height, bot_count, map_lines):
        self.width = width
        self.height = height
        self.bot_count = bot_count
        self.bots = {}
        self.updates = []

        self.spawn_points = {}
        self.map_tiles = []

        tile_types = {
            '#': Wall,
            '.': Floor,
        }

        print(width, height, bot_count)
        clean_map = []
        for y, row in enumerate(map_lines):
            new_row = ""
            self.map_tiles.append([])
            for x, char in enumerate(row):
                if char.isdigit():
                    bot_id = int(char)
                    if bot_id < bot_count:
                        self.spawn_points[bot_id] = (x, y)
                        bot = Bot(bot_id, x, y, 0)
                        self.bots[bot_id] = bot
                        self.update(f"SPAWN {bot_id} {bot.x} {bot.y} {bot.d}")
                    new_char = '.'
                else:
                    new_char = char
                self.map_tiles[y].append(new_char)
                new_row += new_char
            clean_map.append(new_row)

        for i in range(self.bot_count):
            if i not in self.bots:
                raise RuntimeError(f"Bot {i} has no spawnpoint!")
            
        for line in clean_map:
            print(line)

    def update(self, update):
        self.updates.append(update)

    def step(self):
        for i in range(self.bot_count):
            bot = self.bots[i]
            cmds = bot.inputs
            bot.inputs = None
            if cmds is None:
                raise RuntimeError(f"Bot {i} did not send its commands this cycle!")
            
            for cmd in cmds:
                cmd = cmd.lower()
                if cmd == 'forward':
                    bot.move(1)
                elif cmd == 'reverse':
                    bot.move(-1)
                elif cmd == 'dash':
                    bot.move(2)
                elif cmd == 'left':
                    bot.turn(-1)
                elif cmd == 'right':
                    bot.turn(1)

            for update in bot.step():
                self.update(update)

    def send_updates(self):


        print(len(self.updates))
        for update in self.updates:
            print(update)
        sys.stdout.flush()
        self.updates = []
    
    def read_inputs(self):
        for i in range(self.bot_count):
            bot_id, *cmds = input().split(' ')
            bot_id = int(bot_id)

            if bot_id not in self.bots:
                raise KeyError('No such bot.')
            
            bot = self.bots[bot_id]
            if bot.inputs is not None:
                raise RuntimeError('Only one cmd per cycle allowed.')

            bot.inputs = cmds


def main():
    width, height, bot_count = [int(i) for i in input().strip().split()]
    map_lines = []
    for _ in range(height):
        row = input().strip()
        map_lines.append(row)

    board = Board(width, height, bot_count, map_lines)
    sys.stdout.flush()
    while True:
        board.send_updates() 

        try:
            board.read_inputs()
        except EOFError:
            break  # End of input stream

        board.step()


if __name__ == "__main__":
    main()
