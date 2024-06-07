import pandas as pd

def df_rebase(df, order, rename):
    df = df[order]
    df.columns = rename
    return df

def butter_lowpass_filter(data, cutoff, fs, order):
    from scipy.signal import butter, filtfilt
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def split_windows(df, window_size, overlap):
    step = window_size - overlap
    windows = [df[i:i + window_size] for i in range(0, len(df), step) if len(df[i:i + window_size]) == window_size]
    return windows
