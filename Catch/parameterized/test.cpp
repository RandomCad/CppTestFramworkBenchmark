#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>
#include <catch2/generators/catch_generators_range.hpp>

#include <random>
#include <vector>

namespace {

constexpr int ITERATIONS = 1'000'000;

std::vector<int> makeValues() {
    std::vector<int> values;
    values.reserve(ITERATIONS);

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i) {
        values.push_back(dist(rng));
    }

    return values;
}

} // namespace

TEST_CASE("increment twice equals add two", "[parameterized]") {
    static const std::vector<int> values = makeValues();

    int x = GENERATE(from_range(values));

    int a = x;
    a++;
    a++;
    int b = x + 2;

    REQUIRE(a == b);
}
