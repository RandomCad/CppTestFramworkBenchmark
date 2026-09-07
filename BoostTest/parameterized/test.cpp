#define BOOST_TEST_MODULE ParameterizedTests
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/monomorphic.hpp>
#include <boost/test/data/test_case.hpp>

#include <random>
#include <vector>

namespace {

constexpr int ITERATIONS = 1'000'000;

std::vector<int> make_values()
{
    std::vector<int> values;
    values.reserve(ITERATIONS);

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i)
        values.push_back(dist(rng));

    return values;
}

const std::vector<int> g_values = make_values();

} // namespace

BOOST_DATA_TEST_CASE(increment_twice_equals_add_two, g_values, x)
{
    int a = x;
    a++;
    a++;
    int b = x + 2;
    BOOST_TEST(a == b);
}
