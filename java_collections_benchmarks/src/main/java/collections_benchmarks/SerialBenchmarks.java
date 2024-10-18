/*
 * Copyright (c) 2014, Oracle America, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *  * Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 *  * Neither the name of Oracle nor the names of its contributors may be used
 *    to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

package collections_benchmarks;

import java.util.List;

import org.openjdk.jmh.annotations.Level;
import org.openjdk.jmh.annotations.Param;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.Setup;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.infra.Blackhole;

public class SerialBenchmarks extends BaseBenchmarks {


    @State(Scope.Thread)
    public static class SerialState extends SetupState {
        @Param({"ARRAY_LIST", "LINKED_LIST", "VECTOR", "COPY_ON_WRITE_ARRAY_LIST"})
        ListType listType;

        ListType get_list_type() {
            return listType;
        }
    }


    @State(Scope.Thread)
    public static class IndexedState {
        @Param({"10", "20"})//, "30", "40", "50", "60", "70", "80", "90", "100"})
        int progress;
        int index;
        int elem;

        @Setup(Level.Trial)
        public void setup(SerialState state) {
            index = (state.size / 100) * progress;
            elem = state.size + progress;
        }
    }

    @State(Scope.Thread)
    public static class AddAllState {
        List<Integer> list;

        @Setup(Level.Trial)
        public void setup() {
            list = new java.util.ArrayList<>(1000);
            for (int i = 0; i < 1000; i++) {
                list.add(i);
            }
        }
    }

    @Setup(Level.Trial)
    public void list_setup(SerialState state) {
        super.list_setup(state);
    }

    @Setup(Level.Iteration)
    public void elems_setup(SerialState state) {
        super.elems_setup(state);
    }
        

    //@Benchmark
    public void add_at_index(IndexedState state) {
        list.add(state.index, state.elem);
    }

    //@Benchmark
    public void add_all_start(AddAllState state) {
        list.addAll(0, state.list);
    }

    //@Benchmark
    public void add_all_end(AddAllState state) {
        // 1000x opakované přidání 1000 prvků na konec kolekce
        list.addAll(state.list);
    }

    //@Benchmark
    public void get_from_index(IndexedState state) {
        list.get(state.index);
    }

    //@Benchmark
    public void clear() {
        list.clear();
    }

    //@Benchmark
    public void sort() {
        list.sort(null);
    }

    //@Benchmark
    public void to_array(Blackhole bh) {
        bh.consume(list.toArray());
    }

    //@Benchmark
    public void list_iterator(IndexedState state, Blackhole bh) {
        java.util.ListIterator<Integer> it = list.listIterator(state.index);
        bh.consume(it);
    }

}
