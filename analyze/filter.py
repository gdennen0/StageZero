from scipy.signal import butter, cheby1, cheby2, ellip, bessel, lfilter


def apply_filter(filter_type, cutoff, song_data, sample_rate):
    # Ensure inputs are of correct data type
    filter_type = str(filter_type)
    cutoff = float(cutoff)
    sample_rate = int(sample_rate)

    if isinstance(cutoff, list):
        normalized_cutoff = [freq / (0.5 * sample_rate) for freq in cutoff]
        if not all(0 < freq < 1 for freq in normalized_cutoff):
            raise ValueError("Cutoff frequencies must be between 0 and half the sample rate")
    else:
        normalized_cutoff = cutoff / (0.5 * sample_rate)
        if not 0 < normalized_cutoff < 1:
            raise ValueError("Cutoff frequency must be between 0 and half the sample rate")


    print(f"filter type {filter_type} cutoff {cutoff} sample rate {sample_rate}")
    N = 5  # Filter order can be changed based on requirements

    # Determine the filter type and set the special_parameter
    if filter_type == "Low-pass":
        b, a = butter(N, normalized_cutoff, btype='low')
    elif filter_type == "High-pass":
        b, a = butter(N, normalized_cutoff, btype='high')
    elif filter_type == "Band-pass":
        b, a = butter(N, normalized_cutoff, btype='bandpass')
    elif filter_type == "Band-stop":
        b, a = butter(N, normalized_cutoff , btype='bandstop')
    elif filter_type == "Butterworth":
        b, a = butter(N, normalized_cutoff)
    elif filter_type == "Chebyshev I":
        b, a = cheby1(N, 1, normalized_cutoff)
    elif filter_type == "Chebyshev II":
        b, a = cheby2(N, 1, normalized_cutoff)
    elif filter_type == "Elliptic":
        b, a = ellip(N, 1, 1, normalized_cutoff)
    elif filter_type == "Bessel":
        b, a = bessel(N, normalized_cutoff, btype='low')  # Bessel doesn't have bandpass or bandstop
    else:
        raise ValueError("Unsupported filter type")

    # Apply the filter to the data
    filtered_data = lfilter(b, a, song_data)

    return filtered_data