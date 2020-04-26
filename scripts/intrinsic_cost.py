G_DATA_ZERO = 4
G_DATA_NONZERO = 68
G_TRANSACTION = 2100

BYTE_IN_HEX = 2


def main():
    data = str(input('please enter the value of the data field as hex string: '))
    byte_list = [data[i:i+BYTE_IN_HEX]
                 for i in range(0, len(data), BYTE_IN_HEX)]

    gzero = G_TRANSACTION
    for byte in byte_list:
        if len(byte) != 2:
            raise ValueError('{} not a byte'.format(byte))

        if byte == '00':
            gzero += G_DATA_ZERO
        else:
            gzero += G_DATA_NONZERO

    print('intrinsic cost: {}'.format(gzero))


if __name__ == '__main__':
    main()
