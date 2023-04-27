#==============================================================================
def matrixToString(matrix):
    strResult=''
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            strResult+=str(matrix[i][j])
    return strResult
#==============================================================================
# Đổi hexa sang nhị phân:
def hexaToBin(string_64bit_hexa): # 16 chữ cái (0->15) => list<string>
    dictionary = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
                  '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011',
                  'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'}
    result = [] # Ma trận 8x8
    for x in range(0, 16, 2): # 0 2 4 6 ... 14
        # Chuyển giá trị của input[x] và input[x+1] thành chuỗi 8 bits
        _str = dictionary[string_64bit_hexa[x]] + dictionary[string_64bit_hexa[x+1]]
        result.append(_str)
    return result
#==============================================================================
# Đổi bin sang hex:
def binToHex(str_bin_64bits): # str -> str
    dic = {
        '0000':'0', '0001':'1', '0010':'2', '0011':'3', '0100':'4', '0101':'5',
        '0110':'6', '0111':'7', '1000':'8', '1001':'9', '1010':'A', '1011':'B',
        '1100':'C', '1101':'D', '1110':'E', '1111':'F'
        }
    str_hex_64bits = ''
    for i in range(0, len(str_bin_64bits), 4):
        str_hex_64bits+=dic[str_bin_64bits[i:i+4]]
    return str_hex_64bits
#==============================================================================
def IP(string_64bit_hexa): # return (8x8)
    #Bang IP
    IP = [
          [58, 50, 42, 34, 26, 18, 10,  2],
          [60, 52, 44, 36, 28, 20, 12,  4],
          [62, 54, 46, 38, 30, 22, 14,  6],
          [64, 56, 48, 40, 32, 24, 16,  8],
          [57, 49, 41, 33, 25, 17,  9,  1],
          [59, 51, 43, 35, 27, 19, 11,  3],
          [61, 53, 45, 37, 29, 21, 13,  5],
          [63, 55, 47, 39, 31, 23, 15,  7]
          ]
    #Chuyển chuỗi hexa thành matrix binary
    matrix_binary = hexaToBin(string_64bit_hexa)
    #Xếp các bit từ input vào vị trí phù hợp trong IP
    for i in range(8):
        for j in range(8):
            # Vì các vị trí trong IP đánh số từ 1
            x = IP[i][j]-1
            # Thay thế bit tại vị trí x trong input vào IP
            hang = x//8
            cot = x%8
            IP[i][j] = matrix_binary[hang][cot]
    return IP # (8x8)

# Cách khác:
'''
# Quyt luật IP, viết từ dưới lên trên thành hàng ngang, chỉ số từ 0
# Viết các cột: 1 -> 3 -> 5 -> 7 -> 0 -> 2 -> 4 -> 6

result = []
# Đưa các cột chỉ số lẻ vào list
for j in range(4):  # {0, 1, 2, 3}
    j = 2*j+1       # {1, 3, 5, 7}
    hang = []
    for i in range(7, -1, -1):  # {7, 6, 5, 4, 3, 2, 1, 0}
        hang.append(matrix_binary[i][j])
    result.append(hang)
# Đưa các cột chỉ số chẵn vào list
for j in range(4):  # {0, 1, 2, 3}
    j = 2*j      # {0 -> 2 -> 4 -> 6}
    hang = []
    for i in range(7, -1, -1):  # {7, 6, 5, 4, 3, 2, 1, 0}
        hang.append(matrix_binary[i][j])
    result.append(hang)
'''
#==============================================================================
# Tách matrix_binary 64 bits thành 2 matrix_binary con L 32bit, R 32bit
def SPLIT(matrix_binary_IP):
    L = matrix_binary_IP[0:4]
    R = matrix_binary_IP[4:]
    return L, R # (4x8)
#==============================================================================
#Hàm mở rộng E (matrix_binary 32bits -> matrix_binary 48 bits)
def E(matrix_binary_R): #(4x8) => (8x6)
    # Ma trận mẫu 48 bits (8x6)
    matrix_binary_E = [[' ' for cot in range(6)] for hang in range(8)]
    #Chuyển matrix_binary input (4x8) thành (8x4)
    matrix_binary_8x4 = []
    for _8bits in matrix_binary_R:
        matrix_binary_8x4.append(_8bits[0:4])# 4 bits đầu
        matrix_binary_8x4.append(_8bits[4:8])# 4 bits sau
    #Xếp matrix_binary_8x4 vào vị trí thích hợp của matrix_binary_E
    for i in range(8):
        for j in range(1,5):# 1->4
            matrix_binary_E[i][j] = matrix_binary_8x4[i][j-1]
    #Điền thêm 2 cột ở 2 bên matrix_binary_E:
    for hang in range(8):
        #Điền cột 0
        matrix_binary_E[hang][0] = (matrix_binary_E[7][4] if hang==0 else matrix_binary_E[hang-1][4])
        #Điền cột 5
        matrix_binary_E[hang][5] = (matrix_binary_E[0][1] if hang==7 else matrix_binary_E[hang+1][1])
    '''
    print('In ma trận E')
    for x in matrix_binary_E:
        print(*x)
    '''
    return matrix_binary_E # (8x6)
#==============================================================================
def XOR_48bits(matrix_binary_E, matrix_binary_Key): #(8x6) XOR (6x8)
    #Chuyển matrix_binary thành string
    strE = matrixToString(matrix_binary_E)
    strKey=matrixToString(matrix_binary_Key)
    strResult = ""
    
    # strE XOR strKey
    for i in range(len(strE)):
        strResult += ('0' if strE[i]==strKey[i] else '1')
    #Đưa strResult thành matrix_binary (8x6) để thuận tiện cho Sbox
    matrix_binary_XOR = [[' ' for cot in range(6)] for hang in range(8) ]
    for hang in range(8):
        for cot in range(6):
            matrix_binary_XOR[hang][cot] = strResult[hang*6+cot]
    '''
    print('In ma trận XOR')
    for x in matrix_binary_XOR:
        print(*x)
    '''
    return matrix_binary_XOR #(8x6)
#==============================================================================
# Đổi nhị phân sang thập phân:
def binToDec(str_bin): # str -> int
    # bậc của đa thức:
    bac = len(str_bin)-1 # trừ 1 vì số cuối mũ 0
    result = 0
    for a in str_bin:
        result = result + (int(a) * (2**bac) )# tong += a x 2^bac
        bac = bac-1
    return result # int
# Đổi thập phân sang nhị phân:
def decToBin(_input): # int -> str
    # Chia lấy dư cho 2, rồi viết ngược lại
    lstSoDu = []
    while _input>0:
        lstSoDu.append(_input%2)
        _input = _input//2
    lstResult = lstSoDu[::-1] # Đảo ngược list
    # Chuyển list thành string
    str_bin = ''
    for a in lstResult:
        str_bin += str(a)
    return str_bin
#==============================================================================
def SBOX(matrix_binary_XOR): #(8x6) -> (4x8)
    # Khai báo 8 Sbox
    lstSBox = [
        #Sbox1
        [
            [14, 4,13, 1, 2,15,11, 8, 3,10, 6,12, 5, 9, 0, 7],
            [ 0,15, 7, 4,14, 2,13, 1,10, 6,12,11, 9, 5, 3, 8],
            [ 4, 1,14, 8,13, 6, 2,11,15,12, 9, 7, 3,10, 5, 0],
            [15,12, 8, 2, 4, 9, 1, 7, 5,11, 3,14,10, 0, 6,13]
        ],
        #Sbox2
        [
            [15, 1, 8,14, 6,11, 3, 4, 9, 7, 2,13,12, 0, 5,10],
            [ 3,13, 4, 7,15, 2, 8,14,12, 0, 1,10, 6, 9,11, 5],
            [ 0,14, 7,11,10, 4,13, 1, 5, 8,12, 6, 9, 3, 2,15],
            [13, 8,10, 1, 3,15, 4, 2,11, 6, 7,12, 0, 5,14, 9]
        ],
        #Sbox3
        [
            [10, 0, 9,14, 6, 3,15, 5, 1,13,12, 7,11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6,10, 2, 8, 5,14,12,11,15, 1],
            [13, 6, 4, 9, 8,15, 3, 0,11, 1, 2,12, 5,10,14, 7],
            [ 1,10,13, 0, 6, 9, 8, 7, 4,15,14, 3,11, 5, 2,12]
        ],
        #Sbox4
        [
            [ 7,13,14, 3, 0, 6, 9,10, 1, 2, 8, 5,11,12, 4,15],
            [13, 8,11, 5, 6,15, 0, 3, 4, 7, 2,12, 1,10,14, 9],
            [10, 6, 9, 0,12,11, 7,13,15, 1, 3,14, 5, 2, 8, 4],
            [ 3,15, 0, 6,10, 1,13, 8, 9, 4, 5,11,12, 7, 2,14]
        ],
        #Sbox5
        [
            [ 2,12, 4, 1, 7,10,11, 6, 8, 5, 3,15,13, 0,14, 9],
            [14,11, 2,12, 4, 7,13, 1, 5, 0,15,10, 3, 9, 8, 6],
            [ 4, 2, 1,11,10,13, 7, 8,15, 9,12, 5, 6, 3, 0,14],
            [11, 8,12, 7, 1,14, 2,13, 6,15, 0, 9,10, 4, 5, 3]
        ],
        #Sbox6
        [
            [12, 1,10,15, 9, 2, 6, 8, 0,13, 3, 4,14, 7, 5,11],
            [10,15, 4, 2, 7,12, 9, 5, 6, 1,13,14, 0,11, 3, 8],
            [ 9,14,15, 5, 2, 8,12, 3, 7, 0, 4,10, 1,13,11, 6],
            [ 4, 3, 2,12, 9, 5,15,10,11,14, 1, 7, 6, 0, 8,13]
        ],
        #Sbox7
        [
            [ 4,11, 2,14,15, 0, 8,13, 3,12, 9, 7, 5,10, 6, 1],
            [13, 0,11, 7, 4, 9, 1,10,14, 3, 5,12, 2,15, 8, 6],
            [ 1, 4,11,13,12, 3, 7,14,10,15, 6, 8, 0, 5, 9, 2],
            [ 6,11,13, 8, 1, 4,10, 7, 9, 5, 0,15,14, 2, 3,12]
        ],
        #Sbox8
        [
            [13, 2, 8, 4, 6,15,11, 1,10, 9, 3,14, 5, 0,12, 7],
            [ 1,15,13, 8,10, 3, 7, 4,12, 5, 6,11, 0,14, 9, 2],
            [ 7,11, 4, 1, 9,12,14, 2, 0, 6,10,13,15, 3, 5, 8],
            [ 2, 1,14, 7, 4,10, 8,13,15,12, 9, 0, 3, 5, 6,11]
        ]
        ]
    str_Result = ''

    # Tra bảng
    for i in range(8): # 0 1 .. 7
        #Lấy 6 bit:
        _6bits = matrix_binary_XOR[i]

        #Bước 1: Lấy bit đầu-cuối thành hàng, 4 bit giữa thành cột
        bin_hang = str(_6bits[0]) + str(_6bits[-1])
        
        # map để chuyển mỗi phần tử thành str
        # join để chuyển 1 list<string> thành 1 string
        bin_cot  = "".join(map(str, _6bits[1:5]))
        
        # Bước 2: chuyển hàng, cột sang thập phân
        dec_hang = binToDec(bin_hang)
        dec_cot  = binToDec(bin_cot)

        # Bước 3: Tra bảng sbox thứ i trong lstSBox -> int:
        dec_ketQua = lstSBox[i][dec_hang][dec_cot]
        # Bước 4: Chuyển kết quả về 4bits nhị phân và nối vào str_Result:
        str_bin_ketQua=decToBin(dec_ketQua)
        # Vì str_bin_ketQua có thể không đủ 4bits, cần thêm các bit 0 khi nối vào str_Result
        str_4bits_Result=''
        if len(str_bin_ketQua)==0:
            str_4bits_Result = '0000'
        elif len(str_bin_ketQua)==1:
            str_4bits_Result = '000'+str_bin_ketQua
        elif len(str_bin_ketQua)==2:
            str_4bits_Result = '00'+str_bin_ketQua
        elif len(str_bin_ketQua)==3:
            str_4bits_Result = '0'+str_bin_ketQua
        else: str_4bits_Result = str_bin_ketQua
        str_Result = str_Result + str_4bits_Result

    #print('Chuỗi kết quả sbox:'+str_Result)

    # Chuyển string -> matrix_binary (4x8)
    matrix_binary_SBox = [['' for cot in range(8)] for hang in range(4)]
    for i in range(4):
        for j in range(8):
            matrix_binary_SBox[i][j] = str_Result[8*i + j]
    '''
    print('In ma trận SBox')
    for x in matrix_binary_SBox:
        print(*x)
    '''
    return matrix_binary_SBox # (4x8)
#==============================================================================
# Hoán vị P
def P(matrix_binary_SBox): # (4x8) -> (4x8)
    P=[
       [16, 7,20,21,29,12,28,17],
       [ 1,15,23,26, 5,18,31,10],
       [ 2, 8,24,14,32,27, 3, 9],
       [19,13,30, 6,22,11, 4,25]
       ]
    #Xếp các bit ở matrix_binary_SBox vào vị trí phù hợp trong P
    for i in range(4):
        for j in range(8):
            a = P[i][j]-1 # vì index từ 0
            P[i][j] = matrix_binary_SBox[a//8][a%8]
    
    #print('P='+ binToHex(matrixToString(P)))
    return P # (4x8)
#==============================================================================
def XOR_32bits(matrix_binary_L,matrix_binary_P): # (4x8) xor (4x8) -> (4x8)
    # for hang in range(len(matrix_binary_L)):
    #     # Phép xor trong python '^'
    #     matrix_binary_L[hang] = [(int(x) ^ int(y)) for x, y in zip(matrix_binary_L[hang], matrix_binary_P[hang])]
    for i in range(4):
        for j in range(8):
            matrix_binary_L[i][j] = ('0' if int(matrix_binary_L[i][j])==int(matrix_binary_P[i][j]) else '1')

    return matrix_binary_L # (4x8)
#==============================================================================
def IP_1(matrix_binary_R, matrix_binary_L):#(4x8)^(4x8) => string 64bits
# Cách 1:Viết theo quy luật
# Quyt luật IP-1, viết các cột theo chiều từ phải sang trái, với hàng có chỉ số
# 4-0-5-1-6-2-7-3

#Cách 2:
    # Tạo matrix_binary_R (8x8)
    for i in range(4):
        matrix_binary_R.append(matrix_binary_L[i])

    IP_1 = [
        [40, 8,48,16,56,24,64,32],
        [39, 7,47,15,55,23,63,31],
        [38, 6,46,14,54,22,62,30],
        [37, 5,45,13,53,21,61,29],
        [36, 4,44,12,52,20,60,28],
        [35, 3,43,11,51,19,59,27],
        [34, 2,42,10,50,18,58,26],
        [33, 1,41, 9,49,17,57,25]
        ]
    # Xếp các bit trong matrix_binary_R (8x8) vào vị trí phù hợ trong IP_1
    for i in range(8):
        for j in range(8):
            a = IP_1[i][j]-1
            IP_1[i][j] = matrix_binary_R[a//8][a%8]
    return matrixToString(IP_1) # string 64bits
#==============================================================================
def MaHoa(matrix_binary_L, matrix_binary_R, matrix_binary_Key): # (4x8) (4x8) (6x8)
    # Bước 1: Mở rộng E
    matrix_binary_E = E(matrix_binary_R) #(8x6)
    # Bước 2: E Xor Khoa
    matrix_binary_XOR = XOR_48bits(matrix_binary_E, matrix_binary_Key) # (8x6) = (8x6) xor (6x8)
    # Bước 3: Sbox
    matrix_binary_SBox = SBOX(matrix_binary_XOR) # (4x8)
    # Bước 4: Hoán vị P
    matrix_binary_P = P(matrix_binary_SBox) # (4x8)
    # Bước 5: Ri = Li-1 Xor kq4 & Li = Ri-1
    Li = matrix_binary_R
    Ri = XOR_32bits(matrix_binary_L, matrix_binary_P) # (4x8) = (4x8) xor (4x8)
    return Li, Ri # (4x8)
#==============================================================================

if __name__=='__main__':
    print()
