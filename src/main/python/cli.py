import argparse
from main import BitcoinPuzzleSolver

def parse_arguments():
    parser = argparse.ArgumentParser(description="Bitcoin Puzzle Solver")
    parser.add_argument("--threads", type=int, help="Number of threads to use")
    parser.add_argument("--batch-size", type=int, help="Batch size for processing")
    parser.add_argument("--use-gpu", action="store_true", help="Use GPU for computations if available")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    solver = BitcoinPuzzleSolver()
    
    if args.threads:
        solver.threads = args.threads
    if args.batch_size:
        solver.batch_size = args.batch_size
    if args.use_gpu:
        solver.config['puzzle']['use_gpu'] = True

    private_key, address = solver.solve_puzzle()
    print(f"Solution found!")
    print(f"Private Key: {private_key}")
    print(f"Address: {address}")
