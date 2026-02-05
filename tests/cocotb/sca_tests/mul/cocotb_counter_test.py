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
    r = runfiles.Create()
    fixture = await Fixture.Create(dut)
    elf_path = r.Rlocation("coralnpu_hw/tests/cocotb/sca_tests/mul/inst_cycle_counter_example.elf")
    await fixture.load_elf_and_lookup_symbols(
        elf_path,
        ['cycle_count_lo', 'cycle_count_hi', 'inst_count_lo', 'inst_count_hi','input1','input2','output'],
    )

    input1 = np.arange(8,dtype=np.uint32)
    input2 = (5 * np.ones(8, dtype=np.uint32))
    input1_addr = fixture.symbols['input1']
    input2_addr = fixture.symbols['input2']
    await fixture.core_mini_axi.write(input1_addr, input1)
    await fixture.core_mini_axi.write(input2_addr, input2)

    await fixture.run_to_halt()

    cycle_count_lo = (await fixture.read_word('cycle_count_lo')).view(np.int32)
    cycle_count_hi = (await fixture.read_word('cycle_count_hi')).view(np.int32)
#    inst_count_lo =  (await fixture.read_word('inst_count_lo')).view(np.int32)
#    inst_count_hi =  (await fixture.read_word('inst_count_hi')).view(np.int32)
    cycle_count = (cycle_count_hi << 32) | cycle_count_lo
#    instruction_count = (inst_count_hi << 32) | inst_count_lo
#    print(f" {instruction_count[0]} instructions are executed with {cycle_count[0]} compute cycles", flush=True)
    print(f"no .of cycles retired {cycle_count[0]}")
