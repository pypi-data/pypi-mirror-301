# expressive

A library for quickly applying symbolic expressions to NumPy arrays

By enabling callers to front-load sample data, developers can move the runtime cost of Numba's JIT to the application's initial loading (or an earlier build) and also avoid `exec` during runtime, which is otherwise needed when lambdifying symbolic expressions

Inspired in part by this Stack Overflow Question [Using numba.autojit on a lambdify'd sympy expression](https://stackoverflow.com/questions/22793601/using-numba-autojit-on-a-lambdifyd-sympy-expression)

## installation

via pip https://pypi.org/project/expressive/

```shell
pip install expressive
```

## usage

refer to tests for examples for now

generally follow a workflow like
* create instance `expr = Expressive("a + log(b)")`
* build instance `expr.build(sample_data)`
* instance is now callable `expr(full_data)`

The `data` should be provided as dict of NumPy arrays

```python
sample_data = {  # types are used to compile a fast version for full data
    "a": numpy.array([1,2,3,4], dtype="int64"),
    "b": numpy.array([4,3,2,1], dtype="int64"),
}
full_data = {
    "a": numpy.array(range(1_000_000), dtype="int64"),
    "b": numpy.array(range(1_000_000), dtype="int64"),
}
```

## testing

Only `docker` and `docker compose` (v2) are require, which are used to host/generate the test environment

Then just directly run the test script from the root of the repository, it will build the docker test environment and run itself inside it automatically

```shell
sudo apt install docker.io docker-compose-v2
./test/runtests.sh
```

## contributing

The development process is currently private (though most fruits are available here!), largely due to this being my first public project with the potential for other users than myself, and so the potential for more public gaffes is far greater

Please refer to [CONTRIBUTING.md](https://gitlab.com/expressive-py/expressive/-/blob/main/CONTRIBUTING.md) and [LICENSE.txt](https://gitlab.com/expressive-py/expressive/-/blob/main/LICENSE.txt) and feel free to provide feedback, bug reports, etc. via [Issues](https://gitlab.com/expressive-py/expressive/-/issues), subject to the former

#### additional future intentions for contributing

* improve internal development history as time, popularity, and practicality allows
* move to parallel/multi-version/grid CI over all-in-1, single-version dev+test container
* greatly relax dependency version requirements to improve compatibility

## version history

##### v1.4.2
* greatly improved verify
  * `numpy.allclose()` takes exactly 2 arrays to compare (further args are passed to `rtol`, `atol`)
  * SymPy namespace special values `oo`, `zoo`, `nan` are coerced to NumPy equivalents (`inf`, `-inf`, `nan`)
  * raise when result is `False`
  * groundwork to maintain an internal collection of results
* internal symbols collection maintains `IndexedBase` instances (`e.atoms(Symbol)` returns `Symbol` instances)
* improve Exceptions from data that can't be used
* new custom warning helper for testing as `assertWarnsRegex` annoyingly eats every warning it can

##### v1.4.1
* more sensibly fill the result array for non-floats when not provided (only float supports NaN)

##### v1.4.0
* add build-time verify step to help identify math and typing issues
* some improved logic flow and improved `warn()`

##### v1.3.2 (unreleased)
* improved publishing workflow
* improved README

##### v1.3.1
* fix bad math related to indexing range
* add an integration test

##### v1.3.0
* add support for parsing equality to result
* add support for (optionally) passing result array
* hugely improve docstrings

##### v1.2.1
* add more detail to [contributing block](#contributing)
* switch array dimensions checking from `.shape` to `.ndim`
* switch tests from `numpy.array(range())` to `numpy.arange()`

##### v1.2.0
* enable autobuilding (skip explicit `.build()` call)
* basic display support for `Expressive` instances

##### v1.1.1
* add version history block

##### v1.1.0
* fixed bug: signature ordering could be unaligned with symbols, resulting in bad types
* added support for non-vector data arguments

##### v1.0.0

* completely new code tree under Apache 2 license
* basic support for indexed offsets

##### v0.2.0 (unreleased)

##### v0.1.0

* very early version with support for python 3.5
