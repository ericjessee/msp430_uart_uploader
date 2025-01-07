def append_checksum(data):
    """
    Calculates the checksum for the given byte string and returns a new byte string
    with the checksum bytes (CKL and CKH) appended.

    Args:
        data (bytes): A byte string containing bytes B1 to Bn, excluding checksum bytes.

    Returns:
        bytes: A new byte string with CKL and CKH appended.
    """
    # Convert input byte string to a bytearray for mutability
    data_array = bytearray(data)

    # Initialize XOR accumulators for odd and even bytes
    ckl = 0  # XOR of bytes B1, B3, B5, ..., Bn-1
    ckh = 0  # XOR of bytes B2, B4, B6, ..., Bn

    # Iterate over the data, separating odd and even indexed bytes
    for i in range(len(data_array)):
        if i % 2 == 0:  # Odd-indexed bytes (0-based index corresponds to B1, B3, ...)
            ckl ^= data_array[i]
        else:           # Even-indexed bytes (0-based index corresponds to B2, B4, ...)
            ckh ^= data_array[i]

    # Invert the result (bitwise NOT and mask to 8 bits)
    ckl = ~ckl & 0xFF
    ckh = ~ckh & 0xFF

    # Append the checksum bytes to the data array
    data_array.append(ckl)  # CKL
    data_array.append(ckh)  # CKH

    # Convert back to a byte string and return
    return bytes(data_array)


def reverse_byte_order(data):
    """
    Reverses the byte order of the given bytes object.

    Args:
        data (bytes): The input byte string to reverse.

    Returns:
        bytes: A new byte string with the byte order reversed.
    """
    return data[::-1]