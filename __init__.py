# aeon
# A python module for working with dates and date ranges

__author__ = "Michael Vijay Saha"

import datetime

class DateRange:
    #    A class for specifying a line segment (or ray, or line) on the arrow
    #    of time.

    def __init__(self,date1,date2=None):
        # DESCRIPTION:
        #    Build a DateRange object
        #
        # PARAMS:
        #    date1: datetime.date(time) | None | DateRange
        #       One time bound (not necesarily the first one chronologically)
        #       or a DateRange object (in which case date2 is not needed).
        #
        #    [date2]=None: datetime.date(time) | None | datetime.timedelta
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
        #    ValueError: if date2 is specified when the input (date1) is a
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
        # Returns true if d matches type({start,end}) or is None.
        if d is None:
            return True

        if self._start is None:
            if self._end is None: # If both are None
                return isinstance(d,datetime.date)
            else:
                return isinstance(d,type(self._end))
        else:
            return isinstance(d,type(self._start))


    def start(self,setdate=False):
        # DESCRIPTION:
        #    Get or set the earliest bound for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.date(time) | None 
        #
        # RETURNS:
        #    [datetime.date(time)] if set is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate does not match type(end)
        #    ValueError: if setdate > end

        if setdate is not False:
            if setdate is None or self._end is None:
                self._start = None

                if self._end is None:
                    self._nobounds = True

            elif isinstance(setdate,type(self._end)):
                if setdate > self._end:
                    raise ValueError('Cannot set start to be before end: '+
                        str(setdate))
                
                self._start = setdate

            else:
                raise TypeError('Can only set start to None or '+
                    str(type(self._end))+', not '+str(type(setdate)))

        else:
            return self._start


    def end(self,setdate=False):
        # DESCRIPTION:
        #    Get or set the latest bound for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.date(time) | other  
        #
        # RETURNS:
        #    [datetime.date(time)] if setdate is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate does not match type(start)
        #    ValueError: if setdate < start

        if setdate is not False:
            if setdate is None:
                self._end = None

            elif isinstance(setdate,type(self._start)):
                if setdate < self._start:
                    raise ValueError('Cannot set start to be before end: '+
                        str(setdate))
                
                self._end = setdate

            else:
                raise TypeError('Can only set start to None or '+
                    str(type(self._end))+', not '+str(type(setdate)))

        else:
            return self._end


    def __contains__(self,d):
        # DESCRIPTION:
        #    Check if a value is inside this DateRange.
        #
        # PARAMS:
        #    d: datetime.date(time)
        #
        # RETURNS:
        #    bool
        #
        # NOTES:
        #    This will does not do any explicit error checking. Rather, an
        #    error will be called if d is not None and is not comparable to
        #    start, end or both.
        #
        # RAISES:
        #    TypeError: if d in not comparable to start or end
        
        if self._start is None: # No lower bound
            if self._end is None:
                return True
            else:
                return self._end >= d
        else:                   # Finite lower bound
            if self._end is None:
                return self._start <= d
            else:
                return self._start <= d and self._end >= d

        
    def contains(self,date):
        # DESCRIPTION:
        #    Check if a value is inside this DateRange.
        #
        # PARAMS:
        #    d: datetime.date(time) | other
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
        #    Find out the length of time between the first and second date
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

        if self._end is not None or self._start is not None:
            return self._end - self._start


    def __lt__(self,date):
        return date > self._end


    def __gt__(self,date):
        return date < self._start
    

    def __ge__(self,date):
        return self.__gt__(date) or self.__contains__(date)
    

    def __le__(self,date):
        return self.__lt__(date) or self.__contains__(date)
    
    # Probably should remove this...
    def __getitem__(self,i):
        if i is 0:
            return self._start
        elif i is 1:
            return self._end
        else:
            raise Exception("Index out of bounds {0,1}.")


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
        
        if self._dateclass is None or type(d) is self._dateclass:
            return d
        else:
            try:
                d = d.date()
                if not self._validate(d):
                    raise TypeError('Cannot cast from '+str(type(d))+' to '+
                        self._dateclass)
            except:
                raise TypeError('Cannot cast from '+str(type(d))+' to '+
                    self._dateclass)

    def hours(self,reverse=False):
        if reverse:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(hours=-1)
            d = self._end
            end = self._start
        else:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(hours=1)
            d = self._start
            end = self._end
        
        while d in self:
            yield d
            d += dtime
    

    def days(self,reverse=False):
        if reverse:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(days=-1)
            d = self._end
            end = self._start
        else:
            if self._start is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(days=1)
            d = self._start
            end = self._end
        
        while d in self:
            yield d
            d += dtime


    def pentads(self,reverse=False,snap=False):
        if reverse:
            if self._end is None:
                raise ValueError('Cannot start at infinity.')
            dpentad = -1
            d1 = self._end
            end = self._start
        else:
            if self._start is None:
                raise ValueError('Cannot start at infinity.')
            dpentad = 1
            d1 = self._start
            end = self._end

        p1 = date_to_pentad(d1) # Pentad containing start date

        #offset = self._cast(pentad_to_date(d.year,p)) - p1

        if self._cast(pentad_to_datetime(d1.year,p1)) not in self:
            dy,p = bound_pentad(p1+dpentad) # Go to the nearest pentad
            d = self._cast(pentad_to_datetime(d1.year+dy,p))
            p_offset = d1-self._cast(pentad_to_datetime(d1.year,p1))
        else:
            p = p1
            d = d1
            p_offset = datetime.timedelta(0)

        if snap is not True:
            d = d1

        while d in self:
            
            yield d

            p = date_to_pentad(d)
            p += dpentad
            dy,p = bound_pentad(p)

            if snap is True:
                d = self._cast(pentad_to_datetime(d.year+dy,p))
            else:
                d = self._cast(pentad_to_datetime(d.year+dy,p)) + p_offset

    def rpentads(self,reverse=False,snap=False,full=False):
        # DESCRIPTION:
        #    Generator for a range 
        #
        # PARAMS:
        #    reverse: bool
        #       If set to True then we will generate DateRanges in reverse
        #       chronological order
        #    
        #    snap: bool
        #       If set to True then DateRanges will be snapped to logical
        #       calendar breaks.
        #   
        #    full: bool
        #       If set to True then DateRanges will only be returned if they
        #       represent a full calendar pentad.
        #
        # RETURNS:
        #    a DateRange representing a pentad
        #
        # RAISES:
        #    StopIteration: once we have cycled throughall possible DateRanges

        gen = self.pentads(reverse=reverse,snap=snap)

        if reverse is True:
            resolution_modifier = self._resolution

        elif reverse is False:
            resolution_modifier = -self._resolution

        else:
            raise ValueError('reverse must be True or False')

        if snap is True:

            if full is True: # pentads knows where to go
                # if pentads is a full, then go to the first full pentad
                # as a start

                start = next(gen)
                end = next(gen)

            else: # full is False
                if reverse is True:
                    start = self.end()
                    end = next(gen)

                else: # reverse if False
                    start = self.start()
                    end = next(gen)


        elif snap is False:
            # snapping to calendar dates not engaged...
            


        else:
            raise TypeError('snap must be True or False.')

        while end is in :

            yield DateRange(start,end)


            if end not in self:
                if full is True:
                    raise StopIteration
                else:
                    pass
                    #return DateRange(start,self._endOR_start->basedOnReverse)

        #after while is broken, check for full
        # if full is False:
        #     return (remaining chunk)






    
    def months(self,reverse=False):
        
        if reverse:
            if self._end is None:
                raise ValueError("Cannot start at infinity.")
            dmonth = -1
            d = self._end
            end = self._start
        else:
            if self._start is None:
                raise ValueError("Cannot start at infinity.")
            dmonth = 1
            d = self._start
            end = self._end
        
        m = d.month
        
        while d in self:
            yield d
            
            m += dmonth
            (dy,m) = bound_month(m)
            
            d = datetime.datetime(d.year+dy,m,d.day,d.hour,
                d.minute,d.second,d.microsecond)
    
    
    def years(self,reverse=False,snap=True):
        if reverse:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            d = self._end
            interval = 1
        else:
            if self._start is None:
                raise Exception("Cannot start at infinity.")
            d = self._start
            interval = -1

        while d <= self._end:
            yield d
            y = d.year + 1
            d = datetime.datetime(y,d.month,d.day,d.hour,
                d.minute,d.second,d.microsecond)


    def cycle(self,reverse=False):
        pass




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


def days_in_month(y,m):
    m += 1
    if m >= 13:
        m = m - 12
        y += 1

    return (datetime.date()-datetime.timedelta(days=1)).days


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
    return dayofyear_to_date(year,((pentad-1)*5)+1)


def pentad_to_datetime(year,pentad):
    return dayofyear_to_datetime(year,((pentad-1)*5)+1)


def pentad_to_daterange(year,pentad):
    # For a given year and pentad, generate a DateRange
    d1 = pentad_to_date(year,pentad)
    
    if pentad == 73:
        d2 = (datetime.datetime(year+1,1,1) - 
              datetime.timedelta(microseconds=1))
    else:   
        d2 = d1 + datetime.timedelta(days=5,microseconds=-1)
    
    return gs.DateRange(d1,d2)


def bound_month(i):
    # Helper function that takes and integer representing a month
    #{1...12}
    # Thus an integer value of 1 represents Jan, 0:Dec, -1:Nov
    # as well as 13:Jan, 14:Feb, and so on...
    # and bounds rolls it over so 
    # Returns a 2-tuple corresponding to relative year and rolled month:
    # (yr,month)
    # (-1,bounded_month) if i is 0 or negative
    # (0,i)              if i is in {1:12}
    # (1,bounded_month)  if i is positive
        
    if i >= 1 and i <= 12:
        return (0,i)
    elif i > 12:
        return (1,i%12)
    else:
        return (-1,(12-(abs(i)%12)))


def bound_cyclic(i,period): # Assume 1:period labels
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


def bound_pentad(pentad):
    return bound_cyclic(pentad,73)


def month_to_daterange(year,month):
    # Construct a daterange object
    d1 = datetime.datetime(year,month,1)
    dy,month = bound_month(year,month+1)
    d2 = (datetime.datetime(year+dy,month,1) - 
          datetime.timedelta(microseconds=1))

    return gs.DateRange(d1,d2)