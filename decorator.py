from stockfish import Stockfish
from parser import Parser

stockfishy = Stockfish()
pgn_parser = Parser()
pgn_parser.fetch_pgn("game.pgn")

def apply_stock(func):
    def wrapper(*args, **kwargs):
        return func(*args,
                    send_cmd=stockfishy.send_cmd,
                    fetch_resp=stockfishy.fetch_resp,
                    wipe=stockfishy.wipe,
                    parse_moves=lambda: pgn_parser.parse_pgn(),
                    **kwargs)
    return wrapper