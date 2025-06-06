from common.utils import createBase64Encode, createBase64Decode


class MODES:
    ENCRYPT = 0
    DECRYPT = 1


class KEYS:
    # fmt: off
    LS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    LS_MASK = [0x0000000000000000, 0x0000000000100001, 0x0000000000300003]
    MASK = [1 << i for i in range(64)]
    E = [
        31, 0, 1, 2, 3, 4, -1, -1,
        3, 4, 5, 6, 7, 8, -1, -1,
        7, 8, 9, 10, 11, 12, -1, -1,
        11, 12, 13, 14, 15, 16, -1, -1,
        15, 16, 17, 18, 19, 20, -1, -1,
        19, 20, 21, 22, 23, 24, -1, -1,
        23, 24, 25, 26, 27, 28, -1, -1,
        27, 28, 29, 30, 31, 30, -1, -1
    ]
    MATRIX_NS_BOX = [
        [
            14, 4, 3, 15, 2, 13, 5, 3, 13, 14, 6, 9, 11, 2, 0, 5, 4, 1, 10, 12, 15,
            6, 9, 10, 1, 8, 12, 7, 8, 11, 7, 0, 0, 15, 10, 5, 14, 4, 9, 10, 7, 8,
            12, 3, 13, 1, 3, 6, 15, 12, 6, 11, 2, 9, 5, 0, 4, 2, 11, 14, 1, 7, 8,
            13,
        ],
        [
            15, 0, 9, 5, 6, 10, 12, 9, 8, 7, 2, 12, 3, 13, 5, 2, 1, 14, 7, 8, 11, 4,
            0, 3, 14, 11, 13, 6, 4, 1, 10, 15, 3, 13, 12, 11, 15, 3, 6, 0, 4, 10, 1,
            7, 8, 4, 11, 14, 13, 8, 0, 6, 2, 15, 9, 5, 7, 1, 10, 12, 14, 2, 5, 9,
        ],
        [
            10, 13, 1, 11, 6, 8, 11, 5, 9, 4, 12, 2, 15, 3, 2, 14, 0, 6, 13, 1, 3,
            15, 4, 10, 14, 9, 7, 12, 5, 0, 8, 7, 13, 1, 2, 4, 3, 6, 12, 11, 0, 13,
            5, 14, 6, 8, 15, 2, 7, 10, 8, 15, 4, 9, 11, 5, 9, 0, 14, 3, 10, 7, 1,
            12,
        ],
        [
            7, 10, 1, 15, 0, 12, 11, 5, 14, 9, 8, 3, 9, 7, 4, 8, 13, 6, 2, 1, 6, 11,
            12, 2, 3, 0, 5, 14, 10, 13, 15, 4, 13, 3, 4, 9, 6, 10, 1, 12, 11, 0, 2,
            5, 0, 13, 14, 2, 8, 15, 7, 4, 15, 1, 10, 7, 5, 6, 12, 11, 3, 8, 9, 14,
        ],
        [
            2, 4, 8, 15, 7, 10, 13, 6, 4, 1, 3, 12, 11, 7, 14, 0, 12, 2, 5, 9, 10,
            13, 0, 3, 1, 11, 15, 5, 6, 8, 9, 14, 14, 11, 5, 6, 4, 1, 3, 10, 2, 12,
            15, 0, 13, 2, 8, 5, 11, 8, 0, 15, 7, 14, 9, 4, 12, 7, 10, 9, 1, 13, 6,
            3,
        ],
        [
            12, 9, 0, 7, 9, 2, 14, 1, 10, 15, 3, 4, 6, 12, 5, 11, 1, 14, 13, 0, 2,
            8, 7, 13, 15, 5, 4, 10, 8, 3, 11, 6, 10, 4, 6, 11, 7, 9, 0, 6, 4, 2, 13,
            1, 9, 15, 3, 8, 15, 3, 1, 14, 12, 5, 11, 0, 2, 12, 14, 7, 5, 10, 8, 13,
        ],
        [
            4, 1, 3, 10, 15, 12, 5, 0, 2, 11, 9, 6, 8, 7, 6, 9, 11, 4, 12, 15, 0, 3,
            10, 5, 14, 13, 7, 8, 13, 14, 1, 2, 13, 6, 14, 9, 4, 1, 2, 14, 11, 13, 5,
            0, 1, 10, 8, 3, 0, 11, 3, 5, 9, 4, 15, 2, 7, 8, 12, 15, 10, 7, 6, 12,
        ],
        [
            13, 7, 10, 0, 6, 9, 5, 15, 8, 4, 3, 10, 11, 14, 12, 5, 2, 11, 9, 6, 15,
            12, 0, 3, 4, 1, 14, 13, 1, 2, 7, 8, 1, 2, 12, 15, 10, 4, 0, 3, 13, 14,
            6, 9, 7, 8, 9, 6, 15, 1, 5, 12, 3, 10, 14, 5, 8, 7, 11, 0, 4, 13, 2, 11,
        ],
    ]
    P = [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24
    ]
    IP = [
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]
    IP_1 = [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24
    ]
    PC_1 = [
        56, 48, 40, 32, 24, 16, 8, 0,
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 60, 52, 44, 36,
        28, 20, 12, 4, 27, 19, 11, 3
    ]
    PC_2 = [
        13, 16, 10, 23, 0, 4, -1, -1,
        2, 27, 14, 5, 20, 9, -1, -1,
        22, 18, 11, 3, 25, 7, -1, -1,
        15, 6, 26, 19, 12, 1, -1, -1,
        40, 51, 30, 36, 46, 54, -1, -1,
        29, 39, 50, 44, 32, 47, -1, -1,
        43, 48, 38, 55, 33, 52, -1, -1,
        45, 41, 49, 35, 28, 31, -1, -1
    ]
    # fmt: on


class KuwoDes:
    key: bytes
    keyLength: int

    def __init__(self, key: bytes):
        self.key = key
        self.keyLength = len(key)

    def createBitTransform(self, array: list[int], length: int, source: int):
        bts = source
        dest = 0
        for bti in range(length):
            if array[bti] >= 0 and (bts & KEYS.MASK[array[bti]]) != 0:
                dest |= KEYS.MASK[bti]
        return dest

    def createDesSubKeys(self, key: int, mode: int):
        # PC-1 变换
        temp = self.createBitTransform(KEYS.PC_1, 56, key)
        K = [0] * 16
        for j in range(16):
            # 循环左移
            source = temp
            shift = KEYS.LS[j]
            temp = ((source & KEYS.LS_MASK[shift]) << (28 - shift)) | (
                (source & ~KEYS.LS_MASK[shift]) >> shift
            )
            K[j] = self.createBitTransform(KEYS.PC_2, 64, temp)
        if mode == MODES.DECRYPT:
            # 解密时反转子密钥顺序
            for j in range(8):
                K[j], K[15 - j] = K[15 - j], K[j]
        return K

    def createDes64(self, subkeys: list[int], data: int):
        # IP 变换
        out = self.createBitTransform(KEYS.IP, 64, data)
        pSource = [0, 0]
        pSource[0] = out & 0xFFFFFFFF
        pSource[1] = (out >> 32) & 0xFFFFFFFF

        for i in range(16):
            # F 变换开始
            R = pSource[1]
            # E 变换
            R = self.createBitTransform(KEYS.E, 64, R)
            # 与子密钥异或
            R ^= subkeys[i]
            # S盒变换
            pR = [0] * 8
            for k in range(8):
                pR[k] = (R >> (k * 8)) & 0xFF

            SOut = 0
            for sbi in range(7, -1, -1):
                SOut = (SOut << 4) | KEYS.MATRIX_NS_BOX[sbi][pR[sbi]]
            R = SOut
            # P 变换
            R = self.createBitTransform(KEYS.P, 32, R)
            L = pSource[0]
            pSource[0] = pSource[1]
            pSource[1] = L ^ R

        # 交换高低32位
        t = pSource[0]
        pSource[0] = pSource[1]
        pSource[1] = t

        out = ((pSource[1] & 0xFFFFFFFF) << 32) | (pSource[0] & 0xFFFFFFFF)
        # IP-1 变换
        out = self.createBitTransform(KEYS.IP_1, 64, out)

        return out

    def encrypt(self, content: bytes):
        contentLength = len(content)

        subKey = [0] * 16
        keyl = 0
        for i in range(8):
            keyl |= self.key[i] << (i * 8)
        subKey = self.createDesSubKeys(keyl, MODES.ENCRYPT)

        num = contentLength // 8
        pSrc = [0] * num
        for i in range(num):
            for j in range(8):
                pSrc[i] |= (content[i * 8 + j] & 0xFF) << (j * 8)
        pEncyrpt = [0] * (num + 1)
        for i in range(num):
            pEncyrpt[i] = self.createDes64(subKey, pSrc[i])

        tail_num = contentLength % 8
        szTail = content[num * 8 : contentLength]
        tail64 = 0
        for i in range(tail_num):
            tail64 |= (szTail[i] & 0xFF) << (i * 8)
        pEncyrpt[num] = self.createDes64(subKey, tail64)

        result = bytearray((num + 1) * 8)
        temp = 0
        for value in pEncyrpt:
            for j in range(8):
                result[temp] = (value >> (j * 8)) & 0xFF
                temp += 1

        return bytes(result)

    def decrypt(self, content: bytes):
        contentLength = len(content)

        subKey = [0] * 16
        keyl = 0
        for i in range(8):
            keyl |= self.key[i] << (i * 8)
        subKey = self.createDesSubKeys(keyl, MODES.DECRYPT)

        num = contentLength // 8
        encryptData = [0] * num
        for i in range(num):
            for j in range(8):
                encryptData[i] |= (content[i * 8 + j] & 0xFF) << (j * 8)
        planeData = [0] * num
        for i in range(num):
            planeData[i] = self.createDes64(subKey, encryptData[i])

        result = bytearray(num * 8)
        for i in range(num):
            for j in range(8):
                result[i * 8 + j] = (planeData[i] >> (j * 8)) & 0xFF

        return bytes(result).replace(b"\x00", b"")


SECRET_KEY = b"ylzsxkwm"

chiper = KuwoDes(SECRET_KEY)


def createEncrypt(content: str):
    encrypt = chiper.encrypt(bytes(content, encoding="utf-8"))
    return createBase64Encode(encrypt)


def createDecrypt(content: str):
    data = createBase64Decode(content)
    decrypt = chiper.decrypt(bytes(data))
    return decrypt.decode("utf-8")
