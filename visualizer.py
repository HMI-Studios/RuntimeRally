import os
import sys
import subprocess

MAP_FILE = "samples/3.in"
SIMULATOR_CMD = ["python3", "main.py"]

def parse_map(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        width, height, bot_count = map(int, first_line.strip().split())
        map_lines = [f.readline().rstrip() for _ in range(height)]

    return width, height, bot_count, map_lines

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_map(map_data, bot_positions, log):
    display = [list(row) for row in map_data]
    for _, (x, y, direction) in bot_positions.items():
        display[y][x] = ['^', '>', 'v', '<'][direction]
    for i in range(len(display)):
        row = ''.join(display[i])
        log_index = i - min(len(log), len(map_data))
        if log_index < 0:
            row += f"    > {log[log_index]}"
        print(row)

def main():
    width, height, bot_count, map_lines = parse_map(MAP_FILE)

    simulator = subprocess.Popen(SIMULATOR_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    simulator.stdin.write(f"{width} {height} {bot_count}\n")
    for row in map_lines:
        simulator.stdin.write(row + "\n")
    simulator.stdin.flush()
    sys.stdout.flush()

    run = True
    sim_line = simulator.stdout.readline()
    map_data = []
    for _ in range(height):
        try:
            sim_line = simulator.stdout.readline()
            sim_line = sim_line.strip()
            map_data.append(sim_line)
        except KeyboardInterrupt:
            run = False
            break

    log = []
    bot_positions = {}
    while run:
        try:
            sim_line = simulator.stdout.readline()
            if not sim_line:
                break

            sim_line = sim_line.strip()

            n = int(sim_line)
            updates = [simulator.stdout.readline().strip() for _ in range(n)]

            for update in updates:
                log.append(update)

                args = update.split(' ')
                if args[0] == 'SPAWN':
                    id, x, y, d = [int(arg) for arg in args[1:]]
                    bot_positions[id] = (x, y, d)
                elif args[0] == 'MOVE':
                    id, x, y = [int(arg) for arg in args[1:]]
                    _, _, d = bot_positions[id]
                    bot_positions[id] = (x, y, d)
                elif args[0] == 'ROTATE':
                    id, d = [int(arg) for arg in args[1:]]
                    x, y, _ = bot_positions[id]
                    bot_positions[id] = (x, y, d)

            clear_screen()
            render_map(map_data, bot_positions, log)

            for i in range(bot_count):
                user_move = input(f"Bot {i}: ").strip()
                simulator.stdin.write(f"{i} {user_move}\n")

            simulator.stdin.flush()
        except KeyboardInterrupt:
            break
        except ValueError:
            break

    simulator.terminate()

if __name__ == "__main__":
    main()
