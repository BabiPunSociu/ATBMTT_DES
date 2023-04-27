
# Thuat toan chuan hoa du lieu DES
import DES_MaHoa
import DES_SinhKhoa

# import re để sử dụng regular expression
import re

def nhap64bits(mes):
    while True:
        _input = input(mes)
        # Thay thế các kí tự khác "chữ cái hexa hoặc số" bởi chuỗi rỗng
        _input = re.sub('[^A-F0-9]+', '', _input)
        # Kiểm tra input có đủ 16 kí tự ~ 64 bits không?
        if len(_input)== (64/4):
            return _input

if __name__=='__main__':
    # Input (M_64bits, K_64bits)
    M = nhap64bits('Nhập bản rõ 64 bits (dạng hexa): M = ')
    K = nhap64bits('Nhập khóa 64 bits (dạng hexa): K = ')
    
    # Hoán vị PC1 -> C0, D0:
    C, D = DES_SinhKhoa.PC_1(K) # str_28bits
    print('C0 = '+C)
    print('D0 = '+D)
    # Hoán vị khởi đầu IP:
    IP = DES_MaHoa.IP(M) # (8x8)
    # Chia thành 2 phần L0, R0:
    matrix_binary_L, matrix_binary_R = DES_MaHoa.SPLIT(IP) # (4x8)
    
    print('L0 = '+ DES_MaHoa.binToHex(DES_MaHoa.matrixToString(matrix_binary_L)))
    print('R0 = '+ DES_MaHoa.binToHex(DES_MaHoa.matrixToString(matrix_binary_R)))
    
    # Thực hiện lặp 16 vòng sinh khóa + mã hóa:
    for i in range(16):
        print('Vòng thứ '+str(i+1))
        # Sinh khóa
        C, D, matrix_binary_Key = DES_SinhKhoa.SinhKhoa(C, D, i+1) # vì số vòng từ 1-> 16
        print('K'+str(i+1)+' = ' + DES_MaHoa.binToHex(DES_MaHoa.matrixToString(matrix_binary_Key)))
        # Mã hóa
        matrix_binary_L, matrix_binary_R = DES_MaHoa.MaHoa(matrix_binary_L, matrix_binary_R, matrix_binary_Key)

        print('L'+str(i+1)+' = '+ DES_MaHoa.binToHex(DES_MaHoa.matrixToString(matrix_binary_L)))
        print('R'+str(i+1)+' = '+ DES_MaHoa.binToHex(DES_MaHoa.matrixToString(matrix_binary_R)))
    # Hoán vị trái - phải 32 bits và IP-1:
    str_binary_result = DES_MaHoa.IP_1(matrix_binary_R, matrix_binary_L)
    str_hexa_result = DES_MaHoa.binToHex(str_binary_result)
    print('Kết quả:'+str_hexa_result)