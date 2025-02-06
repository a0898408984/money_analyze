import numpy as np

# User inputs
annual_return_rate = 0.15  # 年化報酬率 (%) - Annual return rate (as a decimal) # user input
annual_std_dev = 0.20  # 年化標準差 (%) - Annual standard deviation (as a decimal) # user input
related_fees_10k = 0.53  # 相關費用 (萬) - Related fees (in 10k NTD) # user input
loan_amount_10k = 100  # 借款金額 (萬) - Loan amount (in 10k NTD) # user input
annual_loan_interest = 0.032  # 年借款利率 (%) - Annual loan interest rate (as a decimal) # user input
installments = 12 * 20  # 分期數 (N期) - Number of installments (e.g., 20 years = 240 months) # user input
deduction_rate = 0.006  # 內扣費用 (%) - Upfront deduction rate (as a decimal) # user input
stock_fee_rate = 0.001425  # 股票手續費 (%) - Stock transaction fee rate (as a decimal) # user input
# 交易稅減半至2027(用原價計算)
tax_rate = 0.001  # 交易稅 (%) - Transaction tax rate (as a decimal) (General = 0.3%, Day trading = 0.15%, ETF = 0.1%) # user input
stock_fee_discount = 0.6  # 股票手續費折扣 - Stock transaction fee discount (e.g., 60% of the original fee) # user input
total_investment_10k = loan_amount_10k - related_fees_10k  # 總投資額 (萬) - Total investable amount (in 10k NTD)
init_etf_price = 100 # user input
if_show_maximal = True # user input
test_num=100000
import os


savefiledir = f'{os.path.dirname(os.path.abspath(__file__))}/log'
# if no dir, make dir
if not os.path.exists(savefiledir):
    os.makedirs(savefiledir)
savefilename = f'房貸轉股票_{installments}期_{annual_loan_interest:.4f}_{annual_return_rate:.2f}_{annual_std_dev:.2f}_'
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
        f'年化報酬_趴: {annual_return_rate}\n'
        f'年化標準差_趴: {annual_std_dev}\n'
        f'相關費用_萬: {related_fees_10k}\n'
        f'借錢_萬: {loan_amount_10k}\n'
        f'年借錢利息: {annual_loan_interest}\n'
        f'分N期: {installments}\n'
        f'內扣_趴: {deduction_rate}\n'
        f'股票手續費: {stock_fee_rate}\n'
        f'交易稅_趴: {tax_rate}\n'
        f'股票手續費_打折: {stock_fee_discount}\n'
        f'總投資額_萬: {total_investment_10k}\n'
        f'init_etf_price: {init_etf_price}\n'
        f'if_show_maximal: {if_show_maximal}\n'
        f'test_num: {test_num}\n'
    )



monthly_loan_interest = annual_loan_interest / 12  # 期借款利率 - Monthly loan interest rate
monthly_return_rate = annual_return_rate / 12  # 月化投報率 (%) - Monthly return rate (as a decimal)
monthly_std_dev = annual_std_dev / (12) ** 0.5  # 月化標準差 (%) - Monthly standard deviation (as a decimal)

txt = f'月化投報: {monthly_return_rate}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

txt = f'月化投報: {monthly_return_rate}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')

r = monthly_loan_interest 
n = installments
monthly_payment_10k = loan_amount_10k*(1+r)**n/((1+r)**n - 1) * r   # 月繳 (萬) - Monthly payment to the loan (in 10k NTD)
txt = f'月繳_萬: {monthly_payment_10k}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')



def Annual_interest_rate_after_considering_related_fees(annual_loan_interest,loan_amount_10k,installments,monthly_payment_10k,related_fees_10k):
    # 考慮相關費用後的年利率 Annual_interest_rate_after_considering_related_fees
    Total_annual_interest_rate = -1
    findminidx = -1
    findminidx_tmp = 1000000000000
    n = installments
    r = annual_loan_interest/12
    for i in range(0, 10001):
        tmp_r = annual_loan_interest + i/50000
        tmp_月繳 = loan_amount_10k*(1+tmp_r/12)**n/((1+tmp_r/12)**n - 1) * tmp_r/12
        if abs(tmp_月繳*installments - (monthly_payment_10k*installments+related_fees_10k)) < findminidx_tmp:
            findminidx = i
            findminidx_tmp = abs(tmp_月繳*installments - (monthly_payment_10k*installments+related_fees_10k))
        if tmp_月繳*installments > (monthly_payment_10k*installments+related_fees_10k):
            break
    Total_annual_interest_rate = annual_loan_interest + findminidx/50000
    return Total_annual_interest_rate

Total_annual_interest_rate = Annual_interest_rate_after_considering_related_fees(annual_loan_interest,loan_amount_10k,installments,monthly_payment_10k,related_fees_10k)


txt=f'原本 {annual_loan_interest:.5f} total總年利率: {Total_annual_interest_rate:.5f}'
print(txt)
with open(logpath,'a',encoding='utf-8') as f:
    f.write(txt+'\n')



def stimulation_once(deduction_rate=deduction_rate,
                    stock_fee_rate=stock_fee_rate,
                    tax_rate=tax_rate,
                    stock_fee_discount=stock_fee_discount,
                    monthly_return_rate=monthly_return_rate,
                    monthly_std_dev=monthly_std_dev,
                    total_investment_10k=total_investment_10k,
                    installments=installments,
                    monthly_payment_10k = monthly_payment_10k,
                    init_etf_price = init_etf_price,
                    if_print = True,
                     ):
    
    stock_fee_rate = stock_fee_rate * stock_fee_discount
    monthly_return_rate = monthly_return_rate - deduction_rate/12  
    init_etf_price = 100 
    etf_price = init_etf_price
    etf_init_num_股 = int(total_investment_10k / init_etf_price * (1-stock_fee_rate) * 10000)
    monthly_payment_10k = int(monthly_payment_10k*10000)
    etf_price_list = [init_etf_price]
    if if_print:
        print('etf_init_num_股:', etf_init_num_股)
        
    surplus_shares = 0  # 盈餘股數 - Surplus shares (number of shares available)
    debt = 0  # 負債 - Debt (amount of outstanding debt)
    for i in range(1, installments+1):
        etf_price = etf_price * (1 + np.random.normal(monthly_return_rate, monthly_std_dev))
        etf_price_list.append(etf_price)
        monthly_sell_shares = int(monthly_payment_10k/(1-stock_fee_rate-tax_rate)/etf_price)  # 月賣股數 - Number of shares to sell per month (for loan repayment)
        etf_init_num_股 -= monthly_sell_shares  
        if etf_init_num_股<=0:
            debt += monthly_payment_10k - (etf_init_num_股+monthly_sell_shares )*(1-stock_fee_rate-tax_rate)*etf_price
            debt += monthly_payment_10k*(installments - i)
            etf_init_num_股 = 0
        if if_print:
            tmptxt = f"/股數已清空若要還清剩餘貸款負債: {int(debt)}" if debt > 0 else ''
            txt = f'月繳 {monthly_payment_10k} ( 第{i} 需月賣股數: {monthly_sell_shares } /剩餘股數: {etf_init_num_股} /股價: {etf_price:.2f} {tmptxt})'
            print(txt)
        if etf_init_num_股<=0:
            break
    surplus_shares = etf_init_num_股
    surplus  = etf_init_num_股*etf_price if etf_init_num_股 > 0 else -debt   # 盈餘 - Surplus, calculated from initial ETF shares or debt
    return {
        "負債": debt,
        "盈餘股數": surplus_shares,
        "etf_price_list": etf_price_list,
        "盈餘": surplus ,
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