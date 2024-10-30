#!/usr/bin/env python3

"""
tpqbogo - An implementation of Threaded Pseudo-Quantum Bogosort.

Read the README.md for more information.

Usage: tpqbogo.py [-h] [-D] [-N] [-S] size

An implementation of Threaded Pseudo-Quantum Bogosort.

positional arguments:
  size               the size of the array to sort. Must be a positive non-
                     zero integer.

options:
  -h, --help         show this help message and exit
  -D, --debug        print debug messages to stderr.
  -N, --nanoseconds  only output the elapsed time in nanoseconds.
  -S, --speedtest    test sort speeds for arrays of lengths 1 to <size>.
                     Outputs results as CSV with headings.

Copyright (c) 2024 by Jahin Z. (jahinzee) <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__author__ = "jahinzee"
__copyright__ = "Copyright 2024, jahinzee"
__license__ = "MPLv2"
__email__ = "jahinzee@outlook.com"


from typing import List, NamedTuple, TypeVar
from sys import stderr
from itertools import permutations
from threading import Thread, Lock
from random import shuffle
from time import perf_counter_ns
from argparse import ArgumentParser, Namespace
from math import factorial


class ThreadResult(NamedTuple):
    """
    Collection of successful thread results.
    """

    thread_id: int
    sorted_array: List[int]


class Result(NamedTuple):
    """
    Collection of main sort algorithm results, includes the successful thread
    results and the overall number of permutations.
    """

    num_of_permutations: int
    successful_thread: ThreadResult


class MainResult(NamedTuple):
    """
    Collection of top-level test run results, including the original array
    and elapsed time.
    """

    original_array: List[int]
    elapsed_time_nanoseconds: int
    result: Result


T = TypeVar("T")


class Locked[T]:
    """
    Helper class.
    Pairs an object with a lock for more convenient thread safety.
    """

    def __init__(self, item: T) -> None:
        """
        Creates a new object-lock pair from an existing object.

        Args:
            item (T): The existing object.
        """
        self.lock = Lock()
        self.item = item

    def __enter__(self) -> T:
        """
        Acquires the lock, and returns the contained object.

        Returns:
            T: The contained object.
        """
        self.lock.acquire()
        return self.item

    def __exit__(self, exc_type, exc_vale, traceback):
        """
        Releases the lock.

        Args:
            exc_type (_type_): _description_
            exc_vale (_type_): _description_
            traceback (_type_): _description_
        """
        self.lock.release()


use_debug = False


def dbg(message: str) -> None:
    """
    Prints a message to stderr, only if the global `use_debug` is True.

    Args:
        message (str): The message to print.
    """
    if use_debug:
        print(message, file=stderr)


def tpqbogo(arr: List[int]) -> Result:
    """
    Sorts an array using Threaded Pseudo-Quantum Bogosort.

    Args:
        arr (List[int]): The array to sort.

    Returns:
        Result: Contains the sorted array (inside a ThreadResult), the
                number of permutations checked, and the thread
                that returned the correct answer.
    """

    def check_sort(
        idx: int, arr: List[int], results: Locked[List[ThreadResult]]
    ) -> None:
        """
        The inner "actual" quantum bogosort implementation.

        Args:
            idx (int): The ID of the currently running thread.
            arr (List[int]): The array to "sort".
            results (Locked[List[ThreadResult]]):
                The array where results will be stored (based on `idx`).
        """
        is_sorted = all(left <= right for left, right in zip(arr, arr[1:]))
        dbg(f"  [t{idx}] {arr=}; {is_sorted=}")
        if not is_sorted:
            # Ordinarily, one would explode the universe here.
            # But I'm pretty sure that'd require sudo priviledges,
            # so a simple return would suffice.
            return
        # This universe has survived. We must let the heavens
        # know about our story.
        with results as r:
            r.append(ThreadResult(thread_id=idx, sorted_array=arr))

    # All permutations of the array -- all possible shuffles.
    # The generation is actually done lazily during thread creation.
    arr_permutations = [list(p) for p in permutations(arr)]
    permutation_count = factorial(len(arr))

    dbg(f"[tq*bs] {permutation_count} permutation(s) will be generated.")

    # Initialise thread-safe results queue and thread pool
    results: Locked[List[ThreadResult]] = Locked([])
    threads: List[Thread] = []

    for idx, perm in enumerate(arr_permutations):
        # dbg(f"[tq*bs] Spawning thread [t{idx}].")
        # Create each thread with:
        #   - the thread ID,
        #   - their chosen permutation, and
        #   - the results queue
        t = Thread(target=check_sort, args=(idx, list(perm), results))
        t.start()
        threads.append(t)
    dbg("[tq*bs] All threads spawned.")

    for t in threads:
        t.join()
    dbg("[tq*bs] All threads resolved.")

    with results as r:
        # There should theoretically be only one item in the results queue,
        # but even if there's multiple we just care about one of them.
        first_to_survive = r[0]
        return Result(
            num_of_permutations=permutation_count, successful_thread=first_to_survive
        )


def main_nanoseconds(array_size: int) -> None:
    """
    Calculates `TPQBogo` for an array of the given size, and prints only the
    time it took in nanoseconds.

    Args:
        array_size (int): The size of the array to run TPQBogo on.
    """
    result = main(array_size)

    # Destructure results.
    _, time_elapsed, _ = result
    print(time_elapsed)


def main_speedtest(array_size: int) -> None:
    """
    Tests the speed it takes for `TPQBogo` to sort increasingly large arrays,
    from size 1 to size `array_size`, and writes output to stdout as CSV data.

    Args:
        array_size (int): The maximum size of array to test.
    """

    # Print CSV headers
    print("array_size,permutations,speed_nanoseconds")
    for i in range(1, array_size + 1):
        dbg(f"[speedtest] Iteration {i}.")
        result = main(i)
        print(
            f"{i},{result.result.num_of_permutations},{result.elapsed_time_nanoseconds}"
        )


def main_display(array_size: int) -> None:
    """
    Calculates `TPQBogo` for an array of the given size, and prints the output
    and relevant statistics to stdout.

    Args:
        array_size (int): The size of the array to run TPQBogo on.
    """
    result = main(array_size)

    # Destructure results.
    original_array, time_elapsed, algo_result = result
    permutations_count, thread = algo_result
    thread_idx, sorted_arr = thread

    # Display output.
    dbg("")  # Debug-only blank line for easier delineation of debug and main output.
    print("*** Threaded Pseudo-Quantum Bogosort ***")

    print(f"Your sorted array is:\n  {sorted_arr}")
    print("Statistics:")
    print(f"  Original array:            {original_array}")
    print(f"  Number of permutations:    {permutations_count}")
    print(f"  Successful thread:         t{thread_idx}")
    print(f"  Time elapsed:              {time_elapsed} ns")


def main(array_size: int) -> MainResult:
    """
    Calculates `TPQBogo` for an array of the given size, and returns the output
    and relevant statistics.

    Args:
        array_size (int): The size of the array to run TPQBogo on.
    """
    # Create an array of elements 1 to `array_size`, and shuffle for good measure.
    arr = list(range(1, array_size + 1))
    shuffle(arr)

    if array_size < 1:
        # Given array size is not positive, or is a zero.
        print("tpqbogo: size must be a positive non-zero integer.", file=stderr)
        exit(1)

    # Run TPQBogo.
    timer_start = perf_counter_ns()
    result = tpqbogo(arr)
    timer_end = perf_counter_ns()

    # Destructure results.
    permutations_count, thread = result
    thread_idx, sorted_arr = thread

    # Calculate elapsed time.
    time_elapsed = timer_end - timer_start

    return MainResult(
        original_array=arr, elapsed_time_nanoseconds=time_elapsed, result=result
    )


def get_args() -> Namespace:
    """
    Parses program arguments from `argv`.

    Returns:
        Namespace: The `argsparse` namespace.
    """
    parser = ArgumentParser(
        prog="tpqbogo",
        description="An implementation of Threaded Pseudo-Quantum Bogosort.",
    )
    parser.add_argument(
        "size",
        type=int,
        help="the size of the array to sort. Must be a positive non-zero integer.",
    )
    parser.add_argument(
        "-D", "--debug", action="store_true", help="print debug messages to stderr."
    )
    parser.add_argument(
        "-N",
        "--nanoseconds",
        action="store_true",
        help="only output the elapsed time in nanoseconds.",
    )
    parser.add_argument(
        "-S",
        "--speedtest",
        action="store_true",
        help="test sort speeds for arrays of lengths 1 to <size>. Outputs results as CSV with headings.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    use_debug = args.debug
    if args.speedtest:
        main_speedtest(args.size)
        exit(0)
    if args.nanoseconds:
        main_nanoseconds(args.size)
        exit(0)
    main_display(args.size)
