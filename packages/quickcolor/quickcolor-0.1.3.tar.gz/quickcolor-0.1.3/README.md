# QuickColor

**QuickColor** is a Python library providing tags for color formatting sections of printable content. The tags can be flexibly used as part of any string as they simply resolve to the ASCII color codes interpreted by your terminal or terminal emulator.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **quickcolor**.

```bash
pip install quickcolor
```


## Library Usage For Color Application
```python
from quickcolor.color_def import color

# colorize printable content
print(f"{color.CGREEN2}This text is bold green{color.CEND}")
```
```python
from quickcolor.color_def import colors

# alternate method to colorize printable content
print(f"Formatting this phrase part to {colors.fg.yellow}display yellow{colors.off}")
```


## Library Usage For Color Stripping
```python
from quickcolor.color_filter import strip_ansi_esc_sequences_from_string

testString = f'{color.CYELLOW2}Yellow String!{color.CEND}'
print(testString)
print(f'No longer a {strip_ansi_esc_sequences_from_string(testString)}')
```
```python
from quickcolor.color_filter import strip_ansi_esc_sequences_from_input

testString = f'{color.CBLUE2}Blue String!{color.CEND}'
testBytes = testString.encode(encoding="utf-8")
print(testString)
print(testBytes)
print(f'No longer a {strip_ansi_esc_sequences_from_input(stringOrBytes = testBytes)}')
```


## CLI Utility

The following CLI is included with this package for visualizing available color fields and code combinations.

```bash
# qc -h
usage: qc [-h] {shell.colors,color.fields,strip.color.string,strip.color.input} ...

-.-.-. Color attributes for python scripts

positional arguments:
  {shell.colors,color.fields,strip.color.string,strip.color.input}
    shell.colors        display a color chart for current shell
    color.fields        display class color fields
    strip.color.string  strip color codes from a string
    strip.color.input   strip color codes from a byte input

options:
  -h, --help            show this help message and exit

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements
Inspiration for the color names came from [this StackOverflow reply](https://stackoverflow.com/a/39452138).
The color grid method inspiration came from [this StackOverflow reply](https://stackoverflow.com/a/21786287).
The regex content for the strip methods are also floting around StackOverflow.
