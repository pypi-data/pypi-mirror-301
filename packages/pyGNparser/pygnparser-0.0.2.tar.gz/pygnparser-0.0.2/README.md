# pyGNparser

![https://img.shields.io/pypi/v/pygnparser.svg](https://pypi.python.org/pypi/pygnparser) ![https://github.com/gnames/pygnparser/workflows/Python/badge.svg](https://github.com/gnames/pygnparser/actions?query=workflow%3APython)

This is a Python wrapper on the [GNparser](https://parser.globalnames.org/) API. Code follow the spirit/approach of the [pygbif](https://github.com/gbif/pygbif/graphs/contributors) package, and indeed much of the wrapping utility is copied 1:1 from that repo, thanks [@sckott](https://github.com/sckott) and other [contributors](https://github.com/gbif/pygbif/graphs/contributors).

## Installation

Add this line to your application's requirements.txt:

```python
pygnparser
```

And then execute:

    $ pip install -r requirements.txt

Or install it yourself as:

    $ pip install pygnparser

## Usage


Import the library:
```
from pygnparser import gnparser
```

If you have a local installation of gnparser, set the GNPARSER_BASE_URL to the host and port that the service is running on, for example if running locally on port 8787:

```python
GNPARSER_BASE_URL = "http://localhost:8787/"
```

Without the GNPARSER_BASE_URL environment variable set, the wrapper will default to using the remote API which will perform slower: https://parser.globalnames.org/


---
### Parse a scientific name
Parse a scientific name:
```python
>>> result = gnparser('Ursus arctos Linnaeus, 1758') #  => Dictionary
```

Check if parsed:
```python
>>> result.parsed() #  => Boolean
True
```

Get [parsed quality](https://github.com/gnames/gnparser#figuring-out-if-names-are-well-formed):
```python
>>> result.quality() #  => Integer
1
```

Get the genus name:
```python
>>> result.genus() #  => String
'Ursus'
```

Get the species name:
```python
>>> result.species() #  => String
'arctos'
```

Get the year:
```python
>>> result.year() #  => String
'1758'
```

Get the authorship:
```python
>>> result.authorship() #  => String
'(Linnaeus, 1758)'
```

Get the scientific name without the Latin gender stem:
```python
>>> result.canonical_stemmed() #  => String
'Ursus arct'
```

Get the parsed name components for a hybrid formula:
```python
>>> result = gnparser('Isoetes lacustris × stricta Gay') #  => Dictionary
>>> result.is_hybrid() #  => Boolean
True
>>> result.hybrid() #  => String
'HYBRID_FORMULA'
>>> result.normalized() #  => String
'Isoetes lacustris × Isoetes stricta Gay'
>>> result.hybrid_formula_ranks() #  => Array
['species', 'species']
>>> res.hybrid_formula_genera() #  => Array
['Isoetes', 'Isoetes']
>>> res.hybrid_formula_species() #  => Array
['lacustris', 'stricta']
>>> res.hybrid_formula_authorship() #  => Array
['', 'Gay']
```

---
### Parse multiple scientific names
Parse multiple scientific names by separating them with `\r\n`:
```python
results = gnparser('Ursus arctos Linnaeus, 1758\r\nAlces alces (Linnaeus, 1758)\r\nRangifer tarandus (Linnaeus, 1758)\r\nUrsus maritimus (Phipps, 1774') #  => Array
```

Get the genus of the 1st parsed name in the list:
```python
results[0].genus() #  => String
'Ursus'
```

---
## Deviations

Some extra helpers are included that extend the functionality of GNparser.

1) The page() method gets the page number out of the unparsed tail:
```python
>>> result = gnparser('Ursus arctos Linnaeus, 1758: 81')
result.page()  # => String
'81'
```

2) The authorship() method returns a formatted authorship string depending on the number of authors. If it is one author with a year, it will return as Smith, 1970. For two authors and a year it will return as Smith & Johnson, 1970. For three authors it will return as Smith, Johnson & Jones, 1970. Any additional authors beyond 3 will be comma separated with the last author included with an ampersand.
```python
>>> result = gnparser('Aus bus cus Smith, Johnson, & Jones, 1970')
result.authorship()  # => String
'Smith, Johnson & Jones, 1970'
```

3) The infraspecies() method will return the infraspecies name. Currently there is no special methods for ranks lower than trinomials but you can access them with the infraspecies_details() method. Please [open an issue](https://github.com/gnames/pygnparser/issues/new) if you need it added.
```python
>>> result = gnparser('Aus bus cus')
result.infraspecies()  # => String
'cus'
```

---
## Other GNparser Libraries

* Node.js: [node-gnparser](https://github.com/amazingplants/node-gnparser)
* R: [rgnparser](https://github.com/ropensci/rgnparser)
* Ruby Gem: [biodiversity](https://github.com/GlobalNamesArchitecture/biodiversity)

---
## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/gnames/pygnparser. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [code of conduct](https://github.com/gnames/pygnparser/blob/main/CODE_OF_CONDUCT.md).

---
## Development

After checking out the repo, change into the package directory `cd pygnparser`, run `pip install .` to install the package, and `pip install -r requirements.txt` to install the dependencies. Then, run `pytest` to run the tests. You can also run `bin/console` for an interactive Python prompt that will allow you to experiment with the above example commands.

---
## License

The package is available as open source under the terms of the [MIT](https://github.com/gnames/pygnparser/blob/main/LICENSE.txt) license. You can learn more about the MIT license on [Wikipedia](https://en.wikipedia.org/wiki/MIT_License) and compare it with other open source licenses at the [Open Source Initiative](https://opensource.org/license/mit/).

---
## Code of Conduct

Everyone interacting in the pyGNparser project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/gnames/pygnparser/blob/main/CODE_OF_CONDUCT.md).
