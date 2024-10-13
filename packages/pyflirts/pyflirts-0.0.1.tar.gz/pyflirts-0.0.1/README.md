<h1 align="center"><b>Py-Flirts</b></h1>

<p align="center"><img src="" alt="Pyflirts"></p>

<h2 align="center">one line flirt lines for programmers ( flirt lines as a service )</h3>

<h3 align="center">
    Packed with the latest flirt lines, in diff langs etc. </br>
</h3>

---

![GitHub forks](https://img.shields.io/github/forks/Pyflirts/pyflirts?style=social)
![GitHub Repo stars](https://img.shields.io/github/stars/pyflirts/pyflirts?style=social)

![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-white?&style=social&logo=hugo)
![GitHub license](https://img.shields.io/github/license/pyflirts/pyflirts?&style=social&logo=github)

![Python](https://img.shields.io/badge/Python-v3.10-white?style=social&logo=python)
[![Documentation](https://img.shields.io/badge/Documentations-docs.Pyflirts.tech-white?&style=social&logo=gitbook)]()

[![Telegram Group](https://img.shields.io/badge/Telegram-Group-white?&style=social&logo=telegram)](https://telegram.dog/pyflirtschat)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-white?&style=social&logo=telegram)](https://telegram.dog/pyflirts)

---

## Installation

Install the `pyflirts` module with pip:

```bash
pip3 install pyflirts
```

## Usage

### Python

You can also access the flirt lines in your own project by importing `pyflirts` and using the function
`get_flirt`:

```pycon
>>> import pyflirts
>>> print(pyflirts.get_flirt())
Do you believe in love at first sight, or should I walk by again?
```

We support many languages, and have multiple flirt lines categories like:

```pycon
>>> import pyflirts
>>> print(pyflirts.get_flirt("es"))  # spanish flirt lines
¿Crees en el amor a primera vista, o debo pasar otra vez?
>>> print(pyflirts.get_flirt("es", "crazy"))  # spanish crazy flirt lines
Si fueras una bebida, serías el cóctel perfecto: irresistible y siempre refrescante.
```

There is also a `get_flirts` function which returns all the flirts line in the given language and category like:

```python
import pyflirts

for flirt in pyflirts.get_flirts():
    print(flirt)
```

Alternatively, use the `pyflirts.forever` generator function like:

```python
import pyflirts

for flirt in pyflirts.forever():
    print(flirt)
```

## Maintainers

The project is maintained by the members of the Pyflirts Community:

- Shiva Mishra

## Contributing

- The code is licensed under the [MIT Licence]
- Please use GitHub issues to submit bugs and report issues
- Feel free to contribute to the code
- Feel free to contribute flirt lines (via pull request or [proposal issue](https://github.com/pyflirts/pyflirts/issues/))

## Website and documentation

The pyflirts website and documentation is comming soon....

## credits 
- [Shiva Mishra](https://github.com/shivamishrame)
- [pyjokes](https://github.com/pyjokes/pyjpkes)
