import chess
from dataclasses import dataclass, field
from parser import Parser
from stockfish import Stockfish
import keyboard
import time


# Emoji map
EMOJI_PIECES = {
    chess.PAWN:   (" ♙ ", " ♟ "),
    chess.KNIGHT: (" ♘ ", " ♞ "),
    chess.BISHOP: (" ♗ ", " ♝ "),
    chess.ROOK:   (" ♖ ", " ♜ "),
    chess.QUEEN:  (" ♕ ", " ♛ "),
    chess.KING:   (" ♔ ", " ♚ "),
}

def board_to_emoji(board: chess.Board) -> str:
    rows = []
    for rank in range(8, 0, -1):
        row = f"{rank} "
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = board.piece_at(square)
            if piece:
                white_emoji, black_emoji = EMOJI_PIECES[piece.piece_type]
                row += white_emoji if piece.color == chess.WHITE else black_emoji
            else:
                row += " · "
        rows.append(row)
    rows.append("   a  b  c  d  e  f  g  h")
    return "\n".join(rows)

def side_by_side_as_str(board1_str, board2_str, move_number):
    lines1 = board1_str.split('\n')
    lines2 = board2_str.split('\n')
    max_len1 = max(len(line) for line in lines1)

    result = [f"\nMove {move_number}:"]
    result.append(f"{'Original Game':<{max_len1 + 4}}Stockfish Best Line")
    for l1, l2 in zip(lines1, lines2):
        result.append(f"{l1:<{max_len1 + 4}}{l2}")
    result.append("-" * 56)
    return "\n".join(result)

@dataclass
class GamePlayback:
    moves: list
    board_orig: chess.Board = field(default_factory=chess.Board)
    board_best: chess.Board = field(default_factory=chess.Board)
    stockfish: Stockfish = field(default_factory=Stockfish)
    move_idx: int = 0
    orig_done: bool = False
    best_done: bool = False
    history_orig: list = field(default_factory=list)
    history_best: list = field(default_factory=list)

    def play(self):
        while True:
            self.render()

            key = self.wait_for_key()
            if key == 'right':
                self.do_next_move()
            elif key == 'left':
                self.undo_move()
            elif key == 'q':
                break

    def render(self):
        import os; os.system("cls") if os.name == "nt" else os.system("clear")
        board1_str = board_to_emoji(self.board_orig)
        board2_str = board_to_emoji(self.board_best)
        combined = side_by_side_as_str(board1_str, board2_str, self.move_idx)
        print(combined + "\n(Enter = next, Backspace = undo, Q = quit)", flush=True)

    def do_next_move(self):
        self.move_idx += 1

        # Original move
        if not self.orig_done and self.move_idx <= len(self.moves):
            move_san = self.moves[self.move_idx - 1]
            try:
                move = self.board_orig.parse_san(move_san)
                self.history_orig.append(move)
                self.board_orig.push(move)
                if self.board_orig.is_checkmate():
                    self.orig_done = True
            except:
                print(f"[!] Invalid move in PGN: {move_san}")
                self.orig_done = True
        else:
            self.orig_done = True

        # Stockfish move
        if not self.best_done:
            best_move_uci = self.stockfish.fetch_next_move(self.board_best.fen())
            best_move = chess.Move.from_uci(best_move_uci)
            if best_move in self.board_best.legal_moves:
                self.history_best.append(best_move)
                self.board_best.push(best_move)
                if self.board_best.is_checkmate():
                    self.best_done = True
            else:
                self.best_done = True

        self.stockfish.wipe()

        if self.orig_done and self.best_done:
            print("[Checkmate] Both boards reached checkmate or no more moves.")
            time.sleep(2)

    def undo_move(self):
        if self.history_orig:
            self.board_orig.pop()
            self.history_orig.pop()
            self.orig_done = False
        if self.history_best:
            self.board_best.pop()
            self.history_best.pop()
            self.best_done = False
        self.move_idx = max(0, self.move_idx - 1)

    def wait_for_key(self):
        while True:
            if keyboard.is_pressed('right'):
                while keyboard.is_pressed('right'):
                    pass
                return 'right'
            elif keyboard.is_pressed('left'):
                while keyboard.is_pressed('left'):
                    pass
                return 'left'
            elif keyboard.is_pressed('q'):
                while keyboard.is_pressed('q'):
                    pass
                return 'q'
            time.sleep(0.05)

if __name__ == "__main__":
    parser = Parser()
    parser.fetch_pgn("game.pgn")
    original_moves = parser.parse_pgn()

    print("\n" * 50)  # Pad output so colorama Cursor.POS(0, 0) has space
    playback = GamePlayback(moves=original_moves)
    playback.play()