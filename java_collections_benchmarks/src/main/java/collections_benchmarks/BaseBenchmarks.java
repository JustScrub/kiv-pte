package collections_benchmarks;

import java.util.List;

import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Param;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.Warmup;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;

@State(Scope.Benchmark)
@BenchmarkMode(Mode.AverageTime)
@Fork(value = 1, warmups = 0)
@Warmup(iterations = 0)
@Measurement(iterations = 10, time = 1000, timeUnit = java.util.concurrent.TimeUnit.MILLISECONDS)
@OutputTimeUnit(java.util.concurrent.TimeUnit.MILLISECONDS)
public class BaseBenchmarks {

    List<Integer> list;
    
    @State(Scope.Thread)
    public abstract static class SetupState {
        public enum ListType {
            ARRAY_LIST, LINKED_LIST, VECTOR, COPY_ON_WRITE_ARRAY_LIST
        }
        @Param({"200", "800"})//, "1200", "2000", "8000"})
        int size;

        abstract ListType get_list_type();
    }

    public void list_setup(SetupState state) {
        switch (state.get_list_type()) {
            case ARRAY_LIST:
                list = new java.util.ArrayList<>(state.size);
                break;
            case LINKED_LIST:
                list = new java.util.LinkedList<>();
                break;
            case VECTOR:
                list = new java.util.Vector<>(state.size);
                break;
            case COPY_ON_WRITE_ARRAY_LIST:
                list = new java.util.concurrent.CopyOnWriteArrayList<>();
                break;
        }
        System.gc();
    }

    public void elems_setup(SetupState state) {
        list.clear();
        for (int i = 0; i < state.size; i++) {
            list.add(i);
        }
        System.gc();
    }
}
