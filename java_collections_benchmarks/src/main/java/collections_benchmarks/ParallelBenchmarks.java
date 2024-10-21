package collections_benchmarks;

import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;
import java.util.Random;

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
        List<Boolean> list;
        ListIterator<Boolean> listIterator;

        @Setup(Level.Trial)
        public void setup(ParallelState state) {
            list = new ArrayList<>(state.size);
            for (int i = 0; i < state.size; i++) {
                list.add(true);
            }
            // change random 10% of the elements to false
            Random rand = new Random();
            for (int i = 0; i < state.size / 10; i++) {
                list.set(rand.nextInt(state.size), false);
            }
            listIterator = list.listIterator();
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
        blackhole.consume(list.parallelStream().filter(e -> filterState.listIterator.next()));
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
