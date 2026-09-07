#include <cppunit/extensions/HelperMacros.h>

#include <random>

constexpr int ITERATIONS = 1'000'000;

class LoopTest : public CppUnit::TestFixture {
    CPPUNIT_TEST_SUITE(LoopTest);
    CPPUNIT_TEST(testIncrementLoop);
    CPPUNIT_TEST_SUITE_END();

public:
    void testIncrementLoop() {
        std::mt19937 rng(42);
        std::uniform_int_distribution<int> dist(-1000000, 1000000);

        for (int i = 0; i < ITERATIONS; ++i) {
            int x = dist(rng);

            int a = x;
            a++;
            a++;
            int b = x + 2;

            CPPUNIT_ASSERT(a == b);
        }
    }
};

CPPUNIT_TEST_SUITE_REGISTRATION(LoopTest);
