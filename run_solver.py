import argparse
from src.main.python.main import BitcoinPuzzleSolver

def parse_arguments():
    parser = argparse.ArgumentParser(description="Bitcoin Puzzle Solver with Quantum-Inspired Algorithms")
    parser.add_argument("--threads", type=int, help="Number of threads to use")
    parser.add_argument("--batch-size", type=int, help="Batch size for processing")
    parser.add_argument("--use-gpu", action="store_true", help="Use GPU for computations if available")
    parser.add_argument("--quantum-iterations", type=int, default=1000, help="Number of iterations for quantum-inspired search")
    parser.add_argument("--genetic-generations", type=int, default=100, help="Number of generations for genetic algorithm")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    solver = BitcoinPuzzleSolver()
    
    if args.threads:
        solver.threads = args.threads
    if args.batch_size:
        solver.batch_size = args.batch_size
    if args.use_gpu:
        solver.use_gpu = True
    
    solver.quantum_solver.iterations = args.quantum_iterations
    solver.genetic_solver.generations = args.genetic_generations

    private_key, address = solver.solve_puzzle()
    
    if private_key and address:
        print(f"Solution found!")
        print(f"Private Key: {private_key}")
        print(f"Address: {address}")
    else:
        print("No solution found. Please check the logs for more information.")
