# TPQBogo

A specification and implementation of _Threaded Pseudo-Quantum Bogosort_.

## Table of Contents

<!-- TOC -->

- [TPQBogo](#tpqbogo)
  - [Table of Contents](#table-of-contents)
  - [Preamble](#preamble)
  - [Usage](#usage)
  - [Sample Output](#sample-output)
    - [Main Report](#main-report)
    - [Speedtest Report](#speedtest-report)
    - [Nanoseconds Report](#nanoseconds-report)
  - [Epilogue](#epilogue)

<!-- /TOC -->

## Preamble

As we all know, [Bogosort](https://en.wikipedia.org/wiki/Bogosort) is by far
the most superior sorting algorithm out there – with potentials of reaching up
to $O(1)$ time complexity, and with enough optimisations, a _guaranteed_ $O(1)$
space complexity.

However, top archaeologists and bronchologists alike have done the impossible;
they improved on perfection, with **quantum bogosort** (QuantBogo). The way it
works is similar to bogosort, but with a minor adaptation to guarantee a time
complexity of $O(1)$:

```py
def quantum_bogosort(arr):
    shuffle(arr)
    if not is_sorted(arr):
        universe.rmdir("/")
```

By taking advantage of the
[Axiom of Many-worlds](https://en.wikipedia.org/wiki/Many-worlds_interpretation),
the algorithm either always produces a sorted array instantly, or else it didn't
happen.

Unfortunately, due to the effects of climate change, affordable and scalable
quantum computing will forever remain unattainable
(they [need cold environments](https://en.wikipedia.org/wiki/Quantum_computing#Decoherence),
doncha know?), joining the realms of proper cache invalidation and usable
frontend web frameworks.

However, I have devised a proof-of-concept that simulates a form of quantum
mechanics to achieve a shadow of true powers of QuantBogo, one that still
outperforms even the finest JavaScript interpreters. I call it the _Threaded_
_Pseudo-Quantum Bogosort_, or **TPQBogo** for short.

Powered by
[an obscure and underutilised programming technique](<https://en.wikipedia.org/wiki/Thread_(computing)>),
this algorithm achieves similar results with a space complexity of $O(n)$ and
a time complexity of $O(n!)$ – and when a variable is shouting at you, you know
it's gonna be groundbreaking!

## Usage

> [!IMPORTANT]
> The script requires has been tested on Python 3.12.7. It may work with
> earlier versions, but here be dragons.

An implementation of TPQBogo is available in the included `tpqbogo.py`. It's
got it all: type hints, generators for memory efficiency, full docstrings,
the whole nine yards.

```
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
```

## Sample Output

### Main Report

Here's TPQBogo at work, on a shuffled array of 8 numbers:

**Input:**

```sh
$ python tpqbogo.py 8
```

**Output:**

```
*** Threaded Pseudo-Quantum Bogosort ***
Your sorted array is:
  [1, 2, 3, 4, 5, 6, 7, 8]
Statistics:
  Original array:            [5, 8, 3, 7, 2, 1, 6, 4]
  Number of permutations:    40320
  Successful thread:         t28421
  Time elapsed:              5175589717 ns
```

### Speedtest Report

If you want to see the _real_ power of this algorithm, use the `--speedtest`
flag to see the true glory of $O(n!)$ with your very eyes!

**Input:**

```sh
$ python tpqbogo.py --speedtest 8
```

**Output:**

```csv
array_size,permutations,speed_nanoseconds
1,1,383714
2,2,434690
3,6,787936
4,24,2283009
5,120,12789870
6,720,78388894
7,5040,594754454
8,40320,4809490419
```

The output will be presented in CSV format, perfect for pasting into your
favourite datavis tools.

**Input:**

```sh
$ python tpqbogo.py --speedtest 8 | tabby -e dim
```

**Output:**

```
array_size  permutations  speed_nanoseconds
1           1             367765
2           2             303675
3           6             803805
4           24            3240010
5           120           13727008
6           720           68485239
7           5040          475634019
8           40320         4206413826
```

**Wait, what's a `tabby`?**

It's a Python app I also wrote, and it's
[actually somewhat practical](https://github.com/jahinzee/tabbycat).

### Nanoseconds Report

Actually, why do we need all this extra stuff like "permutations"? Talk is
fluff – numbers in isolation speak a thousand words.

**Input:**

```sh
$ python tpqbogo.py --nanoseconds 8
```

**Output:**

```
4216469864
```

## Epilogue

`</j>`
