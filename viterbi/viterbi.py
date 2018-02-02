#!/usr/bin/env python
#_*_coding:utf-8_*_
'''
村民只有两种简单的属性：健康或者发烧。他们只能通过诊所的医生知道自己是否发烧。聪明的医生通过询问病人感觉如何来诊断是否发烧；村民的回答是：正常、头晕、寒冷三者之一。
假设某病人每天都来诊所告诉医生她感觉如何。医生认为病人的健康状况是一个离散的马尔科夫链（Markov chain）。有两种状态"Healthy"和"Fever"，但是医生没法直接观察到，也就是说这两个状态对医生来说是隐藏(hidden)的。每天，病人会基于自身健康状况，以某个几率告诉医生他的感觉：可能是"normal"、"cold"或"dizzy"三者之一，这些事观察值。这里的整个系统可以看做是隐马尔科夫模型（HMM）。

'''
from numpy import   *
class dataClass:
    def __init__(self):
        #身体两种状态，健康和有病
        self.q = ['healthy', 'fever']
        #观察值，三天内观察到的病人的身体表现
        self.observe = ['normal', 'cold', 'dizzy']
        #初始概率，也就是刚开始时，身体的状态，60%认为健康，40%认为有病
        self.pai = {'healthy':0.6, 'fever':0.4}
        #状态转移概率
        self.A = {'healthy':{'healthy':0.7, 'fever':0.3},'fever':{'healthy':0.4, 'fever':0.6}}
        #生成概率，也称发射概率，确定身体状态时，身体的外在表现
        self.B = {'healthy':{'normal':0.5,'cold':0.4,'dizzy':0.1},
             'fever':{'normal':0.1,'cold':0.3,'dizzy':0.6}}
def viterbi(data, observe):  #输入observe表示了这三天病人的身体表现，返回这三天的健康状况
    tNum = len(observe)  #序列长度
    N = len(data.q) #有多少状态
    delta = {}
    psai = {}
    for i in data.q:
        delta_in = {0:data.pai[i]*data.B[i][observe[0]]} #初始化，根据观测值设定
        delta[i] = delta_in
        psai_in = {0:0}
        psai[i] = psai_in
    for t in range(1,tNum):
        for i in data.q:
            qKey = [j for j in data.q]
            maxProb = max([delta[j][t-1]*data.A[j][i] for j in data.q])
            delta_in = {t:maxProb*data.B[i][observe[t]]}
            delta[i].update(delta_in)
            maxVal = qKey[argmax([delta[j][t-1]*data.A[j][i] for j in data.q])]
            psai[i].update({t:maxVal})
    maxVal = 0.0
    maxIndex = -1
    for i in data.q:
        if delta[i][tNum-1]>maxVal:
            maxVal = delta[i][tNum-1]
            maxIndex = i
    iT = maxIndex
    I = []  #I中存储的即为结果，该结果最能解释对病人都观察值的健康状态序列
    I.append(iT)
    for t in range(tNum-2,-1,-1):
        iT = psai[I[0]][t+1]
        I.insert(0,iT)
    return I


if __name__ == '__main__':
    observe = ['normal','cold','dizzy']  #病人三天的外在表现
    data = dataClass()  #初始化
    result = viterbi(data, observe)
    print('result:',result)


