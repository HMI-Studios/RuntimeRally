import sys


class Board:
    def __init__(self, width, height, bot_count, map_data):
        self.width = width
        self.height = height
        self.bot_count = bot_count
        self.map_data = map_data
        self.inputs = {}
        self.updates = []

    def send_updates(self):
        print(f"CYCLE {len(self.updates)}")
        for update in self.updates:
            print(update)
        sys.stdout.flush()
        self.updates = []
    
    def read_inputs(self):
        self.inputs = { str(i): None for i in range(self.bot_count) }
        for i in range(self.bot_count):
            bot, *cmds = input().split(' ')

            if bot not in self.inputs:
                raise KeyError('No such bot.')
            if self.inputs[bot] is not None:
                raise RuntimeError('Only one cmd per cycle allowed.')

            self.inputs[bot] = cmds

            self.updates.append(f"{bot}")
            self.updates.append(cmds)


def main():
    width, height, bot_count = [int(i) for i in input().strip().split()]
    map_data = []
    for i in range(height):
        map_data.append([])
        row = input().strip()
        for char in row:
            map_data[i].append(char)

    board = Board(width, height, bot_count, map_data)
    while True:
        board.send_updates() 

        try:
            board.read_inputs()
        except EOFError:
            break  # End of input stream


if __name__ == "__main__":
    main()
