#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>

// Naive matrix multiplication: C = A x B
void naiveMultiply(const std::vector<double>& A,
                   const std::vector<double>& B,
                   std::vector<double>& C,
                   int N) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}

// Cache-aware (tiled) matrix multiplication: C = A x B with blocking
void tiledMultiply(const std::vector<double>& A,
                   const std::vector<double>& B,
                   std::vector<double>& C,
                   int N,
                   int BS) {
    // Initialize C to zero
    std::fill(C.begin(), C.end(), 0.0);

    for (int ii = 0; ii < N; ii += BS) {
        for (int kk = 0; kk < N; kk += BS) {
            for (int jj = 0; jj < N; jj += BS) {
                int iMax = std::min(ii + BS, N);
                int kMax = std::min(kk + BS, N);
                int jMax = std::min(jj + BS, N);
                for (int i = ii; i < iMax; ++i) {
                    for (int k = kk; k < kMax; ++k) {
                        double a = A[i * N + k];
                        for (int j = jj; j < jMax; ++j) {
                            C[i * N + j] += a * B[k * N + j];
                        }
                    }
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    // Default matrix size and block size
    int N = 1000;
    int BS = 32;
    if (argc > 1) N = std::stoi(argv[1]);
    if (argc > 2) BS = std::stoi(argv[2]);

    std::cout << "Matrix size: " << N << " x " << N
              << ", Block size: " << BS << std::endl;

    // Allocate and initialize matrices
    std::vector<double> A(N * N), B(N * N), C(N * N);
    std::mt19937_64 rng(0);
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    for (auto& x : A) x = dist(rng);
    for (auto& x : B) x = dist(rng);

    // Measure naive multiplication
    auto t1 = std::chrono::high_resolution_clock::now();
    naiveMultiply(A, B, C, N);
    auto t2 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> durNaive = t2 - t1;
    std::cout << "Naive multiplication took "
              << durNaive.count() << " seconds" << std::endl;

    // Measure tiled multiplication
    std::fill(C.begin(), C.end(), 0.0);
    auto t3 = std::chrono::high_resolution_clock::now();
    tiledMultiply(A, B, C, N, BS);
    auto t4 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> durTiled = t4 - t3;
    std::cout << "Tiled multiplication took "
              << durTiled.count() << " seconds" << std::endl;

    return 0;
}

