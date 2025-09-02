import chess
from parser import Parser
from stockfish import Stockfish

# Mapping chess pieces to emojis
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
        row = f"{rank} "  # rank label
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

def side_by_side(board1_str, board2_str, move_number):
    lines1 = board1_str.split('\n')
    lines2 = board2_str.split('\n')
    max_len1 = max(len(line) for line in lines1)

    print(f"\nMove {move_number}:")
    print(f"{'Original Game':<{max_len1 + 4}}Stockfish Best Line")
    for l1, l2 in zip(lines1, lines2):
        print(f"{l1:<{max_len1 + 4}}{l2}")
    print("-" * 56)

def step_by_step_playback(moves):
    board_orig = chess.Board()
    board_best = chess.Board()
    stockfish = Stockfish()

    move_idx = 0
    orig_done = False
    best_done = False

    while not (orig_done and best_done):
        move_idx += 1

        if not orig_done and move_idx <= len(moves):
            move_san = moves[move_idx - 1]
            try:
                move = board_orig.parse_san(move_san)
                board_orig.push(move)
                if board_orig.is_checkmate():
                    orig_done = True
            except:
                print(f"[!] Invalid move in PGN: {move_san}")
                orig_done = True
        else:
            orig_done = True

        if not best_done:
            best_move_uci = stockfish.fetch_next_move(board_best.fen())
            best_move = chess.Move.from_uci(best_move_uci)
            if best_move in board_best.legal_moves:
                board_best.push(best_move)
                if board_best.is_checkmate():
                    best_done = True
            else:
                best_done = True
        
        stockfish.wipe()

        board1_str = board_to_emoji(board_orig)
        board2_str = board_to_emoji(board_best)
        side_by_side(board1_str, board2_str, move_idx)

        if orig_done and best_done:
            print("[Checkmate] Both boards reached checkmate or no more moves.")
            break

        input("Press Enter for next move...")

if __name__ == "__main__":
    parser = Parser()
    parser.fetch_pgn("game.pgn")
    original_moves = parser.parse_pgn()

    step_by_step_playback(original_moves)
