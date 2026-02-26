# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cocotb
import numpy as np
import os
from bazel_tools.tools.python.runfiles import runfiles
from coralnpu_test_utils.sim_test_fixture import Fixture


@cocotb.test()
async def inst_cycle_counter_test(dut):
    LHS_ROWS = 16
    RHS_COLS = 16
    INNER = 48

    r = runfiles.Create()
    fixture = await Fixture.Create(dut)
    elf_path = r.Rlocation("coralnpu_hw/tests/cocotb/sca_tests/mac/inst_cycle_counter_example.elf")
    await fixture.load_elf_and_lookup_symbols(
        elf_path,
        ['cycle_count_lo', 'cycle_count_hi','lhs_input','rhs_input','result_output'],
    )
    np_type = np.int8
    min_value = np.iinfo(np_type).min
    max_value = np.iinfo(np_type).max + 1  # One above.
    lhs_data = np.random.randint(min_value,
                                 max_value, [LHS_ROWS, INNER],
                                 dtype=np_type)
    rhs_data = np.random.randint(min_value,
                                 max_value, [INNER, RHS_COLS],
                                 dtype=np_type)
    await fixture.write('lhs_input', lhs_data.flatten())
    await fixture.write('rhs_input', rhs_data.transpose().flatten())
    await fixture.run_to_halt(timeout_cycles=1000000)

    '''
    lhs_input = np.arange(256,dtype=np.uint8)
    rhs_input = (5 * np.ones(769, dtype=np.uint8))
    lhs_input_addr = fixture.symbols['lhs_input']
    rhs_input_addr = fixture.symbols['rhs_input']
    await fixture.core_mini_axi.write(lhs_input_addr, lhs_input)
    await fixture.core_mini_axi.write(rhs_input_addr, rhs_input)

    await fixture.run_to_halt()
    '''

    cycle_count_lo = (await fixture.read_word('cycle_count_lo')).view(np.int32)
    cycle_count_hi = (await fixture.read_word('cycle_count_hi')).view(np.int32)
#    inst_count_lo =  (await fixture.read_word('inst_count_lo')).view(np.int32)
#    inst_count_hi =  (await fixture.read_word('inst_count_hi')).view(np.int32)
    cycle_count = (cycle_count_hi << 32) | cycle_count_lo
#    instruction_count = (inst_count_hi << 32) | inst_count_lo
#    print(f" {instruction_count[0]} instructions are executed with {cycle_count[0]} compute cycles", flush=True)
    print(f"no .of cycles retired {cycle_count[0]}")
