import sys
import importlib.util
import subprocess

MAP_FILE = "samples/1.in"
SIMULATOR_CMD = ["python3", "main.py"]

def load_bot(name):
    bot_file = f"bots/{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}.py", bot_file)
    bot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot)
    return bot.decide_move

def parse_map(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        width, height, bot_count = map(int, first_line.strip().split())
        map_lines = [f.readline().rstrip() for _ in range(height)]
        bot_lines = [f.readline().rstrip() for _ in range(bot_count)]

    return width, height, bot_count, map_lines, bot_lines

def main():
    width, height, bot_count, map_data, bot_lines = parse_map(MAP_FILE)

    simulator = subprocess.Popen(SIMULATOR_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    simulator.stdin.write(f"{width} {height} {bot_count}\n")
    for row in map_data:
        simulator.stdin.write(row + "\n")
    simulator.stdin.flush()
    sys.stdout.flush()

    bots = {}
    for i in range(1, bot_count):
        bots[i] = load_bot(bot_lines[i-1])

    run = True
    for _ in range(height + 1):
        try:
            sim_line = simulator.stdout.readline()
            if not sim_line:
                break

            sim_line = sim_line.strip()

            print(sim_line)
        except KeyboardInterrupt:
            run = False
            break

    while run:
        try:
            sim_line = simulator.stdout.readline()
            if not sim_line:
                break

            sim_line = sim_line.strip()
            print(sim_line)
            sys.stdout.flush()

            n = int(sim_line)
            updates = [simulator.stdout.readline().strip() for _ in range(n)]

            for update in updates:
                try:
                    args = update.split(' ')
                    if args[0] == 'R':
                        if int(args[1]) == 0:
                            print(' '.join(args[2:]))
                    else:
                        print(update)
                except ValueError:
                    continue
            sys.stdout.flush()

            try:
                user_move = input().strip()
            except EOFError:
                user_move = "ABORT"

            simulator.stdin.write(f"0 {user_move}\n")

            for bot_id, bot in bots.items():
                move = bot(map_data, updates)
                simulator.stdin.write(f"{bot_id} {move}\n")

            simulator.stdin.flush()
        except KeyboardInterrupt:
            break
        except ValueError:
            break

    simulator.terminate()

if __name__ == "__main__":
    main()
