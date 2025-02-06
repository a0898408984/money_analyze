import numpy as np
年化報酬_趴 = 0.15 # user input
年化標準差_趴 = 0.20 # user input
相關費用_萬 = 0.53  # user input
借錢_萬 = 100  # user input
年借錢利息 = 0.032  # user input
分N期 = 12*20  # user input
內扣_趴 = 0.006  # user input
股票手續費 = 0.001425  # user input
# 交易稅減半至2027(用原價計算)
交易稅_趴 = 0.001  # user input (一般買賣0.3, 當沖=0.15, etf=0.1)
股票手續費_打折 = 0.6 # user input
總投資額_萬 = 借錢_萬-相關費用_萬
init_etf_price = 100 # user input
if_show_maximal = True # user input
test_num=100000
import os


savefiledir = f'{os.path.dirname(os.path.abspath(__file__))}/log'
# if no dir, make dir
if not os.path.exists(savefiledir):
    os.makedirs(savefiledir)
savefilename = f'房貸轉股票_{分N期}期_{年借錢利息:.4f}_{年化報酬_趴:.2f}_{年化標準差_趴:.2f}_'
maxnum = -1
for x in os.listdir(savefiledir):
    if x.find(savefilename) != -1 and x.find('.txt') != -1:
        prefixname = "_".join(x.split('_')[:-1])
        tmpname = x.replace('.txt','').split('_')[-1].strip()
        if tmpname == '':
            tmpname = 0
        else:
            tmpname = int(tmpname)
        maxnum = max(maxnum,tmpname)
savefilename = f'{savefilename}{maxnum+1}.txt'

logpath = f"{savefiledir}/{savefilename}"
with open(logpath,'w',encoding='utf-8') as f:
    f.write(
        f'年化報酬_趴: {年化報酬_趴}\n'
        f'年化標準差_趴: {年化標準差_趴}\n'
        f'相關費用_萬: {相關費用_萬}\n'
        f'借錢_萬: {借錢_萬}\n'
        f'年借錢利息: {年借錢利息}\n'
        f'分N期: {分N期}\n'
        f'內扣_趴: {內扣_趴}\n'
        f'股票手續費: {股票手續費}\n'
        f'交易稅_趴: {交易稅_趴}\n'
        f'股票手續費_打折: {股票手續費_打折}\n'
        f'總投資額_萬: {總投資額_萬}\n'
        f'init_etf_price: {init_etf_price}\n'
        f'if_show_maximal: {if_show_maximal}\n'
        f'test_num: {test_num}\n'
    )



期借錢利期 = 年借錢利息 / 12
月化投報_趴 =年化報酬_趴 / 12
月化標準差_趴 = 年化標準差_趴 / (12) ** 0.5
txt = f'月化投報: {月化投報_趴}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

txt = f'月化投報: {月化投報_趴}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

r = 期借錢利期 
n = 分N期
月繳_萬 = 借錢_萬*(1+r)**n/((1+r)**n - 1) * r 
txt = f'月繳_萬: {月繳_萬}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')



def 考慮相關費用後的年利率(年借錢利息,借錢_萬,分N期,月繳_萬,相關費用_萬):
    # 考慮相關費用後的年利率
    total總年利率 = -1
    findminidx = -1
    findminidx_tmp = 1000000000000
    n = 分N期
    r = 年借錢利息/12
    for i in range(0, 10001):
        tmp_r = 年借錢利息 + i/50000
        tmp_月繳 = 借錢_萬*(1+tmp_r/12)**n/((1+tmp_r/12)**n - 1) * tmp_r/12
        if abs(tmp_月繳*分N期 - (月繳_萬*分N期+相關費用_萬)) < findminidx_tmp:
            findminidx = i
            findminidx_tmp = abs(tmp_月繳*分N期 - (月繳_萬*分N期+相關費用_萬))
        if tmp_月繳*分N期 > (月繳_萬*分N期+相關費用_萬):
            break
    total總年利率 = 年借錢利息 + findminidx/50000
    return total總年利率

total總年利率 = 考慮相關費用後的年利率(年借錢利息,借錢_萬,分N期,月繳_萬,相關費用_萬)


txt=f'原本 {年借錢利息:.5f} total總年利率: {total總年利率:.5f}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')



def stimulation_once(內扣_趴=內扣_趴,
                    股票手續費=股票手續費,
                    交易稅_趴=交易稅_趴,
                    股票手續費_打折=股票手續費_打折,
                    月化投報_趴=月化投報_趴,
                    月化標準差_趴=月化標準差_趴,
                    總投資額_萬=總投資額_萬,
                    分N期=分N期,
                    月繳 = 月繳_萬,
                    init_etf_price = init_etf_price,
                    if_print = True,
                     ):
    
    股票手續費 = 股票手續費 * 股票手續費_打折
    月化投報_趴 = 月化投報_趴 - 內扣_趴/12  

    init_etf_price = 100 
    etf_price = init_etf_price
    etf_init_num_股 = int(總投資額_萬 / init_etf_price * (1-股票手續費) * 10000)
    月繳 = int(月繳_萬*10000)
    etf_price_list = [init_etf_price]
    if if_print:
        print('etf_init_num_股:', etf_init_num_股)
        
    盈餘股數 = 0
    負債 = 0
    for i in range(1, 分N期+1):
        etf_price = etf_price * (1 + np.random.normal(月化投報_趴, 月化標準差_趴))
        etf_price_list.append(etf_price)
        月賣股數 = int(月繳/(1-股票手續費-交易稅_趴)/etf_price)
        etf_init_num_股 -= 月賣股數
        if etf_init_num_股<=0:
            負債 += 月繳 - (etf_init_num_股+月賣股數)*(1-股票手續費-交易稅_趴)*etf_price
            負債 += 月繳*(分N期 - i)
            etf_init_num_股 = 0
        if if_print:
            總負債txt = f"/股數已清空若要還清剩餘貸款負債: {int(負債)}" if 負債 > 0 else ''
            print(f'月繳 {月繳} ( 第{i} 需月賣股數: {月賣股數} /剩餘股數: {etf_init_num_股} /股價: {etf_price:.2f} {總負債txt})')
        if etf_init_num_股<=0:
            break
    盈餘股數 = etf_init_num_股
    盈餘 = etf_init_num_股*etf_price if etf_init_num_股 > 0 else -負債
    return {
        "負債": 負債,
        "盈餘股數": 盈餘股數,
        "etf_price_list": etf_price_list,
        "盈餘": 盈餘,
    }

from tqdm import tqdm

money_list = []
negmoney_list = []
posmoney_list = []
negmoney_dict = {}
posmoney_dict = {}

all_ans = {}
for i in tqdm(range(test_num)):
    ans = stimulation_once(if_print=False)
    money_list.append(ans["盈餘"])
    if ans["盈餘"] <= 0:
        negmoney_list.append(ans["盈餘"])
        negmoney_dict[str(ans["盈餘"])] = i
    if ans["盈餘"] > 0:
        posmoney_list.append(ans["盈餘"])
        posmoney_dict[str(ans["盈餘"])] = i
    if i % 10000 == 9999:
        print(f'目前預期收益: {np.mean(money_list):.2f} / 虧錢次數 {len(negmoney_list )}/{i+1}')
    if if_show_maximal:
        all_ans[i] = ans
negmoney_list.sort()
posmoney_list.sort(reverse=True)
txt = f'目前預期收益: {np.mean(money_list):.2f} / 虧錢次數 {len(negmoney_list )}/{i+1}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

NEG_N = len(negmoney_list)
POS_N = len(posmoney_list )
# 虧損分析
txt = f'虧損時平均負債:{np.mean(negmoney_list):.2f}/\n(最大虧損: {negmoney_list[np.argmin(negmoney_list)]:.2f}/\n 1%平均虧損: {np.mean(negmoney_list[:int(NEG_N*0.01)]):.2f}/\n10%平均虧損: {np.mean(negmoney_list[int(NEG_N*0.01):int(NEG_N*0.1)]):.2f}/\n25%平均虧損: {np.mean(negmoney_list[int(NEG_N*0.1):int(NEG_N*0.25)]):.2f}/\n50%平均虧損: {np.mean(negmoney_list[int(NEG_N*0.25):int(NEG_N*0.50)]):.2f}/\n75%平均虧損: {np.mean(negmoney_list[int(NEG_N*0.5):int(NEG_N*0.75)]):.2f})/\n100%平均虧損: {np.mean(negmoney_list[int(NEG_N*0.75):]):.2f})'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

# 獲利分析
txt = f'獲利時平均獲利:{np.mean(posmoney_list):.2f}/\n(最大獲利: {posmoney_list[np.argmax(posmoney_list)]:.2f}/\n 1%平均獲利: {np.mean(posmoney_list[:int(POS_N*0.01)]):.2f}/\n10%平均獲利: {np.mean(posmoney_list[int(POS_N*0.01):int(POS_N*0.1)]):.2f}/\n25%平均獲利: {np.mean(posmoney_list[int(POS_N*0.1):int(POS_N*0.25)]):.2f}/\n50%平均獲利: {np.mean(posmoney_list[int(POS_N*0.25):int(POS_N*0.50)]):.2f}/\n75%平均獲利: {np.mean(posmoney_list[int(POS_N*0.5):int(POS_N*0.75)]):.2f})/\n100%平均虧損: {np.mean(posmoney_list[int(POS_N*0.75):]):.2f})'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')



if if_show_maximal:
    import matplotlib.pyplot as plt 
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.01)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 1% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.01)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_1percent.png')
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.12)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 12% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.12)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_12percent.png')
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.25)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 25% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.25)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_25percent.png')
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.50)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 50% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.50)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_50percent.png')
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.75)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 75% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.75)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_75percent.png')
    maxneg_price_list = all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.88)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'neg 88% total: {all_ans[negmoney_dict[str(negmoney_list[int(NEG_N*0.88)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_neg_88percent.png')
    # plt.show()

    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.01)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'pos 1% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.01)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_1percent.png')
    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.12)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'pos 12% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.12)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_12percent.png')
    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.25)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'pos 25% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.25)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_25percent.png')
    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.50)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'pos 50% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.50)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_50percent.png')
    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.75)])]]['etf_price_list']
    plt.figure()
    plt.plot(maxneg_price_list)
    plt.title(f'pos 75% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.75)])]]["盈餘"]:.2f}')
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_75percent.png')
    maxneg_price_list = all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.88)])]]['etf_price_list']
    plt.figure()
    plt.title(f'pos 88% total: {all_ans[posmoney_dict[str(posmoney_list[int(POS_N*0.88)])]]["盈餘"]:.2f}')
    plt.plot(maxneg_price_list)
    plt.savefig(f'{savefiledir}/{savefilename.replace(".txt","")}_pos_88percent.png')