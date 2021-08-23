# 万：1 2 3 4 5 6 7 8 9 (wan)
# 条：11 12 13 14 15 16 17 18 19 (tiao)
# 筒：21 22 23 24 25 26 27 28 29 (tong)
# 一副牌13张（庄家开头14张）（每杠一个加一张牌）
# 杠下来的牌因为不能再做任何变动或者与手牌组合，所以从牌组中去掉
# 胡牌 = AA and (AAA or AAAA or ABC)
# AA：是将牌
# AAA：是碰牌
# AAAA：是杠牌
# ABC：是顺子
# 七对情况：1、暗七对（7xAA）2、龙七对（1xAAAA+5xAA）
# 一回合：摸1张牌 - 判断isMatched - isMatched（否）- 换一张牌changeCard（打出去） - 更新牌堆列表
import random
from utils import *
params = [10,2,1]
scale = 50
# 全局手牌剩余字典类
class cardsLeft:
    # 初始化全局手牌
    cardsTotal = {}
    def __init__(self,cardHold):
        cardNumber = 1
        while cardNumber<=29:
            if cardNumber == 10 or cardNumber == 20:
                cardNumber += 1
                continue
            self.cardsTotal[cardNumber] = 4
            cardNumber += 1
        
        for card in cardHold:
            self.cardsTotal[card] -= 1

# 玩家手牌列表类
class cards:
    wanCount = tiaoCount = tongCount = 0
    abandonCardType = 0 # 1为万 2为条 3为筒
    cardsRemain = {}
    scores = []
    # 判断是否为整数
    def __isNumber(self, n):
        if not isinstance(n,(int)):
            return False
        return True
    
    # 初始化
    def __init__(self,args):
        if not args:
            print("请传入起始牌组!")
            self.__failsafe()
        if len(args)>14: # 最大起始牌数14
            print("起始牌组数错误")
            self.__failsafe()
        for arg in args:
            if not self.__isNumber(arg):
                print("牌组代码必须为整数!")
                self.__failsafe()
            if arg<1 or arg>29:
                print("牌组不符合规定!")
                self.__failsafe()
        self.__value = []
        for arg in args:
            self.__add(arg) # 添加牌
        self.__value.sort()
        # 弃一个花色的牌
        self.__abandon()
        self.cardsRemain = cardsLeft(self.__value).cardsTotal
        print(self.debug_getAbandonType())
    
    # 获取牌组列表
    def getList(self):
        return self.__value
    
    # 删除全局已经打出的牌
    def remove(self, card):
        self.cardsRemain[card] -= 1
        return self.cardsRemain[card]
    
    # 添加牌
    def __add(self, card):
        if card<1 or card>29:
            print("牌组不符合规定!")
            return
        if card>=1 and card<=9: # 万
            self.wanCount += 1
        elif card>=11 and card<=19: # 条
            self.tiaoCount += 1
        elif card>=21 and card<=29: # 筒
            self.tongCount += 1
        self.__value.append(card)
    
            
    # 摸到牌之后打出一张手牌
    def changeCard(self,cardGet=0,isBanker=False):
        if not isBanker:
            self.__value.append(cardGet)
        if self.isMatched():
            return 0
        self.generateCardScore()
        discardCard = self.__value[self.scores.index(min(self.scores))]
        self.__value.remove(discardCard)
        return discardCard
    
    # 每张牌的分数，分数低者优先打出
    def generateCardScore(self):

        """ self.__value.sort()
        scores = []
        cards = self.__value
        remains = self.cardsRemain
        wanCards = [ x for x in cards if 1 <= x <= 9 ]
        tiaoCards = [ x for x in cards if 11 <= x <= 19 ]
        tongCards = [ x for x in cards if 21 <= x <= 29 ]
        wanRemains = dict_slice(remains,0,9)
        tiaoRemains = dict_slice(remains,9,18)
        tongRemains = dict_slice(remains,18,27)
        for wan in wanCards:
            score = 0
            if self.abandonCardType != 1: # 要万子
                for w in wanCards:
                    gap = abs(wan-w)
                    if gap<3:
                        score += params[gap]*scale
                for wi in wanRemains:
                    gap = abs(wan-wi)
                    if gap<3:
                        score += params[gap]
            scores.append(score)
        
        for tiao in tiaoCards:
            score = 0
            if self.abandonCardType != 2: # 要条子
                for t in tiaoCards:
                    gap = abs(tiao-t)
                    if gap<3:
                        score += params[gap]*scale
                for ti in tiaoRemains:
                    gap = abs(tiao-ti)
                    if gap<3:
                        score += params[gap]
            scores.append(score)
        
        for tong in tongCards:
            score = 0
            if self.abandonCardType != 3: # 要筒子
                for t in tongCards:
                    gap = abs(tong-t)
                    if gap<3:
                        score += params[gap]*scale
                for ti in tongRemains:
                    gap = abs(tong-ti)
                    if gap<3:
                        score += params[gap]
            scores.append(score)
        
        self.scores=scores """
    
    # 两色一样时顺子和对子的积分决策层
    # 顺子分数:1 对子:2 三连:3(四连不可能为最少的牌)
    def __abandonByScores(self,type1,type2):
        inputList = self.__value
        t1Score = getABCCount(inputList,cardType=type1)+2*getAACount(inputList,cardType=type1,getType=2)+3*getAACount(inputList,cardType=type1,getType=3)
        t2Score = getABCCount(inputList,cardType=type2)+2*getAACount(inputList,cardType=type2,getType=2)+3*getAACount(inputList,cardType=type2,getType=3)
        if t1Score == t2Score: # 积分一样，随机弃牌
            if random.randint(1,2)==1: return type1
            return type2
        if t1Score>t2Score :
            return type2
        return type1

    # 弃一个花色的牌（弃最少的）
    # 可能出现两种花色一样的情况
    # 未考虑初始牌为清一色的情况
    def __abandon(self):
        wanCount = self.wanCount
        tiaoCount = self.tiaoCount
        tongCount = self.tongCount

        if wanCount == tiaoCount:
            if wanCount<tongCount: # 万条花色一样多且都比第三种花色少，根据连子和对子数弃一个花色
                self.abandonCardType = self.__abandonByScores(1,2)
            else: self.abandonCardType = 3
            return
        if wanCount < tiaoCount: # 万比条子少
            if wanCount < tongCount: self.abandonCardType = 1 # 万最少
            elif tongCount < wanCount: self.abandonCardType = 3 # 筒最少
            elif wanCount == tongCount: # 万筒花色一样多且都比第三种花色少，根据连子和对子数弃一个花色
                self.abandonCardType = self.__abandonByScores(1,3)
            return
        if wanCount > tiaoCount: # 万比条子多
            if tiaoCount < tongCount: self.abandonCardType = 2 # 条最少
            elif tongCount < tiaoCount: self.abandonCardType = 3 # 筒最少
            elif tongCount == tiaoCount: # 筒条花色一样多且都比第三种花色少，根据连子和对子数弃一个花色
                self.abandonCardType = self.__abandonByScores(2,3)
            return
    
    # debug
    def debug_getAbandonType(self):
        if self.abandonCardType == 1: return "万"
        if self.abandonCardType == 2: return "条"
        if self.abandonCardType == 3: return "筒"
        return "未指定"
    
    # fail-safe
    def __failsafe(self):
        self.__value = [0]*13
        return

if __name__ == '__main__':
    #cardList = cards(1,1,1,1,2,3,3,3,21,21,21,21,22)
    #cardList = cards(1,2,3,4,5,6,7,8,9,11,12,13,14)
    #cardList = cards(1,1,1,1,5,7,9,11,13,15,16,17,21,25)
    #print(cardList.isMatched())
    #print(cardList.changeCard())
    isBanker = False
    isBanker = bool(input("请选择是否为庄家(1/0):"))
    print("请输入初始手牌：")
    print("万：1 2 3 4 5 6 7 8 9 ")
    print("条：11 12 13 14 15 16 17 18 19 ")
    print("筒：21 22 23 24 25 26 27 28 29 \n")
    if isBanker:
        print("1 2 3 4 5 6 7 8 9 10 11 12 13 14")
        print("__-__-__-__-__-__-__-__-__-__-__-__-__-__ \n")
    else:
        print("1 2 3 4 5 6 7 8 9 10 11 12 13 \n")
        print("__-__-__-__-__-__-__-__-__-__-__-__-__\n")
    userInput = list(map(int,input().split()))
    cardList = cards(userInput)
    if isBanker:
        cardDiscard = cardList.changeCard(isBanker=True)
        print("打出 "+ str(cardDiscard) +" 号牌")
    isMatched = False
    gameMode = 0 # 1 摸到牌 2 其他人打出牌
    while not isMatched:
        if gameMode == 0:
            gameMode = int(input("请选择摸到牌或他人打出牌(1/2)："))
        if gameMode == 1:
            cardGet = int(input("请输入摸到的牌:"))
            cardDiscard = cardList.changeCard(cardGet)
            if cardDiscard == 0: # 自摸
                isMatched = True
                print("自摸了!")
                break 
            else: 
                print("打出 "+ str(cardDiscard) +" 号牌")
                gameMode = 2
                continue
        elif gameMode == 2:
            cardDiscardedByOther = int(input("请输入他人打出的牌:"))
            cardList.remove(cardDiscardedByOther)
            gameMode = 0
            continue
        

