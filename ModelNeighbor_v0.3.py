from MainCalculate import *
import time
import os

def main(path1, path2, path3):
    try:
        main_cal(path1, path2, path3)
        print('finished')
        return 1
    except BaseException as reason:
        print(reason)
        return reason


if __name__ == '__main__':
    main('邻线干扰参数输入_V001.xlsx',
         '仿真输出' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xlsx',
         os.getcwd())
    # main(sys.argv[1], sys.argv[2], sys.argv[3])