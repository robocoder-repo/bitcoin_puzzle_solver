import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy as np

cuda_code = """
__global__ void generate_private_keys(unsigned char *keys, int num_keys) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < num_keys) {
        for (int i = 0; i < 32; i++) {
            keys[idx * 32 + i] = (unsigned char)(rand() & 0xFF);
        }
    }
}
"""

class GPUKeyGenerator:
    def __init__(self):
        self.mod = SourceModule(cuda_code)
        self.generate_private_keys = self.mod.get_function("generate_private_keys")

    def generate_keys(self, num_keys):
        keys = np.zeros((num_keys, 32), dtype=np.uint8)
        keys_gpu = cuda.mem_alloc(keys.nbytes)

        block_size = 256
        grid_size = (num_keys + block_size - 1) // block_size

        self.generate_private_keys(
            keys_gpu,
            np.int32(num_keys),
            block=(block_size, 1, 1),
            grid=(grid_size, 1)
        )

        cuda.memcpy_dtoh(keys, keys_gpu)
        return [''.join(f'{b:02x}' for b in key) for key in keys]

gpu_key_generator = GPUKeyGenerator()
