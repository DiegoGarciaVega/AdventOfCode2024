#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>

constexpr auto per_thread = 2 * 32768ULL;
constexpr auto per_iter = per_thread * 32768ULL;

__global__ void run(uint64_t base, unsigned long long* result)
{
    constexpr std::array<uint64_t, 16> prog = {2, 4, 1, 5, 7, 5, 0, 3, 1, 6, 4, 3, 5, 5, 3, 0};
    

    auto const idx = blockIdx.x * blockDim.x + threadIdx.x;

    for (auto offset = 0ULL; offset < per_thread; ++offset) {
        uint64_t const a_init = base + idx * per_thread + offset;
        uint64_t a = base + idx * per_thread + offset;

        for (auto i = 0; a > 0; ++i, a >>= 3) {
            uint64_t b =  (a % 8) ^5;
            uint64_t c = a / (1ULL << b);
            
            b = b^6;
            b = b^c;
            

            if ((b & 7) != prog[i]) break;

            if (i + 1 == prog.size()) {
                atomicMin(result, a_init);
                return;
            }
        }
    }
}

#define CHECK(code)                                                                      \
    if ((code) != cudaSuccess) {                                                         \
        std::cerr << "CUDA call failed at " << __FILE__ << ":" << __LINE__ << std::endl; \
        std::terminate();                                                                \
    }

int main()
{
    constexpr auto num_threads = 256;
    constexpr auto num_blocks = per_iter / per_thread / num_threads;

    unsigned long long* result_gpu = nullptr;
    CHECK(cudaMalloc(&result_gpu, sizeof(uint64_t)));

    uint64_t result = ~0;
    CHECK(cudaMemcpy(result_gpu, &result, sizeof(result), cudaMemcpyHostToDevice));

    auto begin = std::chrono::high_resolution_clock::now();

    constexpr auto iters_between_status = 1000ULL;

    for (uint64_t base = 35184372088832, i = 0;; base += per_iter, ++i) {
        run<<<num_blocks, num_threads>>>(base, result_gpu);
        uint64_t result;
        CHECK(cudaMemcpy(&result, result_gpu, sizeof(result), cudaMemcpyDeviceToHost));
        if (result != ~0) {
            std::cout << "Part 2: " << result << std::endl;
            break;
        }
        if ((i + 1) % iters_between_status == 0) {
            auto const done = (i + 1) * per_iter;
            auto const now = std::chrono::high_resolution_clock::now();
            std::cout << "base " << base << std::endl;
            std::cout << done << " values tried ("
                      << static_cast<double>(per_iter * iters_between_status) /
                            std::chrono::duration_cast<std::chrono::microseconds>(now - begin).count() / 1e3
                      << " * 10^9 it/s)" << std::endl;
            begin = now;
        }
    }

    return 0;
}