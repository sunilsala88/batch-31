
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


