#include <catch2/catch_test_macros.hpp>

#include <random>

namespace {
constexpr int ITERATIONS = 1'000'000;
}

TEST_CASE("increment twice equals add two", "[loop]") {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i) {
        int x = dist(rng);
        int a = x;
        a++;
        a++;
        int b = x + 2;
        REQUIRE(a == b);
    }
}
