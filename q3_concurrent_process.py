import threading
import time

NUMBERS = [35, 38, 40]    # one thread for each value
ROUNDS = 10


def fibonacci(n):
    """Iterative nth Fibonacci number. The loop runs n - 1 times -> O(n)."""
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


# ---------- WITH multithreading ----------
def run_with_multithreading():
    results = {}          # shared by all threads: n -> Fibonacci value
    start_times = []      # shared: start time of each thread
    finish_times = []     # shared: finish time of each thread
    result_lock = threading.Lock()   # only one thread may change shared data at a time

    def worker(n):
        worker_start = time.perf_counter_ns()
        value = fibonacci(n)
        worker_finish = time.perf_counter_ns()
        with result_lock:             # protect the shared data while we change it
            results[n] = value
            start_times.append(worker_start)
            finish_times.append(worker_finish)

    threads = []
    for n in NUMBERS:
        threads.append(threading.Thread(target=worker, args=(n,)))

    for t in threads:       # start all 3 threads
        t.start()
    for t in threads:       # wait until all 3 have finished
        t.join()

    # T = (finish time of the thread that finished last)
    #   - (start time of the thread that started first)
    elapsed = max(finish_times) - min(start_times)
    return results, elapsed


# ---------- WITHOUT multithreading ----------
def run_without_multithreading():
    start = time.perf_counter_ns()
    results = {}
    for n in NUMBERS:                 # one after another
        results[n] = fibonacci(n)
    end = time.perf_counter_ns()
    return results, end - start


# ---------- run rounds and print ----------
def run_experiment(title, runner):
    print(f"\n=== {title} ===")
    total = 0
    for round_number in range(1, ROUNDS + 1):
        results, elapsed = runner()
        total += elapsed
        print(f"Round {round_number:2d}: Fib(35)={results[35]}, "
              f"Fib(38)={results[38]}, Fib(40)={results[40]} | T = {elapsed:,} ns")
    average = total / ROUNDS
    print(f"Average T ({title}): {average:,.2f} ns")
    return average


def main():
    avg_threads = run_experiment("WITH MULTITHREADING", run_with_multithreading)
    avg_plain = run_experiment("WITHOUT MULTITHREADING", run_without_multithreading)

    print("\n=== SUMMARY ===")
    print(f"Average with multithreading   : {avg_threads:,.2f} ns")
    print(f"Average without multithreading: {avg_plain:,.2f} ns")

    change = (avg_plain - avg_threads) / avg_plain * 100
    if change > 0:
        print(f"Multithreading was {change:.2f}% faster on average.")
    else:
        print(f"Multithreading was {-change:.2f}% slower on average.")


if __name__ == "__main__":
    main()