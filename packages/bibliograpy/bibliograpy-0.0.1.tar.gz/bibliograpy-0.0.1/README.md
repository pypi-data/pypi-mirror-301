# Bibliograpy

Bibliography management to decorate source code.

[![example workflow](https://github.com/SamuelAndresPascal/cosmoloj-py/actions/workflows/bibliograpy.yml/badge.svg)](https://github.com/SamuelAndresPascal/cosmoloj-py/actions)

[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/version.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_relative_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/platforms.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/license.svg)](https://anaconda.org/cosmoloj/bibliograpy)

[![PyPI repository Badge](https://badge.fury.io/py/bibliograpy.svg)](https://badge.fury.io/py/bibliograpy)


* [Documentation](#documentation)


## Documentation

### API

The Bibliograpy API allows to manage bibliographic centralized references using decorators.

Hence, is it possible to factorize all bibliographic sources as variables in a single module, using them as arguments of
decorators.

```py
"""The bibliography module."""

from bibliograpy.api import TechReport

IAU_2006_B1 = TechReport(
    key="iau_2006_b1",
    title="Adoption of the P03 Precession Theory and Definition of the Ecliptic")
```

```py
"""The bibliography_client module using the bibliography.py module."""

from bibliograpy.api import reference

from bibliography import IAU_2006_B1

@reference(IAU_2006_B1)
def my_function():
    """My my_function documentation."""
    # some implementation here using the reference given as a parameter to the decorator

```

The usage of the decorator has two purposes.

First, to use a bibliographic reference defined once and for all, centralized and reusable.

Second, to implicitly add to the documentation of the decorated entity a bibliographical section.

```py
import bibliography_client

>>> help(my_function)
Help on function my_function in module bibliography_client

my_function()
    My my_function documentation.

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
```

### Preprocessing

[Latest release](https://cosmoloj.com/mkdocs/bibliograpy/latest/)

[Trunk](https://cosmoloj.com/mkdocs/bibliograpy/master/)