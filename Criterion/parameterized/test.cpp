#include <criterion/criterion.h>
#include <criterion/parameterized.h>

#include <random>

constexpr int ITERATIONS = 1'000'000;

ParameterizedTestParameters(increment, matches_add_two) {
    static int values[ITERATIONS];

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(-1000000, 1000000);
    for (int i = 0; i < ITERATIONS; ++i) {
        values[i] = dist(rng);
    }

    return cr_make_param_array(int, values, ITERATIONS);
}

ParameterizedTest(int *x_ptr, increment, matches_add_two) {
    int x = *x_ptr;

    int a = x;
    a++;
    a++;
    int b = x + 2;

    cr_assert(a == b);
}
