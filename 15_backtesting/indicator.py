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