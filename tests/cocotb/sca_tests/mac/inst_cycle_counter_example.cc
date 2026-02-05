/*
 * Copyright 2025 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "sw/utils/utils.h"
volatile uint32_t cycle_count_lo;
volatile uint32_t cycle_count_hi;
volatile uint32_t inst_count_lo;
volatile uint32_t inst_count_hi;
volatile uint32_t input1[8];
volatile uint32_t input2[8];
volatile uint32_t output[8];
int main(void) {
  cycle_counter_reset();
  uint64_t cycle_start = mcycle_read();
  for (int i = 0; i <8; i++) {
    output[i] = input1[i] + input2[i];
    output[i] = input1[i] * input2[i] + i;
  }
  uint64_t cycle_end = mcycle_read();
  uint64_t cycle_count = cycle_end - cycle_start;

  cycle_count_lo = cycle_count & 0xFFFFFFFF;
  cycle_count_hi = cycle_count >> 32;
  return 0;
}
