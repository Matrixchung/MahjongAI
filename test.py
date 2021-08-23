import random
from typing import Dict
from utils import *
from main import cards
sys.setrecursionlimit(10000) # 设置递归最大层数为10000

# 玩家回合，摸起来一张牌之后计算打出手中每张牌的胡牌概率，选择一个概率最大的牌打出
# 此方法必须在摸上来牌之后，打出牌之前调用
# 计算胡牌的概率
def getMatchOpportunityPerCard(inputList,remainsDict,abandonType=0,recurse=False,recursedList=[],debug=False):
    inputList.sort()
    remainsSum = sum(remainsDict.values())
    if not recurse: # 第一次计算，递归控制部分

        if isMatched(inputList): # 现在就胡牌
            opts = dict.fromkeys(inputList, 1.0)
            return opts

        # 构建一个概率字典，key为手牌号码，value为打这张牌胡的概率
        opts = dict.fromkeys(inputList, 0.0)
        # 初始化完成，现在打所有手牌胡的概率都为0

        stepToListening = 0 # 至少需要几步才能听牌

        # 普通情况，现在未胡牌，应该打一张牌出来
        for discardingCard in inputList: # 将要被打出的牌
            # 第一种情况：打一张牌之后能听
            # 那么打这张牌能胡的概率就是所有能听的牌占剩余牌数的比例
            recurseList = list(inputList)
            recurseList.remove(discardingCard)
            listeningResult = getListeningCards(recurseList,remainsDict,abandonType=abandonType)
            opt = 0
            if 0 not in listeningResult: # 有能听的牌
                if stepToListening == 0: stepToListening += 1
                for i in listeningResult:
                    opt += remainsDict[i]
                opt = opt/remainsSum
                opts[discardingCard] = opt
        
        if stepToListening == 0: # 打一张牌听不了，那么就递归直到能听
            return getMatchOpportunityPerCard(inputList,remainsDict,abandonType=abandonType,recurse=True,debug=debug)
        else: return opts

    if recurse: # 递归计算部分
        # 从remainsDict中摸一张牌，递归计算胡牌概率，如果胡不了就打出重新递归，最后把所有概率相加
        # 打一张牌再摸一张，再打再摸
        opts = dict.fromkeys(inputList, 0.0)
        stepToListening = 0
        for discardingCard in inputList:
            recurseList = list(inputList)
            recurseList.remove(discardingCard)
            listeningResult = getListeningCards(recurseList,remainsDict,abandonType=abandonType)
            opt = 0
            if 0 not in listeningResult: # 有能听的牌
                print("got it")
                print("now list: "+str(recurseList))
                print("listening: "+str(listeningResult))
                if stepToListening == 0: stepToListening += 1
                for i in listeningResult:
                    opt += remainsDict[i]
                opt = opt/remainsSum
                opts[discardingCard] = opt
            else: # 打这张牌听不了，但是打掉了
                if discardingCard not in recursedList:
                    recursedList.append(discardingCard)
                    print("discard "+str(discardingCard))
                    # 现在需要摸一张
                    for incomingCard in remainsDict.keys():
                        if incomingCard not in recursedList:
                            recurseList.append(incomingCard)
                            nowDict = dict(remainsDict)
                            nowDict[incomingCard] -= 1
                            return getMatchOpportunityPerCard(recurseList,nowDict,abandonType=abandonType,recurse=True,recursedList=recursedList,debug=debug)
        
        # return opts



def findClosestListening(inputList,remainsDict,abandonType=0):
    if len(findListeningByDelete(inputList,remainsDict,abandonType=abandonType)) == 0: # 打一张牌之后无法听牌
         

                        


def findListeningByDelete(inputList,remainsDict,abandonType=0): # 打出一张牌之后能不能听牌
    cardsToListening = [] # 打出之后能听的牌
    discardedList = []
    for discardingCard in inputList:
        if discardingCard not in discardedList:
            discardedList.append(discardingCard)
            tempList = list(inputList)
            tempList.remove(discardingCard) # 打出这张牌
            # 此时 remainsDict 不变
            listeningResult = getListeningCards(tempList,remainsDict,abandonType=abandonType)
            if 0 not in listeningResult: # 有听牌
                print("discardToListen: "+str(discardingCard)) # 打出这张牌后有叫
                print("nowList: "+str(tempList))
                cardsToListening.append(discardingCard)
            else:
                print("discard: "+str(discardingCard))
                print("no listening: "+str(tempList))
            del(tempList)
    return cardsToListening


if __name__=="__main__":
    cardDict = {}
    cardNumber = 1
    while cardNumber<=29:
        if cardNumber == 10 or cardNumber == 20:
            cardNumber += 1
            continue
        cardDict[cardNumber]=4
        cardNumber += 1
    wanRemains = dict_slice(cardDict,18,27)
    # print(wanRemains)
    # cardList = cards([1,2,3,6,6,7,8,9,12,13,17,18,19]) 
    # cardList = cards([1,1,2,2,3,3,4,4,5,5,14,14,14]) # 龙七对
    # cardList = cards([4,5,6,7,8,9,9,14,15,16,17,18,19]) # 3 6 9
    cardList = cards([3,4,5,5,6,7,7,12,14,18,16,17,18,19]) # 1 4 7

    # cardList = cards([4,5,6,5,6,7,6,7,8,7,8,9,9])
    # print(isListening(cardList.getList(),cardList.cardsRemain,abandonType=cardList.abandonCardType))
    # print(getListeningCards(cardList.getList(),cardList.cardsRemain,abandonType=cardList.abandonCardType))
    #print(isMatched([1,2,3,6,6,6,9,9,22,23,24,25,26,27],debug=True))
    # print(isMatchedNew([3,4,5,6,7,8,8,14,15,16,17,18,19,3]))
    #print(isMatched([4,5,6,5,6,7,6,6,7,8,9,11,12,13],debug=True))
    # print(getListeningCards(cardList.getList(),cardList.cardsRemain,abandonType=cardList.abandonCardType))
    # print(getMatchOpportunityPerCard(cardList.getList(),cardList.cardsRemain,cardList.abandonCardType,debug=True))
    print(findClosestListening(cardList.getList(),cardList.cardsRemain,cardList.abandonCardType))



    