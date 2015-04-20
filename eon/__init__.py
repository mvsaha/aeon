# eon
# A python module for working with dates and date ranges
import sys
sys.dont_write_bytecode = True

__author__ = "Michael Vijay Saha"

import datetime

class DateList:

    def __init__(self,dates):
        if isinstance(dates,datetime.datetime):
            self._dates = [dates]

        elif not len(dates):
            self._dates = []

        else:
            # Check iterability
            for i in dates:
                if not isinstance(i,datetime.date):
                    raise Exception("Invalid input: 'dates' must be an iterable \
                        collection of datetime.datetime objects")
            self._dates = dates;

    def __getitem__(self,i):
        return self.dates[i]

    def __repr__(self):
        if len(self._dates) == 0:
            return 'DateList(Empty DateList)'
        else:
            return 'DateList('+str(len(self._dates))+' dates from '+ \
                str(self._dates[0])+' to '+str(self._dates[-1])+')'
    
    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return self._dates.__iter__() # Passthrough to date list

    def __len__(self):
        return len(self._dates)

    def __nonzero__(self):
        return self.__len__()
    
    def __contains__(self,d):
        if isinstance(date,datetimes.date):
            return date in self._dates

    def contains(self,date):
        return self.__contains__(date)

    def intersection(self,other):
        return DateList([d for d in self._dates if other.contains(d)])

class DateRange:
    #A line segment (or ray, or line) on the arrow of time.

    def __init__(self,date1,date2=None):
        # DESCRIPTION:
        #    Build a DateRange object
        #
        # PARAMS:
        #    date1: datetime.date[time] | None | DateRange
        #       One time bound (not necesarily the first one chronologically)
        #       or a DateRange object (in which case date2 is not needed).
        #
        #    [date2]=None: datetime.date[time] | None | datetime.timedelta
        #       Another time bound or a time period.
        #
        # NOTES:
        #    If both date1 and date2 are dates, they must have identical
        #    types. Date1 and date2 will be reordered internally, so date1 
        #    does not necessarily need to be before date2. If date2 is a 
        #    timedelta it can be negative.
        #
        # RAISES:
        #    TypeError: if date1 or date2 is not of an approprite type.
        #    ValueError: if date2 is specified when the input date1 is a
        #       DateRange.
        
        self._start = None # Set these so that we can use validate()
        self._end = None   

        # Construction by DateRange (a special case)
        if isinstance(date1,type(self)):
            if date2 is not None:
                raise ValueError('If date1 is a DateRange then date2 must'+
                    'be left empty')
            else:
                self._start = date1.start()
                self._end =   date1.end()

        else:
            if self._validate(date1):
                self._start = date1
            else:
                raise TypeError('date1 must be None or datetime.date(time)')
            
            if self._validate(date2):
                self._end = date2

            elif isinstance(date2,datetime.timedelta):
                self._end = self._start + date2

            else:
                raise TypeError('date2 must be None, '+str(type(self._start))+
                    'or datetime.timedelta, not '+str(type(date2)))

        # If both bounds are finite order them chronologically
        if (self._end is not None and
            self._start is not None and
            self._start>self._end):

            self._end,self._start=self._start,self._end

        # Remember the type of date that we are storing
        if self._start is not None:
            self._dateclass = type(self._start)

        elif self._end is not None:
            self._dateclass = type(self._end)

        else:
            self._dateclass = None

        if self._dateclass is not None:

            if self._dateclass is datetime.date:
                self._resolution = datetime.timedelta(days=1)

            elif self._dateclass is datetime.datetime:
                self._resolution = datetime.timedelta(microseconds=1)

            else:
                raise TypeError()


    def _validate(self,d):
        # DESCRIPTION:
        # 
        # RAISES: Nothing

        if d is None:
            return True

        if self._start is None:
            if self._end is None: # If both are None
                return isinstance(d,datetime.date)
            else:
                return isinstance(d,type(self._end))
        else:
            return isinstance(d,type(self._start))


    def _cast(self,d):
        # DESCRIPTION:
        #    Cast a datetime.datetime object into a type that matches
        #    start or end.
        #
        # PARAMS:
        #    d: datetime.datetime
        #
        # RETURNS:
        #    date if start or end are dates and datetime if start or end are
        #    datetimes. If both start and end are None (unbounded), then
        #    returns d unchanged.
        # 
        # RAISES:
        #    TypeError: if trying to convert from datetime to date (resulting
        #               in a loss of resolution).
        
        if ( d is None or 
             self._dateclass is None or
             type(d) is self._dateclass ):
            return d

        else:
            try:
                d = d.date()
                if not self._validate(d):
                    raise TypeError('Cannot cast from '+str(type(d))+' to '+
                        str(self._dateclass))
                return d

            except:
                raise TypeError('Cannot cast from '+str(type(d))+' to '+
                    str(self._dateclass))

    def start(self,setdate=False):
        # DESCRIPTION:
        #    Get or set the earliest bound for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.date[time] | None 
        #
        # RETURNS:
        #    [datetime.date[time]] if set is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate does not match type(end)
        #    ValueError: if setdate > end
        
        if setdate is not False:
            setdate = self._cast(setdate)

            if setdate is None:
                self._start = None

                if self.end() is None:
                    self._nobounds = True
            
            elif isinstance(setdate,type(self.end())):
                if setdate > self.end():
                    raise ValueError('Cannot set start to be before end: '+
                        str(setdate))

                self._start = setdate

            elif self.end() is None and isinstance(setdate,type(self.start())):
            	self._start = setdate

            else:
                raise TypeError('Can only set start to None or '+
                    str(type(self._end))+', not '+str(type(setdate)))

            return self

        else:
            return self._start


    def end(self,setdate=False):
        # DESCRIPTION:
        #    Get or set the latest bound for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.date[time] | other  
        #
        # RETURNS:
        #    [datetime.date[time]] if setdate is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate does not match type(start)
        #    ValueError: if setdate < start

        if setdate is not False:
            setdate = self._cast(setdate)

            if setdate is None:
                self._end = None

                if self.start() is None:
                    self._nobounds = True
            
            elif isinstance(setdate,type(self.start())):
                if setdate < self.start():
                    raise ValueError('Cannot set start to be before end: '+
                        str(setdate))

                self._end = setdate

            elif ( self.start() is None and
                   isinstance(setdate,type(self.end())) ):
            	self._end = setdate

            else:
                raise TypeError('Can only set start to None or '+
                    str(type(self._start))+', not '+str(type(setdate)))

            return self

        else:
            return self._end


    def __contains__(self,other):
        # DESCRIPTION:
        #    Check if a value or DateRange is fully inside this DateRange.
        #
        # PARAMS:
        #    other: datetime.date[time] | DateRange
        #
        # RETURNS:
        #    bool
        #
        # NOTES:
        #    This will does not do any explicit error checking. Rather, an
        #    error will be called if other is not None and is not comparable to
        #    start, end or both.
        #
        # RAISES:
        #    TypeError: if d in not comparable to start or end
        
        if other is self:
            return True
        
        elif isinstance(other,datetime.date):
            if self._start is None: # No lower bound
                if self._end is None:
                    return True
                else:
                    return self._end >= other
            else:                   # Finite lower bound
                if self._end is None:
                    return self._start <= other
                else:
                    return self._start <= other and self._end >= other

        elif type(other) is type(self):
            return other.start() in self and other.end() in self

        else:
            raise TypeError('Cannot compare DateRange with '+str(type(other)))


        
    def contains(self,date):
        # DESCRIPTION:
        #    Check if a value is inside this DateRange.
        #
        # PARAMS:
        #    d: datetime.date[time] | other
        #
        # RETURNS: bool
        # 
        # RAISES:
        #    TypeError: if d is not of type({start,end})

        return self.__contains__(date)


    def intersection(self,other):
        # DESCRIPTION:
        #    Find the intersection of this DateRange with another DateRange.
        #
        # PARAMS:
        #    other: DateRange
        #
        # RETURNS:
        #    DateRange representing the intersection of this object with
        #    another.
        #
        # NOTES:
        #    Returns None if self and other do not overlap
        #
        # RAISES:
        #    TypeError: if other is not a DateRange
        
        if other is self:
            return other

        if isinstance(other,type(self)):
            
            if other._start is None and self.start is None:
                start = None
            elif other._start is None:
                start = self._start
            elif self._start is None:
                start = other._start
            else:
                start = max(other._start,self._start)

            if other._end is None and self.start is None:
                end = None
            elif other._end is None:
                end = self._end
            elif self._end is None:
                end = other._end
            else:
                end = min(other._end,self._end)

            return DateRange(start,end)


    def span(self):
        # DESCRIPTION:
        #    Find out the length of spanned by start() and end().
        #
        # PARAMS:
        #    None
        #
        # RETURNS:
        #    datetime.timedelta representing the length of time spanned
        #
        # NOTES:
        #    Returns None if either of the bounds are None.
        #
        # RAISES:
        #    Nothing

        if self.end() is not None and self.start() is not None:
            return (self.end() - self.start()) + self._resolution
        else:
        	return None

    def __lt__(self,date):
        return date > self.end()


    def __gt__(self,date):
        return date < self.start()
    

    def __ge__(self,date):
        return self.__gt__(date) or self.__contains__(date)
    

    def __le__(self,date):
        return self.__lt__(date) or self.__contains__(date)


    def __str__(self):
        if self._start and self._end:
            return 'DateRange('+str(self._start)+' to '+str(self._end)+')'
        elif self._start:
            return  'DateRange(Beginning on '+str(self._start)+')'
        elif self._end:
            return  'DateRange(Ending on '+str(self._end)+')'
        else:
            return 'DateRange(All Dates)'
    
    def __repr__(self):
        return self.__str__()
    
    def startat(self,d):
        d = self._cast(d)
        return DateRange(d,self.end())

    def endat(self,d):
        d = self._cast(d)
        return DateRange(self.start(),d)


    def slide(self,td):
        return DateRange(self.start()+td,self.end()+td)


    #----------------------------------------------------------------
    #|        Generators for cycles inside of the DateRange         |
    #----------------------------------------------------------------


    def cycles(self,dt):
        if dt > datetime.timedelta(0):
            if self.start() is None:
                raise ValueError("timedelta indicates starting at infinite"+
                    "bound.")
            d = self.start()

        elif dt < datetime.timedelta(0):
            if self.end() is None:
                raise ValueError("timedelta indicates starting at infinite"+
                    "bound.")
            d = self.end()

        else:
            raise ValueError("timedelta cannot be 0.")

        while d in self:
            yield d
            d += dt


    def hours(self,snap=False,reverse=False):
        if reverse:
            if self.end() is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(hours=-1)
            d = self.end()
            end = self.start()
        else:
            if self.end() is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(hours=1)
            d = self.start()
            end = self.end()
        
        while d in self:
            yield d
            d += dtime
    

    def days(self,snap=False,reverse=False):
        if reverse:
            if self.end() is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(days=-1)
            d1 = self.end()
            end = self.start()

        else:
            if self.start() is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(days=1)
            d1 = self.start()
            end = self.end()
        
        dsnap = self._cast(datetime.datetime(d1.year,d1.month,d1.day))
        d_offset = d1 - dsnap

        if snap is True:
            d_offset = datetime.timedelta(0)

            if dsnap not in self:
                dsnap=(self._cast(datetime.datetime(d1.year,d1.month,d1.day))+
                       dtime)
        
        d = dsnap + d_offset

        while d in self:
            yield d
            # Must break out dsnap rather than taking the containing pentad
            # of d on each iteration, because it is possible to start this
            # generator with a d_offset of greater than five (last pentad)
            # of a leap year, in which case taking the pentad of a normal
            # date plus a 6-day d_offset may lead to a missed cycle.
            dsnap += dtime
            d = dsnap + d_offset

    def rdays(self,snap=False,reverse=False,full=False):
        # DESCRIPTION:
        gen = self.days(snap=snap,reverse=reverse)
        return self.rcycle(gen,snap=snap,reverse=reverse,full=full)

    def pentads(self,snap=False,reverse=False):
        # DESCRIPTION:
        #    Generate date(time)s representing the beginning of pentads in
        #    this DateRange
        #
        # PARAMS:
        #    [snap=False]: bool
        #       If snap is True then only 'clean' pentads in this DateRange.
        #
        #    [reverse=False]: bool
        #       If reverse is True, then date[time]s are generated in reverse
        #       chronological order.
        #
        # NOTES:
        #    A pentad is defined as a duration of time that breaks the year
        #    into exactly 73 portions, with all but the last portion required
        #    to have exactly 5 days. The last pentad will have 6 days only on
        #    leap years. The date[time]s generated here denote pentads by the
        #    first (chronologically) bound,
        #        e.g.:  1/1, 1/6, 1/11, 1/16, 1/21, 1/31, 2/5, 2/10...
        #    
        #    If the starting value of the pentad, either self.start() or
        #    self.end() if reverse if True, is not a 'clean' pentad that lands
        #    exactly on the list above, then the values are generated as
        #    follows:
        #    
        #    (1) The 'clean' pentad containing the initial date[time], start()
        #    (or end() if reverse if True), is found and the offset between
        #    these two dates if found. 
        #    (2) To generate subsequent values, the next 'clean' pentad is
        #    found and the offset calculated in step (1) is applied to it
        #
        #    If DateRange is based on datetime.date objects, then the offset
        #    and pentads generated will be dates. If the DateRange.
        #    the type of
        #    
        #
        #    To force this generator to yield only 'clean' pentad values in
        #    the parent DateRange, set snap to True.
        #
        # RAISES:
        #    ValueError(): if self.start() is None and reverse is False
        #    ValueError(): if self.end() is None and reverse is True

        if reverse:
            if self.end() is None:
                raise ValueError('Cannot start at infinity.')
            dpentad = -1
            d1 = self.end()
        else:
            if self.start() is None:
                raise ValueError('Cannot start at infinity.')
            dpentad = 1
            d1 = self.start()

        p = date_to_pentad(d1) # Pentad containing start datetime

        dsnap = self._cast(pentad_to_datetime(d1.year,p))
        
        d_offset = d1 - dsnap # 0 in the case that d1 is a calendar pentad

        if snap is True:
            d_offset = datetime.timedelta(0)

            if dsnap not in self:
                dy,p = bound_pentad(p+dpentad)
                dsnap = self._cast( pentad_to_datetime(dsnap.year+dy,p) )

        d = dsnap + d_offset

        while d in self:
            yield d
            # Must break out dsnap rather than taking the containing pentad
            # of d on each iteration, because it is possible to start this
            # generator with a d_offset of greater than five (last pentad)
            # of a leap year, in which case taking the pentad of a normal
            # date plus a 6-day d_offset may lead to a missed cycle.
            dy,p = bound_pentad( date_to_pentad(dsnap) + dpentad )
            dsnap = self._cast( pentad_to_datetime(dsnap.year+dy,p) )
            d = dsnap + d_offset


    def rpentads(self,snap=False,reverse=False,full=False):
        # DESCRIPTION:
        #    Generate DateRanges within from this DateRange one pentad in
        #    duration and in chronological order.
        #
        # PARAMS:
        #    [snap=False]: bool
        #       If set to True then DateRanges will be snapped to logical
        #       calendar breaks.
        #
        #    [reverse=False]: bool
        #       If set to True then we will generate DateRanges in reverse
        #       chronological order
        #
        #    [full=False]: bool
        #       If set to True then partial DateRanges on either side will
        #       be skipped.
        #
        # RETURNS:
        #    generator that yields DateRanges that cover exactly a pentad.
        #    A pentad is defined
        #
        # NOTES: The DateRanges generated are guaranteed to be non-overlapping
        #        and exhaustive within the specified period. Possible
        #        exceptions to this rule arise on either end if full is True.
        #
        # RAISES:
        #    ValueError: if we try starting the generator at an unbounded date
        #    StopIteration: once we have cycled throughall possible DateRanges

        gen = self.pentads(reverse=reverse,snap=snap)
        return self.rcycle(gen,reverse=reverse,snap=snap,full=full)
    

    
    def months(self,snap=False,reverse=False):
        
        if reverse:
            if self.end() is None:
                raise ValueError("Cannot start at infinity.")
            dmonth = -1
            d = self.end()

        else:
            if self.start() is None:
                raise ValueError("Cannot start at infinity.")
            dmonth = 1
            d = self.start()

        # First of the month
        m = d.month
        dsnap = self._cast(datetime.datetime(d.year,d.month,1))
        d_offset = d - dsnap # 0 in the case that d1 is a calendar pentad
        
        if snap is True:
            d_offset = datetime.timedelta(0)

            if dsnap not in self:
                dy,m = bound_month(m+dmonth)
                dsnap = self._cast(datetime.datetime(dsnap.year+dy,m,1))

        d = dsnap + d_offset

        while d in self:
            yield d
            # Must break out dsnap rather than taking the containing pentad
            # of d on each iteration, because it is possible to start this
            # generator with a d_offset of greater than five (last pentad)
            # of a leap year, in which case taking the pentad of a normal
            # date plus a 6-day d_offset may lead to a missed cycle.
            dy,m = bound_month(d.month+dmonth)
            dsnap = self._cast(datetime.datetime(d.year+dy,m,1))
            d = dsnap + d_offset
    
    def rmonths(self,snap=False,reverse=False,full=False):
        gen = self.months(snap=snap,reverse=reverse)
        return self.rcycle(gen,snap=snap,reverse=reverse,full=full)
    
    def years(self,reverse=False,snap=False):

        if reverse:
            if self.end() is None:
                raise ValueError("Cannot start at infinity.")
            dyear = -1
            d = self.end()

        else:
            if self.start() is None:
                raise ValueError("Cannot start at infinity.")
            dyear = 1
            d = self.start()

        if snap is True:
            d = self._cast(datetime.datetime(d.year,1,1)) 
            if not d in self:
                d = self._cast(datetime.datetime(d.year+dyear,1,1))

        else: # snap is false, we can start at d
            month,day = d.month,d.day
            d_offset = d - self._cast(datetime.datetime(d.year,month,day))

        while d in self:
            yield d

            if snap is True:
                d = self._cast(datetime.datetime(d.year+dyear,1,1))
            else:
                d = self._cast(datetime.datetime(d.year+dyear,month,day)+
                               d_offset)

    def ryears(self,snap=False,reverse=False,full=False):
        gen = self.years(snap=snap,reverse=reverse)
        return self.rcycle(gen,snap=snap,reverse=reverse,full=full)

    def rcycle(self,gen,snap=False,reverse=False,full=False):
        # DESCRIPTION:
        #    Generate DateRanges from using date[time] generator
        #
        # PARAMS:
        #    gen: generator object
        #       Can be a built in one like months() or pentads() or a user-
        #       defined one. It must generate dates or datetimes if _dateclass
        #       is datetime.date of datetimes if _dateclass is datetime.
        #    
        #    [snap=False]: bool
        #    [reverse=False]: bool
        #    [full=False]: bool
        #
        # RETURNS:
        #    A generator that produces DateRanges inside of the bounds of the
        #    parent DateRange
        # 
        # RAISES:
        #    ValueError: if we call bools with something other than True or False
        # NOTES:
        # 
        
        if not (full is False or full is True):
            raise ValueError('full must be True or False.')
        elif not (reverse is False or reverse is True):
            raise ValueError('reverse must be True or False.')
        if not (snap is False or snap is True):
            raise ValueError('span must be True or False.')

        if reverse is True:
            resolution_modifier = self._resolution
            natural_start = self.end()
            natural_end = self.start()

        elif reverse is False:
            resolution_modifier = -self._resolution
            natural_start = self.start()
            natural_end = self.end()
        
        # If we can't generate a single date...
        try: 
            maybe_start = next(gen)

        except StopIteration:
            print('hai')
            if full is True:
                raise StopIteration
            else:
                yield DateRange(self.start(),self.end())
                raise StopIteration

        # Handle cases where we can't generate a second date
        if full is True:
            try:
                start = maybe_start
                _start = next(gen)
            except StopIteration:
                raise StopIteration

        else:
            if natural_start == maybe_start:
                try:
                    start = natural_start
                    _start = next(gen)

                except StopIteration:
                    yield DateRange(start,natural_end)
                    raise StopIteration
            else:
                start = natural_start
                _start = maybe_start

        end = _start + resolution_modifier

        # Bound the end in the case that we go over
        if end not in self:
            if full is False:
                yield DateRange(natural_start,natural_end)
            else:
                raise StopIteration

        # The big loop
        try:
            while end in self:

                yield DateRange(start,end)

                start = _start
                _start = next(gen)
                end = _start + resolution_modifier
        
        except StopIteration:
            # Handles the case where the last iterations' start is equal
            # to the stopping criterion (self._start if reverse or
            # self._end if not) At this point, end is NOT in the range, so we
            # know that this DateRange is not 'full'

            if full is False and start in self:
                # Start must be in self to prevent the edge case where the 
                # last iteration ended perfectly on a bound, in which case we
                # do not want to yield any more values
                if reverse is True :
                    yield DateRange(start,self.start())

                else: # reverse is False
                    yield DateRange(self.end(),start)


def date_to_dayofyear(d):
    # Input a datetime.datetime object and return the interger day of year
    # Return value will be in the range [1,366]
    if not isinstance(d,datetime.date) or isinstance(d,datetime.datetime):
        d = d.date()
    return (d - datetime.date(d.year,1,1)).days + 1


def dayofyear_to_date(year,doy):
    return datetime.date(year,1,1)+datetime.timedelta(days=doy-1)


def dayofyear_to_datetime(year,doy):
    return datetime.datetime(year,1,1)+datetime.timedelta(days=doy-1)


def date_to_pentad(d):
    # Convert a datetime.date object to a yearly pentad in the range [1,73]
    # For leap years the last day of the year (day 366) is put in the last
    #pentad
    # The input can also be an integer corresponding to the day of year
    
    if isinstance(d,int):
        doy = d
    else:
        doy = date_to_dayofyear(d)
    
    if doy == 366:
        doy = 365
    
    return int((doy-1)/5.00) + 1


def pentad_to_dayofyear(pentad):
    if pentad > 73 or pentad < 1:
        raise Exception("pentad out of range")
    # This function is leap invariant
    # Returns an int corresponding to the day of year
    return ((pentad-1)*5)+1


def pentad_to_date(year,pentad):
    return dayofyear_to_date(year,pentad_to_dayofyear(pentad))


def pentad_to_datetime(year,pentad):
    dy,pentad = bound_pentad(pentad)
    return dayofyear_to_datetime(year+dy,pentad_to_dayofyear(pentad))


def pentad_to_daterange(year,pentad):
    # For a given year and pentad, generate a DateRange
    dy,pentad = bound_pentad(pentad)
    year = year + dy # Roll year
    d1 = pentad_to_datetime(year,pentad)
    
    if pentad == 73:
        d2 = (datetime.datetime(year+1,1,1) - 
              datetime.timedelta(microseconds=1))
    else:   
        d2 = d1 + datetime.timedelta(days=5,microseconds=-1)
    
    return DateRange(d1,d2)


def bound_cyclic(i,period):
    if i >= 1 and i <= period:
        return(0,i)
    elif i > period:
        return(int(i/period),i%period) 
    elif i < period:
        return (int((i-period)/period),period-(abs(i)%period))


def bound_hour(hr):
    return bound_cyclic(hr,24)


def bound_month(m):
    return bound_cyclic(m,12)


def bound_pentad(pentad,year=None):
    dy,p = bound_cyclic(pentad,73)
    if year is not None:
        return dy+year,p
    else:
        return dy,p


def month_to_daterange(year,month):
    # Construct a daterange object
    d1 = datetime.datetime(year,month,1)

    dy,month = bound_month(month+1)

    d2 = (datetime.datetime(year+dy,month,1) - 
          datetime.timedelta(microseconds=1))

    return DateRange(d1,d2)

