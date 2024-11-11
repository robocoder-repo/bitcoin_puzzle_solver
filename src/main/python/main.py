import logging
from logging.handlers import RotatingFileHandler
import yaml
from typing import List, Dict
import os
import multiprocessing
import time
from pybloom_live import ScalableBloomFilter
from bitcoin_utils import private_key_to_address
from genetic_solver import GeneticSolver
from quantum_inspired import QuantumInspiredSolver
from oversight_agent import OversightAgent
from tqdm import tqdm
from gpu_utils import gpu_key_generator

class BitcoinPuzzleSolver:
    def __init__(self):
        self.config = self.load_config()
        self.setup_logging()
        self.target_addresses = self.load_target_addresses()
        self.bloom_filter = self.setup_bloom_filter()
        self.batch_size = self.config['puzzle']['batch_size']
        self.threads = self.config['puzzle']['threads']
        self.use_gpu = self.config['puzzle'].get('use_gpu', False)
        self.genetic_solver = GeneticSolver(self.target_addresses)
        self.quantum_solver = QuantumInspiredSolver(self.target_addresses)
        self.oversight_agent = OversightAgent()
        self.total_attempts = 0

    def load_config(self):
        with open('config/config.yml', 'r') as file:
            return yaml.safe_load(file)

    def setup_logging(self):
        log_config = self.config['logging']
        handler = RotatingFileHandler(
            log_config['file'],
            maxBytes=log_config['max_file_size'],
            backupCount=log_config['backup_count']
        )
        logging.basicConfig(
            level=log_config['level'],
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[handler]
        )

    def load_target_addresses(self) -> List[str]:
        with open(self.config['puzzle']['target_addresses_file'], 'r') as file:
            return [line.strip() for line in file]

    def setup_bloom_filter(self):
        if self.config['optimization']['use_bloom_filter']:
            return ScalableBloomFilter(
                mode=ScalableBloomFilter.LARGE_SET_GROWTH,
                initial_capacity=self.config['optimization']['bloom_filter_size'],
                error_rate=self.config['optimization']['bloom_filter_fp_prob']
            )
        return None

    def generate_private_keys(self, batch_size) -> List[str]:
        if self.use_gpu:
            return gpu_key_generator.generate_keys(batch_size)
        return [os.urandom(32).hex() for _ in range(batch_size)]

    def check_address(self, address: str) -> bool:
        if self.bloom_filter:
            if address not in self.bloom_filter:
                return False
        return address in self.target_addresses

    def process_batch(self, batch_size):
        private_keys = self.generate_private_keys(batch_size)
        for private_key in private_keys:
            address = private_key_to_address(private_key)
            if self.check_address(address):
                return private_key, address
        return None, None

    def solve_puzzle(self):
        start_time = time.time()
        pbar = tqdm(total=None, desc="Solving puzzle", unit="attempts")

        try:
            with multiprocessing.Pool(self.threads) as pool:
                while True:
                    # Try quantum-inspired approach
                    quantum_private_key, quantum_address = self.quantum_solver.quantum_inspired_search()
                    if quantum_private_key:
                        self.oversight_agent.recognize_concept("Quantum superposition used in search")
                        return self.log_solution(quantum_private_key, quantum_address, "quantum-inspired", pbar)

                    # Try genetic algorithm approach
                    if self.total_attempts % 1000000 == 0:
                        genetic_private_key, genetic_address = self.genetic_solver.evolve(generations=100)
                        if genetic_private_key:
                            self.oversight_agent.recognize_concept("Genetic algorithm evolution completed")
                            return self.log_solution(genetic_private_key, genetic_address, "genetic algorithm", pbar)

                    # Brute force approach
                    results = pool.map(self.process_batch, [self.batch_size] * self.threads)
                    self.total_attempts += self.batch_size * self.threads
                    pbar.update(self.batch_size * self.threads)

                    for private_key, address in results:
                        if private_key:
                            return self.log_solution(private_key, address, "brute force", pbar)

                    if self.total_attempts % 1000000 == 0:
                        self.log_progress(start_time)

        except Exception as e:
            error_message = self.oversight_agent.handle_error(e)
            logging.error(error_message)
            pbar.close()
            return None, None

    def log_solution(self, private_key, address, method, pbar):
        elapsed_time = time.time() - self.start_time
        logging.info(f"Found matching address using {method} after {self.total_attempts} attempts in {elapsed_time:.2f} seconds!")
        logging.info(f"Private Key: {private_key}")
        logging.info(f"Address: {address}")
        pbar.close()
        return private_key, address

    def log_progress(self, start_time):
        elapsed_time = time.time() - start_time
        keys_per_second = self.total_attempts / elapsed_time
        logging.info(f"Attempted {self.total_attempts} keys in {elapsed_time:.2f} seconds")
        self.oversight_agent.log_performance("keys_per_second", keys_per_second)
        
        performance_data = {
            "keys_per_second": keys_per_second,
            "memory_usage": psutil.virtual_memory().percent / 100
        }
        optimization_suggestion = self.oversight_agent.suggest_optimization(performance_data)
        logging.info(f"Optimization suggestion: {optimization_suggestion}")

if __name__ == "__main__":
    solver = BitcoinPuzzleSolver()
    solver.solve_puzzle()
