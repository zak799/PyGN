import subprocess
import os # time

class Stockfish:
    def __init__(self, path = "stockfish/stockfish-windows-x86-64-avx2.exe"):
        self.stockfish = subprocess.Popen(
            path,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            encoding = "UTF-8",
            universal_newlines=True,
            bufsize = 1,
        )

    def wipe(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def send_cmd(self, cmd):
        self.stockfish.stdin.write(cmd + "\n")
        self.stockfish.stdin.flush()
    
    def fetch_resp(self, wait):
        while True:
            # time.sleep(0.1)
            line = self.stockfish.stdout.readline().strip()
            print(line)
            if wait in line: 
                break
    
    def fetch_next_move(self, fen_pos):
        self.send_cmd(f"position fen {fen_pos}")
        self.send_cmd("go depth 15")
        while True:
            line = self.stockfish.stdout.readline().strip()
            if line.startswith("bestmove"):
                return line.split(" ")[1]