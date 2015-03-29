# eon
***Line segments (or rays, or lines) on the arrow of time***


### Introduction
This module defines the ```DateRange``` class, which wraps two dates to represent a duration of time. ```DateRanges``` can be constructed with two ```dates```:

```python
>>> from datetime import date,datetime,timedelta
>>> import eon
>>> eon.DateRange( date(1999,1,1), date(2009,3,6) )
DateRange(1999-01-01 to 2009-03-06)
```
Or two ```datetimes```:
```python
>>> dr = eon.DateRange( datetime(1997,8,4), datetime(1997,8,29,2,14) )
>>> dr
DateRange(1997-08-04 00:00:00 to 1997-08-29 02:14:00)
```

Or a ```datetime``` and a ```timedelta```:
```python
>>> DateRange( datetime(2010,1,1), timedelta(days=-12) )
DateRange(2009-12-20 00:00:00 to 2010-01-01 00:00:00)
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
>>> dr = eon.DateRange(datetime(2006,5,4,3,2,1),datetime(2008,1,1))
>>> datetime(2006,5,4,3,2,1) in dr
True
>>> datetime(2006,5,4,3,2) in dr
False
```

Infinite times can be represented by constructing with ```None```:
```python
>>> dr = eon.DateRange( datetime(2006,1,1), None )
>>> dr
DateRange(Beginning on 2006-01-01 00:00:00)
>>> datetime(2312,1,1) in dr
True
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
```

Call ```span()``` to retrieve the length of time spanned by the two dates in the form of a ```timedelta```:
```python
>>> dr = eon.DateRange(datetime(1945,3,9),datetime(2102,1,3))
>>> print( dr.span() )
57278 days, 0:00:00.000001
>>> dr.end(None)
DateRange(Beginning on 1945-03-09 00:00:00)
>>> print( dr.span() ) # Infinite spans return None
None
```

Both ```start()``` and ```end()``` return ```self```, so logic can be chained:
```python
>>> dr.end(datetime(2022,5,12)).span() # Modify the bound, then get the updated span
datetime.timedelta(28188, 0, 1)
```

```startat()``` and ```endat()``` will create new DateRanges with modified bounds, leaving the original unchanged.
```python
>>> dr = eon.DateRange(datetime(1000,1,1),datetime(2000,1,1))
>>> dr2 = dr.endat(datetime(3000,1,1))
>>> dr2
DateRange(1000-01-01 00:00:00 to 3000-01-01 00:00:00)
>>> dr # Unmodified
DateRange(1000-01-01 00:00:00 to 2000-01-01 00:00:00)
```

### Cycles
Periodic timestamps can be retrieved from a ```DateRange``` by calling a generator for common durations:

Days:
```python
>>> DateRange( datetime(2012,1,1), datetime(2012,2,1) ).days()
<generator object days at 0x000XXXX>
>>> for d in DateRange( datetime(2012,1,1), datetime(2012,2,1) ).days():
...    print(d)
datetime(2012,1,1)
datetime(2012,1,2)
...
datetime(2012,1,31)
datetime(2012,2,1)
```

Months:
```python
>>> [d for d in DateRange( datetime(2012,1,1), datetime(2012,2,1) ).months()]
[datetime(2012,1,1),datetime(2012,2,1)]
```
Years:
```python
>>> [d for d in DateRange( datetime(2012,1,1), datetime(2012,2,1) ).months()]
[datetime(2012,1,1),datetime(2012,2,1)]
```

Generate them in reverse chronological order using the ```reverse=True``` named argument:
```python
>>> for d in DateRange( datetime(2012,1,1), datetime(2012,2,1) ).days():
...    print(d)
datetime(2012,2,1)
datetime(2012,1,31)
...
datetime(2012,1,2)
datetime(2012,1,1)
```

However, we often won't have nice, clean bounds on our ```DateRange```. _Ex_:
```python
>>> dr = DateRange( datetime(2012,1,3,hour=2,minute=1,second=4),
                    datetime(2012,4,7,hour=19))
>>> dr
DateRange(2012-01-03 02:01:04 to 2012-04-07 19:00:00)
```

In this case of a generic cycle, _C_<sub>{1...2}</sub>, we use the following algorithm to generate ```date```(```time```)s:
    (1) Find the cycle _C_<sub>i</sub> that contains ```start()``` (or ```end()``` if ```reverse=True```)
