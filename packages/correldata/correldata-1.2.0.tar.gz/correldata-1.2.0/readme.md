# correldata

[![PyPI Version](https://img.shields.io/pypi/v/correldata.svg)](https://pypi.python.org/pypi/correldata)

Read/write vectors of correlated data from/to a csv file.

These data are stored in a dictionary, whose values are numpy arrays
with elements which may be strings, floats, or floats with associated uncertainties
as defined in the [uncertainties](https://pypi.org/project/uncertainties) library.

When reading data from a csv file, column names are interpreted in the following way:

* In most cases, each columns is converted to a dict value, with the corresponding
dict key being the column's label.
* Columns whose label starts with `SE` are interpreted as specifying the standard
error for the latest preceding data column.
* Columns whose label starts with `correl` are interpreted as specifying the
correlation matrix for the latest preceding data column. In that case, column labels
are ignored for the rest of the columns belonging to this matrix.
* Columns whose label starts with `covar` are interpreted as specifying the
covariance matrix for the latest preceding data column. In that case, column labels
are ignored for the rest of the columns belonging to this matrix.
* `SE`, `correl`, and `covar` may be specified for any arbitrary variable other than
the latest preceding data column, by adding an underscore followed by the variable's
label (ex: `SE_foo`, `correl_bar`, `covar_baz`).
* `correl`, and `covar` may also be specified for any pair of variable, by adding an
underscore followed by the two variable labels, joined by a second underscore
(ex: `correl_foo_bar`, `covar_X_Y`). The elements of the first and second variables
correspond, respectively, to the lines and columns of this matrix.
* Exceptions will be raised, for any given variable:
	- when specifying both `covar` and any combination of (`SE`, `correl`)
	- when specifying `correl` without `SE`

## Example

```py
import correldata

data  = '''
Sample, Tacid,  D47,   SE,        correl,,,  D48,           covar,,, correl_D47_D48
   FOO,   90., .245, .005,     1, 0.5, 0.5, .145,  4e-4, 1e-4, 1e-4,  0.5, 0.0, 0.0
   BAR,   90., .246, .005,   0.5,   1, 0.5, .146,  1e-4, 4e-4, 1e-4,  0.0, 0.5, 0.0
   BAZ,   90., .247, .005,   0.5, 0.5,   1, .147,  1e-4, 1e-4, 4e-4,  0.0, 0.0, 0.5
'''[1:-1]

print(correldata.read_data(data))

# yields:
# 
# {
#     'Sample': array(['FOO', 'BAR', 'BAZ'], dtype='<U3'),
#     'Tacid': array([90., 90., 90.]),
#     'D47': _correl_array([0.245+/-0.004999999999999998, 0.246+/-0.004999999999999997, 0.247+/-0.005], dtype=object),
#     'D48': _correl_array([0.145+/-0.019999999999999993, 0.146+/-0.019999999999999993, 0.147+/-0.019999999999999997], dtype=object),
# }
```

## Documentation / API

[https://mdaeron.github.io/correldata](https://mdaeron.github.io/correldata)