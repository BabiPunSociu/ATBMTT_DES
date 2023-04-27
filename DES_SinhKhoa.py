import DES_MaHoa
#==============================================================================
def PC_1(string_64bit_hexa):
    # Chuyển hexa thành bin: list<string>
    str_binary = DES_MaHoa.hexaToBin(string_64bit_hexa) # (8x8)

    # PC1: 56bits (8x7)
    PC1 = [
        [57,49,41,33,25,17, 9],
        [ 1,58,50,42,34,26,18],
        [10, 2,59,51,43,35,27],
        [19,11, 3,60,52,44,36],
        [63,55,47,39,31,23,15],
        [ 7,62,54,46,38,30,22],
        [14, 6,61,53,45,37,29],
        [21,13, 5,28,20,12, 4]
        ]
    # Xếp các bit ở matrix_binary vào vị trí phù hợp trong PC1
    for i in range(8):
        for j in range(7):
            a = PC1[i][j]-1
            PC1[i][j]=str_binary[a//8][a%8]
    # Chia thành 2 nửa C, D
    C = PC1[:4]
    D = PC1[4:]
    # Chuyển C, D thành string để dễ thực hiện các bước sau
    str_C = DES_MaHoa.matrixToString(C)
    str_D = DES_MaHoa.matrixToString(D)
    return str_C, str_D # string 28 bits
#==============================================================================
def LeftShifts(string_binary_28bits, vong_i): # str -> str
    # Tạo chuỗi chứa 28bits
    str_28bits =""
    for rows in string_binary_28bits:
        for x in rows:
            str_28bits += str(x)
    # LeftShift:
    lst_dich_vong_trai_1bits = [1,2,9,16]
    if vong_i in lst_dich_vong_trai_1bits:
        str_28bits = str_28bits[1:]+str_28bits[0]
    else: # Dịch vòng trái 2 bits
        str_28bits = str_28bits[2:]+str_28bits[0]+str_28bits[1]
    return str_28bits
#==============================================================================
def PC_2(str_C, str_D): # return matrix (6x8)
    str_CD = str_C + str_D
    PC2=[
        [14,17,11,24, 1, 5, 3,28],
        [15, 6,21,10,23,19,12, 4],
        [26, 8,16, 7,27,20,13, 2],
        [41,52,31,37,47,55,30,40],
        [51,45,33,48,44,49,39,56],
        [34,53,46,42,50,36,29,32]
        ]
    # Xếp các bits ở str_CD vào vị trí phù hợp trong PC2
    for i in range(6):
        for j in range(8):
            a = PC2[i][j]-1 # vì chỉ số bắt đầu từ 0
            PC2[i][j] = str_CD[a]
    return PC2 # matrix binary (6x8)
#==============================================================================
def SinhKhoa(str_C, str_D, vong_i):
    # Bước 1: LeftShift
    Ci = LeftShifts(str_C, vong_i)
    Di = LeftShifts(str_D, vong_i)
    # Bước 2: PC2 -> khóa Ki
    matrix_binary_Key = PC_2(Ci, Di)
    return Ci, Di, matrix_binary_Key
#==============================================================================
if __name__=='__main__':
    print()