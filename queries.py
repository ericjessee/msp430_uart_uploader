from checksum import append_checksum

CMD_RX_DATA_BLOCK = 0x12
CMD_RX_PWD = 0x10
CMD_MASS_ERASE = 0x18
CMD_LOAD_PC = 0x1A
CMD_TX_DAT = 0x14
CMD_TX_BSL_VER = 0x1e

header_char = 0x80
ack_char = 0x90
ver_query_msg = append_checksum(bytearray(b'\x80\x1e\x04\x04\xde\xad\xbe\xef'))
mass_erase_cmd = append_checksum(bytearray([header_char, CMD_MASS_ERASE, 0x04, 0x04, 0xbe, 0xef, 0x06, 0xa5]))

def password_unlock_cmd(password):
    msg = bytearray([header_char, CMD_RX_PWD, 0x24, 0x24, 0xde, 0xad, 0xbe, 0xef])
    for byte in password:
        msg.append(byte)
    return append_checksum(msg)

def read_mem_query(address, length):
    AL = address[1]
    AH = address[0]
    LL = length
    LH = 0
    msg = bytearray([header_char, CMD_TX_DAT, 0x04, 0x04, AL, AH, LL, LH])
    return append_checksum(msg)

def write_mem_cmd(address, data):
    L1 = len(data)+4
    L2 = L1
    AL = address[1]
    AH = address[0]
    LL = len(data)
    LH = 0
    msg = bytearray([header_char, CMD_RX_DATA_BLOCK, L1, L2, AL, AH, LL, LH])
    for byte in data:
        msg.append(byte)
    return append_checksum(msg)

def load_pc_cmd(address):
    L1 = 0x04
    L2 = 0x04
    AL = address[1]
    AH = address[0]
    LL = 0xbe
    LH = 0xef
    msg = bytearray([header_char, CMD_LOAD_PC, L1, L2, AL, AH, LL, LH])
    return append_checksum(msg)
