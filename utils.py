import sys
sys.setrecursionlimit(10000) # 设置递归最大层数为10000

# 暴力计算胡牌的概率
def getMatchOpportunity(inputList,remainsDict,abandonType=0,recurse=False):
    pass
# 计算现在可以胡哪些牌（0为不能胡）
def getListeningCards(inputList,remainsDict,abandonType=0): # abandonType=0（不忽略缺一门）1（缺万子）2（缺条子）3（缺筒子）
    # 例：remainsDict = {1:2,...,3:1,...,15:3} 代表一万剩两张，三万剩一张，五条剩三张 没有的用0表示数量
    # Brute-force searching
    if abandonType != 0:
        remainsDict = getDictByAbandonColor(remainsDict,abandonType=abandonType)
    listeningCards = []
    for card in remainsDict.keys():
        if remainsDict[card]>0: # 剩了这个牌
            tempList = list(inputList)
            tempList.append(card)
            if isMatched(tempList): # 加一张场上剩余牌之后可以胡牌，代表现在可以听牌
                listeningCards.append(card)

    if len(listeningCards) == 0: # 没有可以胡的牌
        return [0]
    return listeningCards

# 判断是否可以听牌，有没有叫
def isListening(inputList,remainsDict,abandonType=0): # abandonType=0（不忽略缺一门）1（缺万子）2（缺条子）3（缺筒子）
    # 例：remainsDict = {1:2,...,3:1,...,15:3} 代表一万剩两张，三万剩一张，五条剩三张 没有的用0表示数量
    # Brute-force searching
    remainsDict = getDictByAbandonColor(remainsDict,abandonType=abandonType)
    for card in remainsDict.keys():
        if remainsDict[card]>0: # 剩了这个牌
            tempList = list(inputList)
            tempList.append(card)
            if isMatched(tempList): # 加一张场上剩余牌之后可以胡牌，代表现在可以听牌
                return True
    return False

# 递归判断胡牌
def isMatched(inputList,debug=False,recurse=False): # recurse: 递归控制，传入参数时不需要该参数
    inputList.sort()
    if not recurse:
        # 暗七对
        if getAACount(inputList,getType=2) == 7:
            return True
        # 龙七对
        if getAACount(inputList,getType=2) == 5 and getAACount(inputList,getType=4) == 1:
            return True
    # 普通情况
    if not recurse: # 第一次查找，先去除将
        AAList = [] # 记录已经移除过的将牌
        success = 0
        for card in inputList:
            if inputList.count(card)>=2 and card not in AAList: # 可能的将牌
                recurseList = list(inputList)
                recurseList.remove(card)
                recurseList.remove(card)
                AAList.append(card)
                if debug:
                    print("remove "+str(card)+" as AA")
                    print("now recurseList: "+str(recurseList))
                if isMatched(recurseList,debug=debug,recurse=True) : # 这里可能第一个对子胡不了，所以要遍历完所有对子，有一个匹配的就能胡
                    success += 1
        if success == 0:
            return False
        return True
    if recurse: # 去除将牌之后的递归
        if len(inputList)==0: return True
        if inputList.count(inputList[0])<=2: # 第一张牌只有一张或两张，则其必须组成顺子才能胡牌，否则胡不了
            if inputList[0]+1 in inputList and inputList[0]+2 in inputList:
                recurseList = list(inputList)
                recurseList.remove(inputList[0])
                recurseList.remove(inputList[0]+1)
                recurseList.remove(inputList[0]+2)
                if debug:
                    print("remove "+str(inputList[0])+" as ABC")
                    print("now recurseList: "+str(recurseList))
                if len(recurseList) == 0 : return True
                else: return isMatched(recurseList,debug=debug,recurse=True)
            else: 
                return False
        if inputList.count(inputList[0])>=3: # 第一张牌有三张或四张，则其可以自己组成一个三连，剩下的一张跟后面的组成一个顺子，这里因为去除了杠下来的牌，所以不考虑四张自己组成一个杠的情况
            recurseList = list(inputList)
            recurseList.remove(inputList[0])
            recurseList.remove(inputList[0])
            recurseList.remove(inputList[0])
            return isMatched(recurseList,debug=debug,recurse=True)


# 获取对子、三连、四连数
def getAACount(inputCardList, cardType=0, getType=2): # cardType = 0（全部）1（万）2（条）3（筒） getType = 2（对子）3（三连）4（四连）
    """
    获取对子、三连、四连数
    :param inputCardList: 传入的牌组列表
    :param cardType: 0（全部）1（万）2（条）3（筒）
    :param getType: 2（对子）3（三连）4（四连）
    :return AACount: 对子、三连、四连数
    """
    if cardType > 3 or cardType < 0 :
        print("[getAACount]获取对子参数不符合规定!")
        return
    AACount = 0
    if cardType == 0:
        cardList = inputCardList
    elif cardType == 1: # 万子
        cardList = getListByColor(inputCardList,cardType=1)
    elif cardType == 2: # 条子
        cardList = getListByColor(inputCardList,cardType=2)
    elif cardType == 3: # 筒子
        cardList = getListByColor(inputCardList,cardType=3)
    index = 0
    cardList.sort() # 对指定牌组排序
    while index<len(cardList):
        if cardList.count(cardList[index]) == getType: # 数量相等
            AACount += 1
            index += getType # 跳过等量的牌
        else: index += 1
    return AACount

# 获取ABC顺子数
def getABCCount(inputCardList, cardType=0): # cardType = 0（全部）1（万）2（条）3（筒）
    """
    获取顺子数
    :param inputCardList: 传入的牌组列表
    :param cardType: 0（全部）1（万）2（条）3（筒）
    :return ABCCount: 顺子数
    """
    if cardType > 3 or cardType < 0 :
        print("[getABCCount]获取顺子参数不符合规定!")
        return
    ABCCount = 0
    if cardType == 0:
        cardList = inputCardList
    elif cardType == 1: # 万子
        cardList = getListByColor(inputCardList,cardType=1)
    elif cardType == 2: # 条子
        cardList = getListByColor(inputCardList,cardType=2)
    elif cardType == 3: # 筒子
        cardList = getListByColor(inputCardList,cardType=3)
    index = 0
    cardList.sort() # 对指定牌组排序
    while index<len(cardList)-2: # 最后两张不用搜索
        if cardList[index]+1==cardList[index+1] and cardList[index]+2==cardList[index+2]: # 找到ABC顺子牌
            ABCCount += 1
            index += 3 # 跳过这三张牌
        else: index += 1
    return ABCCount

# 根据花色获取牌组列表
def getListByColor(inputCardList, cardType=0): # cardType = 0（全部）1（万）2（条）3（筒）
    """
    根据花色获取牌组列表
    :param inputCardList: 传入的牌组列表
    :param cardType: 0（全部）1（万）2（条）3（筒）
    :return outputList: 筛选出的牌组列表
    """
    if cardType > 3 or cardType < 0 :
        print("[getListByColor]牌花色参数不符合规定!")
        return
    if cardType == 0:
        outputList = inputCardList
    elif cardType == 1: # 万子
        outputList = [ x for x in inputCardList if 1 <= x <= 9 ]
    elif cardType == 2: # 条子
        outputList = [ x for x in inputCardList if 11 <= x <= 19 ]
    elif cardType == 3: # 筒子
        outputList = [ x for x in inputCardList if 21 <= x <= 29 ]
    return outputList

# 根据弃牌花色获取剩余牌组字典
def getDictByAbandonColor(inputCardDict, abandonType=0):# abandonType=0（不忽略缺一门）1（缺万子）2（缺条子）3（缺筒子）
    if abandonType == 0:
        outputDict = inputCardDict
    elif abandonType == 1: # 不要万子
        outputDict = dict_slice(inputCardDict,9,27) # 输出筒子和条子
    elif abandonType == 2: # 不要条子
        outputDict = {**dict_slice(inputCardDict,0,9),**dict_slice(inputCardDict,18,27)} # 拼接万子和筒子，最后输出
    elif abandonType == 3: # 不要筒子
        outputDict = dict_slice(inputCardDict,0,18) # 输出万子和条子
    return outputDict

# 字典切片
def dict_slice(ori_dict, start, end):
    """
    字典类切片
    :param ori_dict: 字典
    :param start: 起始
    :param end: 终点
    :return:
    """
    slice_dict = {k: ori_dict[k] for k in list(ori_dict.keys())[start:end]}
    return slice_dict
