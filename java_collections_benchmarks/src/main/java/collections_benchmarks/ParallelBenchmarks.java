package collections_benchmarks;

import java.util.HashSet;

import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.Level;
import org.openjdk.jmh.annotations.Param;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.Setup;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.infra.Blackhole;

public class ParallelBenchmarks extends BaseBenchmarks {

    @State(Scope.Thread)
    public static class ParallelState extends SetupState {
        @Param({"ARRAY_LIST", "LINKED_LIST"})
        ListType listType;

        ListType get_list_type() {
            return listType;
        }
    }

    @State(Scope.Thread)
    public static class FilterState {
        HashSet<Integer> set;

        @Setup(Level.Trial)
        public void setup(ParallelState state) {
            set = new HashSet<>();
            for (int i = 0; i < state.size; i+= state.size / 10) {
                set.add(i);
            }
        }
    }

    @Setup(Level.Trial)
    public void list_setup(ParallelState state) {
        super.list_setup(state);
    }

    @Setup(Level.Iteration)
    public void elems_setup(ParallelState state) {
        super.elems_setup(state);
    }

    @Benchmark
    public void parallel_filter(FilterState filterState, Blackhole blackhole) {
        blackhole.consume(list.parallelStream().filter(filterState.set::contains));
    }

    @Benchmark
    public void parallel_count(Blackhole blackhole) {
        blackhole.consume(list.parallelStream().count());
    }

    @Benchmark
    public void parallel_sort(Blackhole blackhole) {
        blackhole.consume(list.parallelStream().sorted());
    }


}
