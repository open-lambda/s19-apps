
import src2.lampy as np
# from src2.lampy import

def openlambda_reqeust():
    return "curl -X "



def start_server():
    pass




if __name__ == '__main__':
    """
    Example1: 2D Convolution
        In remote setting, lazy create the Object M and N
        
    """


    start_server()

    url_M = ""
    url_N = ""
    M = np.array(url_M)
    N = np.array(url_N)
    M.shape
    N.shape

    # Method 1. Lazy Initilization
    # Method 2. Object Preview
    # print(M)
    # print(N)
    A = M.conv(N)
    A.shape

