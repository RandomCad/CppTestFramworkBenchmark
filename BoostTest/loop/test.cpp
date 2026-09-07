#define BOOST_TEST_MODULE LoopTest
#include <boost/test/included/unit_test.hpp>

#include <random>

namespace {
constexpr int ITERATIONS = 1'000'000;
}

BOOST_AUTO_TEST_CASE(increment_twice_equals_add_two)
{
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i) {
        int x = dist(rng);
        int a = x;
        a++;
        a++;
        int b = x + 2;
        BOOST_TEST(a == b);
    }
}
