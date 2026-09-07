#include <gtest/gtest.h>

#include <random>
#include <vector>

namespace {

constexpr int ITERATIONS = 1'000'000;

std::vector<int> GenerateValues() {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    std::vector<int> values;
    values.reserve(ITERATIONS);
    for (int i = 0; i < ITERATIONS; ++i) {
        values.push_back(dist(rng));
    }
    return values;
}

class IncrementTest : public ::testing::TestWithParam<int> {};

TEST_P(IncrementTest, IncrementTwiceEqualsAddTwo) {
    int x = GetParam();

    int a = x;
    a++;
    a++;
    int b = x + 2;

    ASSERT_EQ(a, b);
}

INSTANTIATE_TEST_SUITE_P(
    GeneratedValues,
    IncrementTest,
    ::testing::ValuesIn(GenerateValues()));

}  // namespace
