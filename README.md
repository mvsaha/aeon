***This was a learning project. You should not use this library!***

# eon
***Line segments (or rays, or lines) on the arrow of time***

Written in pure python. Depends only on the built-in _datetime_ package.

### Installing ***eon*** 
On the command line (must have pip installed)
```
pip install https://github.com/mvsaha/eon/zipball/master
```

Now we can import it in python
```python
>>>import eon
```

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

```slide()``` will create a new DateRange with both bounds shifted by an input ```timedelta```:
```python
>>>dr3 = dr.slide(timedelta(days=20,hours=10,microseconds=33))
DateRange(1000-01-21 10:00:00:000033 to 2000-01-21 10:00:00.000033 )
```

### Cycles
Periodic timestamps can be retrieved from a ```DateRange``` by calling generators.

Generic cycles are defined using only a ```timedelta```: 
```python
>>> DateRange( datetime(2012,1,1), datetime(2012,2,1) ).cycles(timedelta(days=11))
<generator object days at 0x000XXXX>
>>> [d for dr in DateRange( datetime(2012,1,1),
                            datetime(2012,2,1) ).cycles(timedelta(days=11))]
[datetime.datetime(2012, 1, 1, 0, 0),
datetime.datetime(2012, 1, 12, 0, 0),
datetime.datetime(2012, 1, 23, 0, 0)]
```

If the ```timedelta``` is negative then we start at ```end``` instead of ```start```.
```python
>>> [d for dr in DateRange( datetime(2012,1,1),
                            datetime(2012,2,1) ).cycles(timedelta(days=-11))]
[datetime.datetime(2012, 2, 1, 0, 0),
datetime.datetime(2012, 1, 21, 0, 0),
datetime.datetime(2012, 1, 10, 0, 0)]
```

Other common time periods are specially defined:
Days:
```python
>>> 
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
[datetime(2012,1,1)]
```

Generate them in reverse chronological order using the ```reverse=True``` named argument:
```python
>>> for d in DateRange( datetime(2012,1,1), datetime(2012,2,1) ).days(reverse=True):
...    print(d)
datetime(2012,2,1)
datetime(2012,1,31)
...
datetime(2012,1,2)
datetime(2012,1,1)
```

However, we often won't have nice, clean bounds on our ```DateRange```:
```python
>>> dr = DateRange( datetime(2012,1,3,hour=2,minute=1,second=4),
                    datetime(2012,1,7,hour=19))
>>> dr
DateRange(2012-01-03 02:01:04 to 2012-01-07 19:00:00)
```

If we cycle through the ```days()```, we get timestamps of consecutive days, starting on ```start```:
```python
>>> [d for d in dr.days()]
[datetime.datetime(2012, 1, 3, 2, 1, 4),
datetime.datetime(2012, 1, 4, 2, 1, 4),
datetime.datetime(2012, 1, 5, 2, 1, 4),
datetime.datetime(2012, 1, 6, 2, 1, 4),
datetime.datetime(2012, 1, 7, 2, 1, 4)]
```

If we use ```reverse=True``` we get timestamps going in reverse chronological order, starting with ```end```.
```python
>>>[d for d in dr.days(reverse=True)]
[datetime.datetime(2012,1,7,19),
datetime.datetime(2012,1,6,19)
datetime.datetime(2012,1,5,19)
datetime.datetime(2012,1,4,19)
datetime.datetime(2012,1,3,19)]
```

The dates generated by cycles are constructed as you call ```next()``` on them, so you only pay for datetimes that you use. This also allows you to generate dates from an unbounded ```DateRange```, i.e. representative of and infinite period of time. To do this call the cycle generator with an ```n``` argument.
```python
>>>dr = DateRange(datetime(2012,1,1),None)
>>>dr
DateRange(Beginning on 2012-01-01 00:00:00)
>>>l = [d for d in dr.years(n=100)]) # Get the first 100 years of dr
>>>len(l)
100
```

However, if we try to call this ```reverse=True```, we get an Exception!
```
>>>[d for d in dr.years(n=100)]
...
ValueError: Cannot start at infinity.
```
It is impossible to start iterating from the unbounded ```end``` of a DateRange().

### Range Cycles
We can also generate  periodic ```DateRanges``` corresponding by prepending ```r``` to cycle generators. Range generators are guaranteed to sample time fully and uniquely. In other words, any given ```date```(```time```) in a ```DateRange``` will fall into exactly one range cycle.
####TO BE FILLED IN...
