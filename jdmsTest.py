# -*- coding: utf-8-*-
import requests
import json
import re
import csv 
import xlwt
import xlutils

dnbg = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=29&_=1495211171059'#电脑办公
shdq= 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=19&_=1495250002658' #生活电器
sjtx = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=30&_=1495251020781' #手机通讯
dxjd = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=25&_=1495251044176' #大型家电
znsm = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=31&_=1495251057993' #智能数码
yljs = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=45&_=1495251084828' # 饮料酒水
jjjz = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=37&_=1495251148047' #家具家装
mytz = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=43&_=1495251122767' #母婴童装
spsx = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=44&_=1495250603966' #食品生鲜
ghjq = 'https://ai.jd.com/index_new?app=Seckill&action=pcSeckillCategoryGoods&callback=pcSeckillCategoryGoods&id=32&_=1495251170952' #个护家清

categoryList = [
            ["电脑办公",dnbg],
            ["生活电器",shdq],
            ["手机通讯",sjtx],
            ["大型家电",dxjd],
            ["智能数码",znsm],
            ["饮料酒水",yljs],
            ["家具家装",jjjz],
            ["母婴童装",mytz],
            ["食品生鲜",spsx],
            ["个护家清",ghjq]
        ]


def jdmiaosha(categoryList): #开始只是想爬去电脑办公的 函数是后来加上去的
    workbook = xlwt.Workbook(encoding = 'utf-8')
    name = 0
    url = 1
    for category in categoryList:
    
        resp= requests.get(category[url]).text
    #print(resp)
        resp = re.findall(r'\((.+)\)',resp)[0] #提取纯json代码 不然解析会出错
    #print(resp)
        s = json.loads(resp)
        # print(s)
        
        
        worksheet = workbook.add_sheet(category[name])
        worksheet.col(0).width = 30000
        worksheet.col(6).width = 8000

        row = worksheet.row(0)
        row.write(0,"商品名称")
        row.write(1,"京东价格")
        row.write(2,"秒杀价格")
        row.write(3,"折扣比例")
        row.write(4,"开始时间")
        row.write(5,"销售状态")
        row.write(6,"链接")
        line = 0
        for i in s['goodsList']:
            line = line + 1
            row = worksheet.row( line )
            sales_url = "https://item.jd.com/" + str( i['wareId'] ) +".html"
            if 'soldRate' in i.keys():
                sales_status = str( i['soldRate'] ) + "%"  # 区别是否开抢   确定销售状态
            else:
                if not i['startTimeContent']:
                    sales_status = "---"
                else:
                    sales_status = i[ 'startTimeContent' ]
            # print('商品：{0}\t价格：{1}\t销售状态:{2}\t链接:{3}.'.format(i['wname'],i['miaoShaPrice'],sales_status,sales_url))  #格式化输出
            row.write( 0, i['wname'] )
            row.write( 1, i['jdPrice'] )
            row.write( 2, i['miaoShaPrice'] )
            percent = ( float(i['jdPrice']) - float( i['miaoShaPrice']) ) / float( i['jdPrice'] )*100
            percent = round( percent, 2 )
            row.write( 3, str( percent ) + "%" )
            row.write( 4, i[ 'startTimeShow' ] )
            row.write( 5, sales_status )
            row.write( 6, sales_url )
    workbook.save( "jd.xls" );    


if __name__ == '__main__':
    jdmiaosha(categoryList)

