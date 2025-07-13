
def sma(close, length=None, talib=None, offset=None, **kwargs):
    # Convert input to list to avoid pandas indexing issues
    if close is None:
        return None
    
    try:
        # Convert any iterable to list (pandas Series, tuple, numpy array, etc.)
        close = list(close)
    except TypeError:
        raise TypeError("close must be an iterable")
    
    n = len(close)
    if n == 0:
        return None

    # Validate parameters
    length = int(length) if length is not None and length > 0 else 10
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    offset = int(offset) if offset is not None else 0

    # Precompute cumulative sums for efficient SMA calculation
    cumulative = [0] * (n + 1)
    for i in range(1, n + 1):
        cumulative[i] = cumulative[i - 1] + close[i - 1]

    # Calculate SMA with min_periods handling
    sma_vals = []
    for i in range(n):
        start_idx = max(0, i - length + 1)
        window_length = i - start_idx + 1
        
        if window_length < min_periods:
            sma_vals.append(None)
        else:
            window_sum = cumulative[i + 1] - cumulative[start_idx]
            sma_vals.append(window_sum / window_length)

    # Apply offset
    if offset > 0:
        sma_vals = [None] * offset + sma_vals[:n-offset]
    elif offset < 0:
        offset_abs = abs(offset)
        sma_vals = sma_vals[offset_abs:] + [None] * min(offset_abs, n)

    # Handle fillna
    if "fillna" in kwargs:
        fill_val = kwargs["fillna"]
        sma_vals = [fill_val if x is None else x for x in sma_vals]

    # Handle fill methods
    if "fill_method" in kwargs:
        method = kwargs["fill_method"]
        n = len(sma_vals)
        
        if method == "ffill":
            last_val = None
            for i in range(n):
                if sma_vals[i] is not None:
                    last_val = sma_vals[i]
                elif last_val is not None:
                    sma_vals[i] = last_val
        
        if method == "bfill":
            next_val = None
            for i in range(n-1, -1, -1):
                if sma_vals[i] is not None:
                    next_val = sma_vals[i]
                elif next_val is not None:
                    sma_vals[i] = next_val

    return sma_vals





def shift_list(arr, offset):
    if offset == 0:
        return arr
    n = len(arr)
    if offset > 0:
        return [None] * offset + arr[:-offset]
    else:
        return arr[-offset:] + [None] * (-offset)

def fillna(arr, fill_value=None, fill_method=None):
    if fill_value is not None:
        return [fill_value if x is None else x for x in arr]
    elif fill_method == 'ffill':
        result = []
        last_val = None
        for x in arr:
            if x is not None:
                last_val = x
                result.append(x)
            else:
                result.append(last_val)
        return result
    return arr

def hl2(high, low):
    return [(h + l) / 2.0 for h, l in zip(high, low)]

def atr(high, low, close, length):
    n = len(high)
    tr = [0.0] * n
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i-1])
        tr3 = abs(low[i] - close[i-1])
        tr[i] = max(tr1, tr2, tr3)
    
    atr_values = [None] * n
    if n < length:
        return atr_values
    
    # Calculate the first ATR as the average of the first 'length' TRs
    atr_values[length-1] = sum(tr[:length]) / length
    for i in range(length, n):
        atr_values[i] = (atr_values[i-1] * (length - 1) + tr[i]) / length
    
    return atr_values

def supertrend(high, low, close, length=None, multiplier=None, offset=None, **kwargs):
    # Validate and set default parameters
    length = int(length) if length and length > 0 else 7
    multiplier = float(multiplier) if multiplier and multiplier > 0 else 3.0
    offset = int(offset) if offset else 0
    
    m = len(close)
    # Validate series length
    if m < length or len(high) != m or len(low) != m:
        return None
    
    # Initialize arrays
    dir_ = [1] * m
    trend = [None] * m
    long = [None] * m
    short = [None] * m
    
    # Calculate HL2 and ATR
    hl2_ = hl2(high, low)
    atr_values = atr(high, low, close, length)
    
    # Compute upper and lower bands
    upperband = [None] * m
    lowerband = [None] * m
    for i in range(m):
        if atr_values[i] is not None:
            upperband[i] = hl2_[i] + multiplier * atr_values[i]
            lowerband[i] = hl2_[i] - multiplier * atr_values[i]
    
    # Process Supertrend logic starting from the 'length' index
    for i in range(length, m):
        if close[i] > upperband[i-1]:
            dir_[i] = 1
        elif close[i] < lowerband[i-1]:
            dir_[i] = -1
        else:
            dir_[i] = dir_[i-1]
            if dir_[i] == 1 and lowerband[i] < lowerband[i-1]:
                lowerband[i] = lowerband[i-1]
            elif dir_[i] == -1 and upperband[i] > upperband[i-1]:
                upperband[i] = upperband[i-1]
        
        if dir_[i] == 1:
            trend[i] = lowerband[i]
            long[i] = lowerband[i]
        else:
            trend[i] = upperband[i]
            short[i] = upperband[i]
    
    # Apply offset if needed
    if offset != 0:
        trend = shift_list(trend, offset)
        dir_ = shift_list(dir_, offset)
        long = shift_list(long, offset)
        short = shift_list(short, offset)
    
    # Handle fillna parameters
    fill_value = kwargs.get('fillna', None)
    fill_method = kwargs.get('fill_method', None)
    
    trend = fillna(trend, fill_value, fill_method)
    dir_ = fillna(dir_, fill_value, fill_method)
    long = fillna(long, fill_value, fill_method)
    short = fillna(short, fill_value, fill_method)
    
    # Prepare result dictionary
    _props = f"_{length}_{multiplier}"
    return {
        f"SUPERT{_props}": trend,
        f"SUPERTd{_props}": dir_,
        f"SUPERTl{_props}": long,
        f"SUPERTs{_props}": short
    }

