#define CESTER_NO_MAIN
#include <exotic/cester.h>

#include <random>

CESTER_BODY(
constexpr int ITERATIONS = 1'000'000;
)

CESTER_TEST(increment_twice_equals_add_two, instance,
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);

    for (int i = 0; i < ITERATIONS; ++i) {
        int x = dist(rng);
        int a = x;
        a++;
        a++;
        int b = x + 2;
        cester_assert_int_eq(a, b);
    }
)

CESTER_BODY(
int main(int argc, char** argv) {
    CESTER_REGISTER_TEST(increment_twice_equals_add_two);
    return CESTER_RUN_ALL_TESTS(argc, argv);
}
)
