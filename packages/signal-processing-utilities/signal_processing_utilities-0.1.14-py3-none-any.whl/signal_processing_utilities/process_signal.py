"""This module is used to modify filters & remove the noise of the
raw data."""

# Imports
import numpy as np
import scipy.signal

from glob import glob
from scipy.signal import lfilter, butter
from collections import deque
import os


def identify_index_split(rle_locations_in_index_array, verbose=False):
    """This will identify where the rle_location values reset to a value
       that is below 65530.
    Args:
        rle_locations_in_index_array (list): This is a list of locations
                                             of values that are encoded
                                             in the index_array.

    Returns:
        split_indices (deque): This is a list of indices where the
                               values are reset in the
                               rle_locations_array.
    """
    split_indices = []
    for index, value in enumerate(rle_locations_in_index_array):
        if index == 0:
            prev_value = value
            continue
        if value > prev_value:
            prev_value = value
        else:
            if verbose:
                print(f"index: {index}")
                print(f"prev_value: {prev_value}")
                print(f"value: {value}")
            split_indices.append(index)
            prev_value = value
    return split_indices


def modify_filters(fft, freq_bins, percentage):
    """This function will filter the signal of the fast fourier
    transform by a percentage of the frequency with the maximum
    magnitude.

    Args:
        fft (numpy.ndarray): This is the fast fourier transform of an
                             audio waveform.
        freq_bins (numpy.ndarray): These are the bins of each frequency
                                   of the FFT.
        percentage (float): This is the percentage at which to filter
                            the FFT.

    Returns:
        numpy.ndarray: This is the filtered FFT which has each freqency
                       equal to or below the calculated threshold set to
                       zero.
    """
    threshold = percentage * (2 * np.abs(fft[0 : len(fft) // 2]) / len(freq_bins)).max()
    filtered_fft = fft.copy()
    filtered_fft_magnitude = np.abs(filtered_fft)
    filtered_fft_magnitude = 2 * filtered_fft_magnitude / len(freq_bins)
    filtered_fft[filtered_fft_magnitude <= threshold] = 0
    return filtered_fft


def preprocess_to_frequency_domain(raw_signal_array, sample_rate):
    """This method converts the signal from a raw signal to a
    preprocessed signal in the frequency domain. It will detrend the
    signal before returning the fast fourier transform of the detrended
    signal for further processing. This function serves as an
    intermediate preprocessing first step.

    Args:
        raw_signal_array (numpy.ndarray): This is the raw signal in
                                          numpy array format.
        sample_rate (int): This is the rate at which the data was
                           sampled.

    Returns:
        fft (numpy.ndarray): This is the transformed signal in the
                             frequency domain.
        freq_bins (numpy.ndarray): This is the bins of frequencies
                                pertaining to the fast fourier
                                transform.
    """
    detrended_signal = scipy.signal.detrend(raw_signal_array)
    fft = np.fft.fft(detrended_signal)
    freq_bins = np.arange(
        start=0, stop=(sample_rate // 2), step=(sample_rate / len(fft))
    )
    return fft, freq_bins


def identify_potential_initial_spikes(amplitude_array, return_local_maximum=True):
    """This function searches for peak amplitudes that may be initial
    neural spiking activity. This function is extended to filter the
    local maximum or minimum spiking activity. This is used to identify
    second or third spikes as well.

    Args:
        amplitude_array (numpy.ndarray): This contains an array of
                                         amplitudes of neural signal.
        return_local_maximum (bool, optional): This defines the logic of
                                               the returned values. If
                                               True, the values will be
                                               the local maximums of the
                                               amplitude array. When
                                               False,the returned list
                                               will be local minimums.

    Returns:
        list: This is a list of boolean values that indicate whether a
        point is a local maximum with respect to the next and previous
        amplitudes. If return_local_maximum is set to False, then the
        returned list contains information of local minimums instead.
    """
    if len(amplitude_array) < 3:
        if len(amplitude_array) == 0:
            return ValueError("Length of amplitude array must be greater than 0")
        elif len(amplitude_array) == 1:
            return [True]
        else:
            if return_local_maximum:
                if amplitude_array[0] < amplitude_array[1]:
                    return [False, True]
                else:
                    return [True, False]
            else:
                if amplitude_array[0] < amplitude_array[1]:
                    return [True, False]
                else:
                    return [False, True]
    else:
        if return_local_maximum:
            local_maximum_list = []
            for idx, val in enumerate(amplitude_array[0:-1]):
                if idx == 0:
                    if amplitude_array[idx + 1] < val:
                        local_maximum_list.append(True)
                    else:
                        local_maximum_list.append(False)
                    continue
                if (amplitude_array[idx - 1] < val) and (
                    val > amplitude_array[idx + 1]
                ):
                    local_maximum_list.append(True)
                else:
                    local_maximum_list.append(False)
            if amplitude_array[-1] > amplitude_array[-2]:
                local_maximum_list.append(True)
            else:
                local_maximum_list.append(False)
            return local_maximum_list
        else:
            local_minimum_list = []
            for idx, val in enumerate(amplitude_array[0:-1]):
                if idx == 0:
                    if amplitude_array[idx + 1] > val:
                        local_minimum_list.append(True)
                    else:
                        local_minimum_list.append(False)
                    continue
                if (amplitude_array[idx - 1] > val) and (
                    val < amplitude_array[idx + 1]
                ):
                    local_minimum_list.append(True)
                else:
                    local_minimum_list.append(False)
            if amplitude_array[-1] < amplitude_array[-2]:
                local_minimum_list.append(True)
            else:
                local_minimum_list.append(False)
            return local_minimum_list


def estimate_noise_floor(amplitude_array, window_size=10):
    """This function will estimate the noise floor. The amplitude array
    must be at least the length of the window size or a single value.

    Args:
        amplitude_array (numpy.ndarray): Array of amplitudes with which
                                         to derive the noise floor.

        window_size (int, optional): This is the width of the window
                                     used to calculate a rolling median
                                     average.

    Return:
        noise_floor_estimate (np.ndarray): This is the estimate of the
                                           noise floor.
    """
    if len(amplitude_array) == 0:
        raise ValueError("Length of amplitude array must be greater than 0")
    elif len(amplitude_array) == 1:
        noise_floor_estimate = np.array(
            [np.sqrt(np.abs(np.float64(amplitude_array[0])) ** 2)]
        )
        return noise_floor_estimate
    else:
        if len(amplitude_array) < window_size:
            window_size = len(amplitude_array)
        power_of_filtered_data = np.abs(np.float64(amplitude_array) ** 2)

        rolling_median_array = []
        for index in range(0, len(power_of_filtered_data), 1):
            current_median = np.median(
                power_of_filtered_data[index : index + window_size]
            )
            rolling_median_array.append(current_median)

        rolling_median_array = np.array(rolling_median_array)

        noise_floor_estimate = np.sqrt(rolling_median_array)

        return noise_floor_estimate


def detect_neural_spikes(neural_data, single_spike_detection=False):
    """This function detects spikes in real-time.
    It returns an array of spikes at specific times and amplitudes with
    zeroed out noise.

    Args:
        neural_data (array): This is the array of amplitudes for each
                             point of time of the neural data.
        single_spike_detection (bool): This is a boolean flag that
                                       indicates whether a single spike
                                       is to be returned. This will
                                       truncate the neural data to
                                       reflect only these detected
                                       amplitudes that correspond with
                                       the single detected spike.
    Returns:
        (list): This is the array inclusive of amplitudes of spikes at
                each specific point in the initial time array. Non-spike
                points have been replaced with amplitudes of zero value.
    """
    noise_floor_window = 5
    initial_first_point_of_spike_detected = False
    second_point_of_spike_detected = False
    third_point_of_spike_detected = False
    spike_train_time_index_list = []

    for current_time_index, value in enumerate(neural_data):
        # Estimate the noise floor
        if current_time_index < noise_floor_window:
            current_noise_floor_estimate_list = estimate_noise_floor(
                [neural_data[current_time_index]]
            )
        else:
            current_noise_floor_estimate_list = estimate_noise_floor(
                neural_data[
                    current_time_index - noise_floor_window : current_time_index
                ],
                window_size=noise_floor_window,
            )

        current_noise_floor_estimate = current_noise_floor_estimate_list[0]
        current_noise_floor_estimate_inverse = -(current_noise_floor_estimate)

        # Detect Initial First Point
        if initial_first_point_of_spike_detected == False:
            if current_time_index == 0:
                local_maximum_list_of_current_time_index = (
                    identify_potential_initial_spikes(
                        neural_data[current_time_index : current_time_index + 1]
                    )
                )
                is_current_time_index_local_maximum = (
                    local_maximum_list_of_current_time_index[0]
                )
            else:
                local_maximum_list_of_current_time_index = (
                    identify_potential_initial_spikes(
                        neural_data[current_time_index - 1 : current_time_index + 2]
                    )
                )
                is_current_time_index_local_maximum = (
                    local_maximum_list_of_current_time_index[1]
                )

            if is_current_time_index_local_maximum == True:
                # First Point Potentially Identified
                initial_first_point_of_spike_detected = True
                spike_time_index_first_point = current_time_index
        elif (
            second_point_of_spike_detected == False
            and initial_first_point_of_spike_detected == True
        ):
            # Detect Second Point
            local_minimum_list_of_current_time_index = (
                identify_potential_initial_spikes(
                    neural_data[current_time_index - 1 : current_time_index + 2],
                    return_local_maximum=False,
                )
            )
            is_current_time_index_local_minimum = (
                local_minimum_list_of_current_time_index[1]
            )
            if is_current_time_index_local_minimum == True:
                if (
                    neural_data[current_time_index]
                    < current_noise_floor_estimate_inverse
                ):
                    # Second Point Found
                    spike_time_index_list_first_to_second_points = np.arange(
                        start=spike_time_index_first_point,
                        stop=current_time_index,
                        step=1,
                    )
                    spike_time_index_second_point = current_time_index
                    second_point_of_spike_detected = True
                else:
                    initial_first_point_of_spike_detected = False
        elif (
            initial_first_point_of_spike_detected == True
            and second_point_of_spike_detected == True
            and third_point_of_spike_detected == False
        ):
            # Detect Third Point
            local_maximum_list_of_current_time_index = (
                identify_potential_initial_spikes(
                    neural_data[current_time_index - 1 : current_time_index + 2]
                )
            )
            is_current_time_index_local_maximum = (
                local_maximum_list_of_current_time_index[1]
            )
            if is_current_time_index_local_maximum == True:
                if neural_data[current_time_index] > current_noise_floor_estimate:
                    # Third Point Found
                    spike_time_index_list_second_to_third_points = np.arange(
                        spike_time_index_second_point,
                        current_time_index,
                        step=1,
                    )
                    third_point_of_spike_detected = True
                    time_index_of_most_recent_third_spike = current_time_index
                else:
                    initial_first_point_of_spike_detected = True
                    second_point_of_spike_detected = False
                    spike_time_index_first_point = current_time_index
        elif (
            initial_first_point_of_spike_detected == True
            and second_point_of_spike_detected == True
            and third_point_of_spike_detected == True
        ):
            # Detect Fourth Point
            if neural_data[current_time_index] < 0:
                time_index_of_most_recent_fourth_spike_point = current_time_index
                spike_time_index_list_third_to_fourth_points = np.arange(
                    time_index_of_most_recent_third_spike,
                    time_index_of_most_recent_fourth_spike_point
                    + 1,  # include the fourth detected point
                    step=1,
                )
                spike_time_index_list = np.concatenate(
                    [
                        spike_time_index_list_first_to_second_points,
                        spike_time_index_list_second_to_third_points,
                        spike_time_index_list_third_to_fourth_points,
                    ]
                )
                spike_train_time_index_list.append(spike_time_index_list)

                initial_first_point_of_spike_detected = False
                second_point_of_spike_detected = False
                third_point_of_spike_detected = False
                if single_spike_detection == True:
                    break
        else:
            raise ValueError("Error in Spike Detection State")
    if len(spike_time_index_list) > 0:
        return spike_train_time_index_list
    else:
        raise ValueError("No Detected Spikes")


def create_encoded_data(
    sample_rate,
    number_of_samples,
    spike_train_time_index_list,
    neural_data,
):
    """This function creates an encoded version of the initial data.

    Args:
        spike_train_time_index_list (list): This is the list of array of
                                            floats that indicate indices
                                            of amplitudes.
        neural_data (array): These are the amplitudes of all values in
                             the dataset.
        time_array_of_neural_data (array): These are the points of time
                                           of the dataset.
        sample_rate (int): This is the sample rate of the data. The
                              samples are equidistant depending upon the
                              sampling frequency as calculated from the
                              inverse of the sample rate.
        number_of_samples (int): This is the total number of samples in
                                 the dataset.

    Returns:
        encoded_data (list): This is the encoded data. This encoded data
                             has the sample rate, the number of samples,
                             the initial start time index of the first
                             amplitude, and the information of the
                             amplitudes of the detected eeg spikes.
                             This pattern of the initial time index
                             of the first amplitude, represented as an
                             int, followed by the number of points in
                             the detected spike, followed by the array
                             of amplitude values at each sample is
                             repeated for each detected spike. It is
                             implied that the samples are equidistant
                             depending upon the sampling frequency as
                             calculated from the inverse of the sample
                             rate, that the length of time of the entire
                             data is inferred from the number of samples
                             divided by the sample rate, and all
                             amplitudes at samples not explicitly
                             defined are to be considered noise and are
                             therefore set to zero to reduce size while
                             retaining information. The time of each
                             amplitude is calculated as the division of
                             the starting time index plus the current
                             position of each amplitude by the current
                             position in the zero-based amplitude array
                             by the sample rate.
    """
    encoded_data = []
    encoded_data.append(np.int32(sample_rate))
    encoded_data.append(np.int32(number_of_samples))
    for spike_train_index, spike_train_value in enumerate(spike_train_time_index_list):
        # Time index of the first spike point
        encoded_data.append(np.int32(spike_train_value[0]))
        # The number of points in the detected spike to decode the byte string.
        encoded_data.append(np.int32(len(neural_data[spike_train_value])))
        # The amplitude array of points in the spike.
        encoded_data.append(neural_data[spike_train_value])

    return encoded_data


def preprocess_signal(raw_neural_signal, sample_rate):
    """This function will process the raw neural signal by detrending
    then filtering the signal with a band-pass filter with a passband
    between 500 Hz and 5 KHz.

    Args:
        raw_neural_signal (ndarray): This is the array of amplitudes of
                                     a raw signal from the neuralink.
                                     This signal needs to be detrended
                                     and filtered to later extract the
                                     spike information contained within
                                     the signal.

    Returns:
        filtered_data_bandpass (ndarray): This is the array of the
                                          amplitude of the detrended,
                                          and band-pass filtered signal.
    """

    # Detrending the signal
    detrended_neural_data = np.int16(scipy.signal.detrend(raw_neural_signal))

    # Band-pass Filter
    nyq = sample_rate // 2
    low_cutoff_freq = 500
    high_cutoff_freq = 5000
    low = low_cutoff_freq / nyq
    high = high_cutoff_freq / nyq
    order = 4
    numerator, denominator = butter(order, [low, high], btype="band")

    filtered_data_bandpass = np.int16(
        lfilter(numerator, denominator, detrended_neural_data)
    )
    return filtered_data_bandpass


def decode_data(encoded_data):
    """This function will decode the encoded file. It will convert the
    encoded format into an array of values containing only the
    amplitudes of the neural spike activity and zero-values in lieu of
    noise.

    Args:
        encoded_data (deque): This is the encoded data. It is a list
        where the first index is the sample rate, & the second index is
        the number of samples. The subsequent pair of indices contain
        the starting time of the first spike amplitude and the array of
        the amplitude values of the spike. This pattern follows for each
        detected spike in the original data.

    Returns:
        amplitude_array (ndarray): This is the array of spike amplitudes
                                   detected in the original signal. The
                                   noise of the signal has been
                                   nullified.
        sample_rate (int): This is the rate of the sample.
    """

    # Extract Metadata
    encoded_data = deque(encoded_data)
    sample_rate = encoded_data.popleft()
    number_of_samples = encoded_data.popleft()

    # Construct the Time Array
    time_endpoint = number_of_samples / sample_rate
    time_array = np.arange(start=0, stop=time_endpoint, step=(1 / sample_rate))

    # Create the Amplitude Array
    amplitude_array = np.int16(np.zeros(len(time_array)))
    while len(encoded_data) > 0:
        amplitude_start_time_index = encoded_data.popleft()
        number_of_spike_points = encoded_data.popleft()
        spike_amplitudes = encoded_data.popleft()
        for amplitude_index, amplitude in enumerate(spike_amplitudes):
            amplitude_array[amplitude_start_time_index + amplitude_index] = amplitude
    return sample_rate, amplitude_array


def calculate_time_array(sample_rate: int, neural_data: np.ndarray):
    """This function creates the array of time values corresponding to
    the sample values in the raw_neural_data.

    Args:
        sample_rate (int): This is the rate the sample was taken.
        raw_neural_data (numpy.ndarray): This is the array of amplitudes.

    Returns:
        time_array_of_neural_data (numpy.ndarray): This is the array of
                                                   values where each
                                                   index corresponds to
                                                   the time width of the
                                                   frequency of the
                                                   sampling rate. The
                                                   frequency of the
                                                   sampling rate is
                                                   calculated as one
                                                   divided by the
                                                   sampling rate.
    """
    time_array_length = len(neural_data) / sample_rate
    time_array_of_neural_data = np.arange(
        start=0, stop=time_array_length, step=(1 / sample_rate)
    )
    return time_array_of_neural_data


def convert_encoded_data_to_byte_string(encoded_data: list):
    """This converts the encoded data to a string of bytes.

    Args:
        encoded_data (list): This is the array of values to be converted
                             into a string of bytes.

    Returns:
        encoded_data_byte_string (str): This is the string of bytes that
                                        represent the encoded data.
    """
    byte_string = encoded_data[0].tobytes()
    for data in encoded_data[1:]:
        byte_string += data.tobytes()

    return byte_string


def convert_byte_string_to_encoded_data(encoded_data_byte_string: str):
    """This converts the string of bytes to the encoded data
    representation of the input wav so that it may be decoded and
    assembled into an array of amplitudes.

    Args:
        encoded_data_byte_string (str): This is the string of bytes that
                                        represent the encoded data.
    Returns:
        encoded_data (list): This is the list of integers which contain
                             the spike information of the dissassembled
                             amplitude array.
    """
    encoded_data = []

    # Sample Rate:
    encoded_data.append(np.frombuffer(encoded_data_byte_string[0:4], dtype=np.int32)[0])
    encoded_data_byte_string = encoded_data_byte_string[4:]

    # Number of Samples:
    encoded_data.append(np.frombuffer(encoded_data_byte_string[0:4], dtype=np.int32)[0])
    encoded_data_byte_string = encoded_data_byte_string[4:]

    while len(encoded_data_byte_string) > 0:
        # Time index of first spike point:
        encoded_data.append(
            np.frombuffer(encoded_data_byte_string[0:4], dtype=np.int32)[0]
        )
        encoded_data_byte_string = encoded_data_byte_string[4:]

        # Number of points in the following spike amplitude array:
        number_of_points_in_the_spike_amplitude_array = np.frombuffer(
            encoded_data_byte_string[0:4], dtype=np.int32
        )[0]
        encoded_data.append(number_of_points_in_the_spike_amplitude_array)
        encoded_data_byte_string = encoded_data_byte_string[4:]

        # Array of spike amplitudes:
        encoded_data.append(
            np.frombuffer(
                encoded_data_byte_string[
                    0 : 2 * number_of_points_in_the_spike_amplitude_array
                ],
                dtype=np.int16,
            )
        )
        encoded_data_byte_string = encoded_data_byte_string[
            2 * number_of_points_in_the_spike_amplitude_array :
        ]

    return encoded_data


def print_size_of_file_compression(file_path: str, compressed_file_path: str):
    """This function prints the file size, the compressed file size, and
    the percent the file has been compressed.

    Args:
        file_path (str): This is the path of the original file.
        compressed_file_path (str): This is the path of the compressed
                                    file.
    """
    file_size = os.path.getsize(file_path)
    compressed_file_size = os.path.getsize(compressed_file_path)
    percent_of_compression = (1 - (compressed_file_size / file_size)) * 100
    file_size_requirement = file_size // 200
    percent_of_file_size_relative_to_file_size_requirement = (
        compressed_file_size / file_size_requirement
    ) * 100
    print(f"Original File Size: {file_size}")
    print(f"Compressed File Size: {compressed_file_size}")
    print(f"Percent of Compression: {percent_of_compression:.2f}%")
    print(f"Percent of Compressed File Size Relative to ", end="")
    print(f"Required File Size: ", end="")
    print(f"{percent_of_file_size_relative_to_file_size_requirement:.3f}%")


def print_time_each_function_takes_to_complete_processing(
    start_time: int, stop_time: int, executed_line: str = None, units: str = None
):
    """This function prints the time delta between the start time and
    the stop time.

    Args:
        start_time (int): This is the integer representation of the
                          start time in nanoseconds.
        stop_time (int): This is the integer representation of the stop
                         time in nanoseconds.
        executed_line (str, optional): This is the line of code that was
                                       executed. Defaults to None.
        units (str, optional): These are the units to be printed. If no
                               value is provided, nanoseconds,
                               milliseconds, microseconds, and
                               seconds are printed as the selected
                               units.
    """
    time_Δ = stop_time - start_time
    if executed_line != None:
        executed_line_str = "Executed Line: "
        executed_line_str += executed_line
        executed_line_str += "..."
        print(f"\n{executed_line_str}")
    else:
        print(f"\n")
    if units == None or units == "All":
        print(f"Time Δ Nanoseconds: {(time_Δ)}")
        print(f"Time Δ Microseconds: {(time_Δ / 1e3)}")
        print(f"Time Δ Milliseconds: {(time_Δ / 1e6)}")
        print(f"Time Δ Seconds: {(time_Δ / 1e9)}")
        print(f"\n")
    elif units == "ns":
        print(f"Time Δ Nanoseconds: {(time_Δ)}")
        print(f"\n")
    elif units == "μs":
        print(f"Time Δ Microseconds: {(time_Δ / 1e3)}")
        print(f"\n")
    elif units == "ms":
        print(f"Time Δ Milliseconds: {(time_Δ / 1e6)}")
        print(f"\n")
    elif units == "s":
        print(f"Time Δ Seconds: {(time_Δ / 1e9)}")
        print(f"\n")
    else:
        error_string = "Error: 'units' must be declared as one of the "
        +"following: All, ns, μs, ms, or s."
        raise ValueError(error_string)


def write_file_bytes(file_path: str, data_bytes: bytes):
    """This function will write the given data as bytes to the defined
       file path.

    Args:
        file_path (str): This is the path of the file to be read as
                         bytes.
        data_bytes (bytes): This is the string of bytes to be written to
                            a file.
    """
    with open(file_path, "wb+") as fp:
        fp.write(data_bytes)
        fp.close()


def read_file_bytes(file_path: str):
    """This function will read a file at the given path and return a
       string of bytes.

    Args:
        file_path (str): This is the path of the file to be read as
                         bytes.

    Returns:
        file_bytes (bytes): This is the string of bytes that represent
                            the file that was read.
    """
    with open(file_path, "rb") as fp:
        file_bytes = fp.read()
        fp.close()
    return file_bytes


def print_file_size(file_path: str):
    """This function prints the size of the given file in Bytes.

    Args:
        file_path (str): This is the path to the file to be
                                analyzed with respect to size in Bytes.

    Returns:
        file_size (int): this is the size of the file in Bytes.
    """
    file_size = os.path.getsize(file_path)
    print(f'File Name: "{os.path.basename(file_path)}".')
    print(f"Size: {file_size} Bytes.")
    return file_size


def decode_rle(
    index_array: list,
    rle_locations_in_index_array=[],
    use_rle_locations=False,
    UNSIGNED_INTEGER_CUTOFF_VALUE=65530,
):
    """This will expand the index array where the values have been
       compressed by run-length-encoding. If use_rle_locations is set to
       'False', then the index_array will be presumed to have a format of
       ['value', 'frequency', 'value', etc...]. A separate
       implementation is defined to parse this format. If
       use_rle_locations is set to 'True', then the
       rle_locations_in_index_array is non-optional and must be used as
       an input.

    Args:
        index_array (list): This is a list of values which contain
                            either signular values or run-length-encoded
                            values followed by the frequency of the
                            run-length-encoded value.
        rle_locations_in_index_array (list, optional): This is a list of
                              locations in the index_array where the
                              locations have been run-length-encoded.
                              The subsequent values of these locations
                              are frequencies of the run-length-encoded
                              values.

    Returns:
        reconstructed_array (list): This is the list of the original
                                    values before run-length-encoding
                                    was applied.
    """

    index = 0
    rle_index = 0
    rle_location = 0
    reconstructed_array = []

    if use_rle_locations:
        try:
            if rle_locations_in_index_array:
                # rle_locations_in_index_array exists
                pass
        except:
            error_string = (
                "rle_locations_in_index_array must be "
                + "declared when 'use_rle_locations' is set to 'True'."
            )
            raise NameError(error_string)
        rle_location_split_array = identify_index_split(rle_locations_in_index_array)
        current_rle_location_split_array_index = 0

        while rle_index < len(rle_locations_in_index_array):
            try:
                if (
                    rle_index
                    >= rle_location_split_array[current_rle_location_split_array_index]
                ):
                    current_rle_location_split_array_index += 1
            except:
                # This is an Index Location Error: the
                # rle_location_split_array contains indices that are
                # innermost boundaries within the
                # larger rle_locations_in_index_array array. That is to say,
                # the rle_locations_in_index_array
                # array will surpass the ultimate location in the
                # rle_location_split_array. The index of the
                # rle_location_split_array will not need to be incremented as
                # the index is being used as a scalar to scale the value of the
                # UNSIGNED_INTEGER_CUTOFF_VALUE to properly calculate the
                # rle_location in the index_array.
                pass

            rle_location = rle_locations_in_index_array[rle_index] + (
                current_rle_location_split_array_index * UNSIGNED_INTEGER_CUTOFF_VALUE
            )

            reconstructed_array.extend(index_array[index:(rle_location)])

            rle_index_of_value = rle_location
            rle_index_of_frequency = rle_location + 1

            expanded_rle_value = [
                index_array[rle_index_of_value]
                for frequency in range(index_array[rle_index_of_frequency])
            ]

            reconstructed_array.extend(expanded_rle_value)
            index = rle_index_of_value + 2
            rle_index += 1

        reconstructed_array.extend(index_array[index:])
        return reconstructed_array
    else:
        while index < len(index_array):
            reconstructed_array.extend(
                [index_array[index] for value in range(index_array[index + 1])]
            )
            index += 2
        return reconstructed_array


def encode_rle(
    original_data_list: list,
    use_rle_locations=False,
    UNSIGNED_INTEGER_CUTOFF_VALUE=65530,
):
    """This algorithm will search for contiguous values within the
       array. When the number_of_values_apriori_in_index_array is
       greater than the value 65530, the count is reduced by this value
       in order to prevent an overflow of an unsigned 16-bit integer.
       This allows for the data to be stored with 2 bytes when the
       format of the array is a known value in advance of decoding this
       format. The choice of integer 65530 is an arbitrary value less
       than that of the maximum value of an unsigned 16-bit integer
       (65536). In this body of work, the value 65530 is denoted as the
       UNSIGNED_INTEGER_CUTOFF_VALUE.

    Args:
        original_data_list (list): This is a list of integer values to
                                   be encoded.
        use_rle_locations (bool, optional): This is a flag which
                                            indicates whether a
                                            locations array will be
                                            implemented to identify
                                            where the run-length-encoded
                                            values exist within the
                                            compressed array. This is
                                            because the compressed array
                                            in this mode will not
                                            contain run-length-encoded
                                            values for values that have
                                            singular representations.

    Returns:
        index_array (list): This is the list of run length encoded
                            values.
        rle_locations_in_index_array (list): This is a list of locations
                                             of elements that are
                                             repeated that are present
                                             in the array of indices.
    """
    initial_index = 0
    second_index = 1
    frequency = 0
    index_array = []
    rle_locations_in_index_array = []
    number_of_values_apriori_in_index_array = 0

    while second_index < len(original_data_list):
        if original_data_list[initial_index] == original_data_list[second_index]:
            index_array.append(original_data_list[initial_index])
            if use_rle_locations:
                rle_locations_in_index_array.append(
                    number_of_values_apriori_in_index_array
                )
            frequency += 1  # This accounts for the first detected value.

            # continue searching the breadth of the array; increasing
            # the detected frequency of the value. This will break out
            # of the while loop when the first & second indices are not
            # equal. ∴, the first value will not be accounted for
            # because the while loop will be broken where the value
            # would have been incremented.
            while (
                second_index < len(original_data_list)
                and original_data_list[initial_index]
                == original_data_list[second_index]
            ):
                frequency += 1
                second_index += 1
            index_array.append(frequency)
            if use_rle_locations:
                if (
                    number_of_values_apriori_in_index_array
                    > UNSIGNED_INTEGER_CUTOFF_VALUE
                ):
                    number_of_values_apriori_in_index_array -= (
                        UNSIGNED_INTEGER_CUTOFF_VALUE
                    )
                # The code below is to skip over the indices that contain
                # the run-length-encoded value and the frequency of that
                # value.
                number_of_values_apriori_in_index_array += 2
        else:
            index_array.append(original_data_list[initial_index])
            if use_rle_locations:
                if (
                    number_of_values_apriori_in_index_array
                    > UNSIGNED_INTEGER_CUTOFF_VALUE
                ):
                    number_of_values_apriori_in_index_array -= (
                        UNSIGNED_INTEGER_CUTOFF_VALUE
                    )
            # The code below is to skip over the index that contains an
            # individual run-length-encoded value.
            if use_rle_locations:
                number_of_values_apriori_in_index_array += 1
            else:
                index_array.append(1)
        frequency = 0
        initial_index = second_index
        second_index += 1
    if original_data_list[-1] != index_array[-2]:
        index_array.append(original_data_list[-1])
        if use_rle_locations == False:
            index_array.append(1)
    return index_array, rle_locations_in_index_array


# RLE for bit compression
def rle_bit_compression(byte_string: bytes, compress=True, rle_locations=None):
    """This function will compress the byte string using
    run-length-encoding. It will create a rle_locations byte string to
    differentiate between frequency and value locations. When compress
    is set to true, rle_locations is non-optional. The return value
    established when compress is set to true is the expected input.
    This is labeled "rle_locations_compressed_byte_string". If
    "compress" is set to "False", the return values are the byte
    string object of the original byte_string input and the
    rle_locations as a list of integers. The rle_locations can be
    safely ignored.

    Args:
        byte_string (bytes): This is a bytes object of 0 and 1 values.
        compress (bool, optional): This is a flag to indicate if mode
                                   is to compress or decompress.
                                   Defaults to True.
        rle_locations (_type_, optional): These are the rle_locations
                                          that are used when
                                          decompressing. If "compress"
                                          is equal to "True", then this
                                          can safely be set to "None".
                                          Otherwise, this is a mandatory
                                          input. Defaults to None.

    Returns:
        rle_compressed_bytes (bytes): This is a byte string object of
                                       the compressed byte_string.
        rle_locations_compressed_byte_string (bytes): This is a
                                                      compressed byte
                                                      string object of
                                                      the rle_locations.
    """
    if compress:
        byte_string_str = str(byte_string).lstrip("b'").rstrip("'")
        # Convert byte string to string of bits

        initial_index = 0
        second_index = 1
        frequency = 0
        rle_compression = []
        rle_locations = []

        # RLE compessing the byte_string_str
        while second_index < len(byte_string_str):
            if byte_string_str[initial_index] == byte_string_str[second_index]:
                rle_compression.append(str(byte_string_str[initial_index]))
                frequency += 1
                while byte_string_str[initial_index] == byte_string_str[second_index]:
                    second_index += 1
                    frequency += 1
                    if second_index >= len(byte_string_str):
                        break
                rle_compression.append(str(frequency))
            else:
                rle_compression.append(byte_string_str[initial_index])
                rle_compression.append("x")
            frequency = 0
            initial_index = second_index
            second_index += 1
        # Accounting for the case of the frequency
        #   byte_string_str[second_index] not being accounted for if it
        #   is a unique value.
        # If non-unique, this will be handled by the frequency in the
        #   second while loop. Otherwise the second_index will be
        #   larger than the length of the byte_string_str, and the
        #   frequency of the individual value must be declared.

        if byte_string_str[-2] != byte_string_str[-1]:
            if rle_compression[-1] != "x":  # Redundancy to prevent error
                rle_compression.append("x")

        # verify rle_compression has captured all values:
        total = 0
        for index in range(0, len(rle_compression), 2):
            if rle_compression[index + 1] == "x":
                total += 1
            else:
                total = total + int(rle_compression[index + 1])

        # RLE locations array run-length-encoded compression:
        # -1 signifies the start of a run-length-encoding.
        # Otherwise the value is written individually.

        # Establishing RLE Locations
        for index in range(0, len(rle_compression)):
            rle_locations.append(len(rle_compression[index]))

        # Compression of RLE Locations
        initial_index = 0
        second_index = 1
        frequency = 0
        rle_locations_compressed = []
        while second_index < len(rle_locations):
            if rle_locations[initial_index] == rle_locations[second_index]:
                rle_locations_compressed.append(-1)
                rle_locations_compressed.append(rle_locations[initial_index])
                frequency += 1
                while rle_locations[initial_index] == rle_locations[second_index]:
                    second_index += 1
                    frequency += 1
                    if second_index >= len(rle_locations):
                        break
                rle_locations_compressed.append(frequency)
            else:
                rle_locations_compressed.append(rle_locations[initial_index])
            frequency = 0
            initial_index = second_index
            second_index += 1
        if rle_locations[-2] != rle_locations[-1]:
            rle_locations_compressed.append(rle_locations[-1])

        # RLE Locations Compressed to Byte String:
        rle_locations_compressed_byte_string_l = [
            rle_locations_compressed[index].to_bytes(2, "big", signed=True)
            for index in range(len(rle_locations_compressed))
        ]
        rle_locations_compressed_byte_string = b""
        for byte in rle_locations_compressed_byte_string_l:
            rle_locations_compressed_byte_string += byte

        rle_compression_join = "".join(rle_compression)
        rle_compressed_bytes = bytes(rle_compression_join, encoding="utf-8")

        return rle_compressed_bytes, rle_locations_compressed_byte_string
    else:
        rle_compressed_bytes = byte_string
        rle_locations_compressed_byte_string = rle_locations
        # RLE Locations Compressed Byte String Expansion:
        # int.from_bytes(, signed=True)
        rle_locations_compressed_byte_string_l = [
            rle_locations_compressed_byte_string[index : index + 2]
            for index in range(len(rle_locations_compressed_byte_string))
        ]

        rle_locations_compressed = []
        for index in range(0, len(rle_locations_compressed_byte_string_l), 2):
            rle_locations_compressed.append(
                int.from_bytes(
                    rle_locations_compressed_byte_string_l[index], signed=True
                )
            )

        # Expansion of RLE Locations Compressed:
        rle_locations = []
        index = 0
        # rle_locations appears to have locations and rle_compression
        # This is causing an error.
        while index < len(rle_locations_compressed):
            if rle_locations_compressed[index] != -1:
                rle_locations.append(rle_locations_compressed[index])
                index += 1
            else:
                index += 1
                rle_expanded_value_l = []
                rle_value = rle_locations_compressed[index]
                rle_value_frequency = rle_locations_compressed[index + 1]
                rle_expanded_value_l = [
                    rle_value for index in range(rle_value_frequency)
                ]
                rle_locations.extend(rle_expanded_value_l)
                index += 2

        # Original Byte Expansion
        rle_compressed_bytes_index = 0
        rle_location_index = 0
        rle_compressed_str_l = []

        while rle_location_index < len(rle_locations):
            rle_compressed_str = (
                str(
                    rle_compressed_bytes[
                        rle_compressed_bytes_index : rle_compressed_bytes_index
                        + rle_locations[rle_location_index]
                    ],
                )
                .lstrip("b'")
                .rstrip("'")
            )
            rle_compressed_str_l.append(rle_compressed_str)

            rle_compressed_bytes_index += rle_locations[rle_location_index]
            rle_location_index += 1

        # Expand rle_compressed_int_l to a string
        byte_string_str = ""
        index = 0
        while index < len(rle_compressed_str_l):
            byte_string_str_subset_value = rle_compressed_str_l[index]
            byte_string_str_subset_value_frequency = rle_compressed_str_l[index + 1]
            if byte_string_str_subset_value_frequency != "x":
                byte_string_str_subset_l = [
                    byte_string_str_subset_value
                    for value in range(int(byte_string_str_subset_value_frequency))
                ]
                byte_string_str_subset_str = "".join(byte_string_str_subset_l)
                byte_string_str += byte_string_str_subset_str
                index += 2
            else:
                byte_string_str += byte_string_str_subset_value
                index += 2

        # Convert String type to original byte string
        byte_string = bytes(byte_string_str, encoding="utf-8")
        return byte_string, rle_locations


def compare_compression_ratio(
    original_data, compressed_data: bytes, method: str = None
):
    """This function prints the compression ratio of two byte strings.

    Args:
        original_data (numpy.ndarray): This is the array of amplitudes before
                              compression.
        compressed_data (bytes): This is the compressed representation of
                               the amplitudes after the method of
                               compression has been applied.
        method (str):  This is the string representing the method of
                       compression. Defaults to None.
    """
    percent_compression = (
        1 - (len(compressed_data) / len(original_data.tobytes()))
    ) * 100
    if method != None:
        print(f"\nMethod of Compression: {method}")
    else:
        print("\n")
    print(f"Initial file size: {len(original_data.tobytes())} bytes.")
    print(f"Compressed File Size: {len(compressed_data)} bytes.")
    print(f"Percent of Compression: {percent_compression:.2f}%")
    print(f"\n")


def print_compression_efficiency_metrics_wrapper(
    original_data,
    compressed_data: bytes,
    start_time: int,
    stop_time: int,
    method: str,
):
    """This is a wrapper function to print the start and stop times as
       well as the ratio of compression. The compressed file may be the
       output compressed string of bytes.

    Args:
        file (numpy.ndarray): This is the array of amplitudes before compression
        compressed_file (bytes): This is the compressed representation of
                               the amplitudes after the method of
                               compression has been applied.
        start_time (int): This is the initial starting time in
                          nanoseconds.
        stop_time (int): This is the final time in nanoseconds of the
                         chosen method of compression.
        method (str): This is the string representing the
                                method of compression.
    """
    compare_compression_ratio(
        original_data=original_data, compressed_data=compressed_data, method=method
    )
    print_time_each_function_takes_to_complete_processing(
        start_time=start_time, stop_time=stop_time, executed_line=method
    )
