from decorator import apply_stock
from HexText import HexText
from parser import Parser
import json


pgn_parser = Parser()
pgn_parser.fetch_pgn("game.pgn")
colorText = HexText()

@apply_stock
def run_stock(send_cmd, fetch_resp, wipe, parse_moves):
    global moves
    send_cmd("uci"); fetch_resp("uciok")
    send_cmd("isready"); fetch_resp("readyok")
    wipe()
    moves = parse_moves()
    return moves

if __name__ == "__main__":
    run_stock()

    status = ["uciok", "readyok"]

    for item in status:
        print(f"{colorText('[SUCCESS] - ', color='#00ff15')}{item}")
    print(f"{colorText('[INFO] Parsed moves:', color="#f700ff")} {json.dumps(moves)}")
