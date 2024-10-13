## impyrialaremou

A package for converting between imperial unit lengths and weights.

This package was created for the [DataCamp](https://www.datacamp.com) course "Developing Python Packages".

### Features

- Convert lengths between miles, yards, feet and inches.
- Convert weights between hundredweight, stone, pounds and ounces.

### Usage

```python
import impyrialaremou

# Convert 500 miles to feet
impyrialaremou.length.convert_unit(500, from_unit='yd', to_unit='ft')  # returns 1500.0

# Convert 100 ounces to pounds
impyrialaremou.weight.convert_unit(100, from_unit='oz', to_unit='lb')  # returns 6.25
```
