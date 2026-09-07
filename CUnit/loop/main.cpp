#include "test.hpp"

#include <CUnit/Basic.h>
#include <CUnit/CUnit.h>

int main() {
    if (CU_initialize_registry() != CUE_SUCCESS) {
        return static_cast<int>(CU_get_error());
    }

    if (register_loop_suite() == nullptr) {
        CU_cleanup_registry();
        return static_cast<int>(CU_get_error());
    }

    CU_basic_set_mode(CU_BRM_NORMAL);
    CU_basic_run_tests();

    unsigned int failures = CU_get_number_of_failures();
    CU_cleanup_registry();

    return failures == 0 ? 0 : 1;
}
