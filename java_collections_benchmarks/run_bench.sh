mvn clean install
java -jar target/benchmarks.jar -rf json | tee results.txt