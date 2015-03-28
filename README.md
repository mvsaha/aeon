# eon
***Line segments (or rays, or lines) on the arrow of time***


### Introduction
This module defines the ```DateRange``` class, which wraps two dates to represent a duration of time. ```DateRanges``` can be constructed with two ```dates```:

```python
>>> from datetime import date,datetime
>>> import eon
>>> eon.DateRange( date(1999,1,1), date(2009,3,6) )
DateRange(1999-01-01 to 2009-03-06)
```
```datetimes``` can also be used:
```python
>>> dr = eon.DateRange( datetime(1997,8,4), datetime(1997,8,29,2,14) )
>>> dr
DateRange(1997-08-04 00:00:00 to 1997-08-29 02:14:00)
```

We can check if a ```date``` is inside this ```DateRange```:
```python
>>> datetime(2006,1,2,3,4,5) in eon.DateRange(datetime(2006,1,1),datetime(2008,1,1))
True
>>> datetime(2012,1,1) in dr
False
```

Bounds are _always_ _inclusive_:
```python
>>> dr = eon.DateRange(datetime(2006,1,1),datetime(2008,1,1))
>>> datetime(2006,1,1) in dr
True
>>> datetime(2008,1,1) in dr
True
```

Infinite times can be represented by constructing with ```None```:
```python
>>> dr = eon.DateRange( datetime(2006,1,1), None )
>>> dr
DateRange(Beginning on 2006-01-01 00:00:00)
>>> datetime(2312,1,1) in dr
True
```

Call ```span()``` to retrieve the length of time spanned by the two dates in the form of a ```timedelta```:
```python
>>> print( dr.span() )
3287 days, 0:00:00.000001
>>> print( dr.end(None).span()) # dr.end
```

Individual bounds can be queried or changed with the ```start()``` and ```end()``` getter/setter methods. Calling this with no arguments retrieves the current bounds:
```python
>>> dr
DateRange(Beginning on 2006-01-01 00:00:00)
>>> dr.start() # Get the chronologically earliest bound.
datetime.datetime(2006, 1, 1, 0, 0)
>>> dr.end() # Get the last bound (None)
>>> dr.end(datetime(2012,1,1)) # Set the chronologically latest bound.
DateRange(2006-01-01 00:00:00 to 2014-01-01 00:00:00)
>>> dr
DateRange(2006-01-01 00:00:00 to 2012-01-01 00:00:00)
```

Both ```start()``` and ```end()``` return ```self```, so logic can be chained:
```python
dr.end(datetime(2022,5,12)).span() # Modify the bound, then get the updated span
```


