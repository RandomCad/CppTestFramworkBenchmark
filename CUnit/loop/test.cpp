#include "test.hpp"

#include <CUnit/CUnit.h>
#include <random>

namespace {

constexpr int ITERATIONS = 1'000'000;

void test_increment_matches_addition() {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i) {
        int x = dist(rng);

        int a = x;
        a++;
        a++;
        int b = x + 2;

        CU_ASSERT_EQUAL(a, b);
    }
}

} // namespace

extern "C" CU_pSuite register_loop_suite(void) {
    CU_pSuite suite = CU_add_suite("loop_suite", nullptr, nullptr);
    if (suite == nullptr) {
        return nullptr;
    }

    if (CU_add_test(suite, "test_increment_matches_addition", test_increment_matches_addition) == nullptr) {
        return nullptr;
    }

    return suite;
}
