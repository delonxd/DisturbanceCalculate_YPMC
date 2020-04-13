import pandas as pd
import os

filepath = 'C:\\Users\\Delon\\Desktop\\徐州东邻线干扰仿真'
dir_path = 'C:\\Users\\Delon\\Desktop\\徐州东邻线干扰仿真\\结果导出'

file_list = [
    # '电码化_2600对2000_极性交叉.xlsx',
    # '412m_2300对1700_6电容_送端电容未拆除.xlsx',
    # '421m_2600对2000_6电容_送端电容拆除.xlsx',
    # '422m_2600对2000_7电容_送端电容未拆除.xlsx',
    # '406.5m_2600对2000_主4被4（不含TB）_已拆除送端电容.xlsx',
    # '406.5m_2600对2000_主5被6（不含TB）_已拆除送端电容.xlsx',
    # '406.5m_2600对2000_主6被7（不含TB）_未拆除送端电容.xlsx',
    # '北京南测试_有砟路基21_已拆除送端电容.xlsx',
    # '北京南测试_太青场参数_已拆除送端电容.xlsx',
    # '北京南测试_太青场参数_未拆除送端电容.xlsx',
    # '北京南测试_太青场参数_未拆除送端电容_道床电阻20.xlsx',
    # '北京南测试_太青场参数_修正.xlsx',
    # '电码化拆除发送端电容.xlsx',
    # '650m_主2600_被2000_被串C35换TB_断线遍历.xlsx',
    # '650m_主2300_被1700_被串C35换TB_断线遍历.xlsx',
    # '650m_主2600_被2000_被串C246换TB_断线遍历.xlsx',
    # '650m_主2300_被1700_被串C246换TB_断线遍历.xlsx',
    # '650m_电容断线遍历.xlsx',
    # '650m_C2C3断线.xlsx',
    # '626m_主2600_被2000_被串换5个TB_断线两TB遍历.xlsx',
    # '同频率_被串轨入电压遍历.xlsx',
    # '650m_全频率_1700和2000换装TB.xlsx',
    '移频脉冲_650m_全频率_4级电平.xlsx',
]

for filename in file_list:
    new_path = os.path.join(dir_path, filename)
    tp = os.path.join(filepath, filename)
    df_input = pd.read_excel(tp, sheet_name=None)

    with pd.ExcelWriter(new_path) as writer:
        for sheet_name, df_output in df_input.items():
            df_output.to_excel(writer, sheet_name=sheet_name, index=False)
pass