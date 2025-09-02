class Parser:
    def __init__(self, pgn=None):
        self.lines = []
        self.moves = []
        self.pgn = pgn
        if pgn:
            self.lines = pgn.strip().split("\n")

    def fetch_pgn(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.pgn = f.read()
            self.lines = self.pgn.strip().split('\n')

    def parse_pgn(self):
        for line in self.lines:
            if not line.startswith("["):
                self.moves.extend(line.strip().split())

        parsed_moves = []
        for token in self.moves:
            if token[0].isdigit() and "." in token:
                continue
            elif token in ["1-0", "0-1", "1/2-1/2", "*"]:
                continue
            parsed_moves.append(token)
        return parsed_moves

