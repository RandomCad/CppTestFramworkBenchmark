#include "test.hpp"

#include "cute_runner.h"
#include "ide_listener.h"

int main() {
    cute::ide_listener<> listener{};
    bool success = cute::makeRunner(listener)(loop_test);
    return success ? 0 : 1;
}
