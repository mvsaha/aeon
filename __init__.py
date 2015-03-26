# aeon
# A python module for working with dates and date ranges

__author__ = "Michael Vijay Saha"

import datetime

class DateRange:
    #    A class for specifying a line segment (or line, or ray) on the arrow
    #    of time.
    
    def __init__(self,date1,date2=None):
        # DESCRIPTION:
        #    Build a datetime.datetime object
        #
        # PARAMS:
        #    date1: datetime.date(time) | None | DateRange
        #       One time bound (not necesarily the first one chronologically)
        #       or a DateRange object (in which case date2 is not needed).
        #
        #    [date2]: datetime.date(time) | None | datetime.timedelta
        #       Another time bound or a time period. If date2 is a timedelta
        #       it can be negative.
        #
        # RETURNS:
        #    Nothing
        #
        # NOTES:
        #    date1 and date2 will be reordered internally, so date1 does not
        #    necessarily need to be before date2.
        #
        # RAISES:
        #    TypeError if date1 or date2 is not of an approprite type
        
        if date1 is None:
            self._start = None

        elif isinstance(date1,self.type):
            

        elif isinstance(date1,datetime.date):
            self._start = date1

            if date2 is None:
                self._end = None

            elif isinstance(date2,datetime.date):
                self._end = date2

            elif isinstance(date2,datetime.timedelta):
                self._end = self._start + date2

            else:
                raise TypeError('Argument 2 must be None, '+
                    'datetime.datetime or datetime.timedelta')

        else:
            raise TypeError('Argument 1 must be None or datetime.datetime')

        # Make sure that _end is ALWAYS chronologically last if both bounds 
        # are finite
        if self._end and self._start and self._start>self._end:
            self._end,self._start=self._start,self._end

    def start(self,set_date=False):
        # DESCRIPTION:
        #    Get or set the starting period for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.date(time) object  
        #
        # RETURNS:
        #    datetime.date(time) if set is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate is not a datetime.date(time)
        #    ValueError: if setdate > end date

        if set_date is not False:
            if date1 is None:
                self.start = None
            elif isinstance(set_date,datetime.date):
                set_date = self.date_to_datetime(set_date)
                if set_date > self._end:
                    raise Exception('Cannot set start to be before end: %s',
                        set_date)
                self._start = set_date
            else:
                raise Exception('Can only set end() to None or '+
                    'datetime.datetime:%s',set_date)
        else:
            return self._start

    def end(self,setdate=False):
        # DESCRIPTION:
        #    Get or set the ending period for DateRange
        #    
        # PARAMS:
        #    [setdate]: datetime.datetime object  
        #
        # RETURNS:
        #    datetime.datetime if set is not specified (getter mode)
        #
        # RAISES:
        #    TypeError: if setdate is not a datetime.datetime
        #    ValueError: if setdate < start date

        if setdate is not False:
            if not isinstance(setdate,datetime.datetime):
                raise TypeError('Must be a ')

            if setdate is None:
                self._end = None

            elif setdate < self._start:
                raise ValueError('Cannot set end to be before start: %s',
                    setdate)

            self._end = setdate

        else:
            return self._end

    def __contains__(self,other):
        # Try converting if necessary
        if not isinstance(other,datetime.date):
            try:
                other = other.date()
                assert(isinstance(other,datetime.date))
            except:
                raise Exception('Not convertible to datetime.date or'+
                    ' datetime.datetime comparison')

        # If we have a datetime
        if isinstance(other,datetime.datetime):
            if self._start and self._end:
                return other>=self._start and other<=self._end
            elif self._start:
                return other>=self._start
            elif self._end:
                return other<=self._end
            else: # Both dates are none and therefore contain all dates
                return True

        else:
            assert(isinstance(other,datetime.date))
            if self._start and self._end:
                return other>=self._start.date() and other<=self._end.date()
            elif self._start:
                return other>=self._start.date()
            elif self._end:
                return other<=self._end.date()
            else: # Both dates are none and therefore contain all dates
                return True
        
    def contains(self,date):
        return self.__contains__(date)

    def intersection(self,other):
        # DESCRIPTION:
        #    Find the intersection of this DateRange with another DateRange.
        #
        # PARAMS:
        #    other:DateRange
        #
        # RETURNS:
        #    DateRange representing the intersection of this object with another.
        #
        # NOTES:
        #
        # RAISES:
        #    Nothing

        if self is other: # Check for self comparison
            return self

        elif isinstance(other,self.__class__): # both DateRange

            if other._end and self._start: # If there are non-overlapping
                if other._end < self._start:
                    return DateList([])
            elif other._start and self._end:
                if other._start > self._end:
                    return DateList([])

            if other._start and self._start:
                start = max(other._start,self._start)
            elif other._start:
                start = other._start
            elif self._start:
                start = self._start
            else:
                start = None

            if other._end and self._end:
                end = min(other._end,self._end)
            elif other._end:
                end = other._end
            elif self._end:
                end = self._end
            else:
                end = None

            return DateRange((start,end))

        else: # Dates must be a DateList
            return DateList([ d for d in other._dates if self.contains(d) ])
    
    def date_to_datetime(self,d):
        return datetime.datetime(*d.timetuple()[:6])

    def span(self):
        # DESCRIPTION:
        #    Find out the length of time between the first and second date
        #
        # PARAMS:
        #    NONE
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
        # Returns True if and only if the date is greater than _end
        # If _end of the DateRange is open (i.e None) it will return False
        print('calling __lt__()')
        # Try to cast it as a datetime.date
        if not isinstance(date,datetime.datetime):
            try:
                date = date_to_datetime(date)
            except:
                raise Exception('Invalid comparison')

        if self._end is None:
            return False
        else:
            return date > self._end

    def __gt__(self,date):
        print('calling __gt__()')
        # Try to cast it as a datetime.date
        if not isinstance(date,datetime.datetime):
            try:
                date = date_to_datetime(date)
            except:
                raise Exception('Invalid comparison')

        if self._start is None:
            return False
        else:
            return date < self._start

    
    def __ge__(self,date):
        return self.__gt__(date) or self.__contains__(date)
    
    
    def __le__(self,date):
        return self.__lt__(date) or self.__contains__(date)
    
    
    def __getitem__(self,i):
        ##
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
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dtime = datetime.timedelta(days=1)
            d = self._start
            end = self._end
        
        while d in self:
            yield d
            d += dtime
    
    
    def months(self,reverse=False):
        
        if reverse:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dmonth = -1
            d = self._end
            end = self._start
        else:
            if self._end is None:
                raise Exception("Cannot start at infinity.")
            dmonth = 1
            d = self._start
            end = self._end
        
        m = d.month
        
        while d in self:
            yield d
            
            m += dmonth
            (dy,m) = self._bound_month(m)
            
            d = datetime.datetime(d.year+dy,m,d.day,d.hour,
                d.minute,d.second,d.microsecond)
    
    
    def years(self,to=None,reverse=False):
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

    def cycle(self,to=None,reverse=False):
        pass

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

    def __contains__(self,date):
        if isinstance(date,datetimes.datetime):
            return date in self._dates
        elif isinstance(date,File):
            return date._date in self._dates

    def contains(self,date):
        return self.__contains__(date)

    def intersection(self,dates):
        return DateList([d for d in self._dates if dates.contains(d)])

def _days_in_month(y,m):
            m += 1
            if m >= 13:
                m = m - 12
                y += 1
            return (datetime.date()-datetime.timedelta(days=1)).days


def date_to_dayofyear(d):
    # Input a datetime.datetime object and return the interger day of year
    # Return value will be in the range [1,366]
    if not isinstance(d,datetime.date) or isinstance(d,datetime.datetime):
        d = d.date()

    return (d - datetime.date(d.year,1,1)).days + 1


def dayofyear_to_date(year,doy):
    return datetime.datetime(year,1,1)+datetime.timedelta(days=doy-1)


def days_in_month(y,m):
    m += 1
    if m >= 13:
        m = m - 12
        y += 1

    return (datetime.date()-datetime.timedelta(days=1)).days


def date_to_pentad(d):
    # Convert a datetime.date object to a yearly pentad in the range [1,73]
    # For leap years the last day of the year (day 366) is put in the last pentad
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



def pentad_to_daterange(year,pentad):
    # For a given year and pentad, generate a DateRange
    d1 = pentad_to_date(year,pentad)
    
    if pentad == 73:
        d2 = datetime.datetime(year+1,1,1)-datetime.timedelta(microseconds=1)
    else:   
        d2 = d1 + datetime.timedelta(days=5,microseconds=-1)
    
    return gs.DateRange(d1,d2)



def bound_month(self,i):
        # Helper function that takes and integer representing a month {1...12}
        # Thus an integer value of 1 represents Jan, 0:Dec, -1:Nov
        # as well as 13:Jan, 14:Feb, and so on...
        # and bounds rolls it over so 
        # Returns a 2-tuple corresponding to relative year and rolled month: (yr,month)
        # (-1,bounded_month) if i is 0 or negative
        # (0,i)              if i is in {1:12}
        # (1,bounded_month)  if i is positive
        
        if i >= 1 and i <= 12:
            return (0,i)
        elif i > 12:
            return (1,i%12)
        else:
            return (-1,(12-(abs(i)%12)))



def month_to_daterange(year,month):
    # Construct a daterange object
    d1 = datetime.datetime(year,month,1)
    dy,month = bound_month(year,month+1)
    d2 = datetime.datetime(year+dy,month,1) - datetime.timedelta(microseconds=1)
    return gs.DateRange(d1,d2)