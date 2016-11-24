'''
这是一个应用在动态规划领域的维特比算法及一个例子。具体网址可见：
https://zh.wikipedia.org/wiki/%E7%BB%B4%E7%89%B9%E6%AF%94%E7%AE%97%E6%B3%95
本代码对原网址的代码进行了适当修改，主要目的是为了更好的显示运算逻辑及结果，其原理与原作完全一致
test函数提供您多次输入observation给出status的示例
修改者：叶强 qqiangye@gmail.com
修改日期：2016/11/24
'''
import math
# 状态的样本空间
states = ('Healthy', 'Fever')
# 观测的样本空间
observations = ('normal', 'cold', 'dizzy')
# 起始个状态概率
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
# 状态转移概率
transition_probability = {
  'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
  'Fever': {'Healthy': 0.4, 'Fever': 0.6},
}
# 状态->观测的发散概率
emission_probability = {
  'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
  'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
}
# 计算以E为底的幂
def E(x):
  return math.pow(math.e,x)


def display_result(observations,result_m):
  """
  较为友好清晰的显示结果
  :param result_m:
  :return:
  """
  # 从结果中找出最佳路径
  infered_states = []
  final = len(result_m)-1
  (p,pre_state),final_state = max(zip(result_m[final].values(), result_m[final].keys()))
  infered_states.insert(0, final_state)
  infered_states.insert(0, pre_state)
  for t in range(final-1,0,-1):
    _, pre_state = result_m[t][pre_state]
    infered_states.insert(0,pre_state)
    
  print(format("Viterbi Result","=^59s"))
  head = format("obs"," ^10s")
  head += format("Infered state"," ^18s")
  for s in states:
    head += format(s," ^15s")
  print(head)
  print(format("", "-^59s"))

  for obs,result,infered_state in zip(observations,result_m,infered_states):
    item = format(obs," ^10s")
    item += format(infered_state," ^18s")
    for s in states:
      item += format(result[s][0]," >12.8f")
      if infered_state == s:
        item += "(*)"
      else:
        item +="   "

    print(item)
  print(format("", "=^59s"))



def viterbi(obs, states, start_p, trans_p, emit_p):

  result_m = [{}] # 存放结果,每一个元素是一个字典，每一个字典的形式是 state:(p,pre_state)
                  # 其中state,p分别是当前状态下的概率值，pre_state表示该值由上一次的那个状态计算得到
  for s in states:  # 对于每一个状态
    result_m[0][s] = (start_p[s]*emit_p[s][obs[0]],None) # 把第一个观测节点对应的各状态值计算出来

  for t in range(1,len(obs)):
    result_m.append({})  # 准备t时刻的结果存放字典，形式同上

    for s in states: # 对于每一个t时刻状态s,获取t-1时刻每个状态s0的p,结合由s0转化为s的转移概率和s状态至obs的发散概率
                     # 计算t时刻s状态的最大概率，并记录该概率的来源状态s0
                     # max()内部比较的是一个tuple:(p,s0),max比较tuple内的第一个元素值
      result_m[t][s] = max([(result_m[t-1][s0][0]*trans_p[s0][s]*emit_p[s][obs[t]],s0) for s0 in states])
  return result_m    # 所有结果（包括最佳路径）都在这里，但直观的最佳路径还需要依此结果单独生成，在显示的时候生成


def example():
  """
  一个可以交互的示例
  """
  result_m = viterbi(observations,
                 states,
                 start_probability,
                 transition_probability,
                 emission_probability)
  display_result(observations,result_m)
  while True:
    user_obs = input("Now give me your observation, I will infer the state\n"
                "Using 'N' for normal, 'C' for cold and 'D' for dizzy\n"
                "Input here('q' to exit):")

    if len(user_obs) ==0 or 'q' in user_obs or 'Q' in user_obs:
      break
    else:
      obs = []
      for o in user_obs:
        if o.upper() == 'N':
          obs.append("normal")
        elif o.upper() == 'C':
          obs.append("cold")
        elif o.upper() == 'D':
          obs.append("dizzy")
        else:
          pass
      result_m = viterbi(obs,
                       states,
                       start_probability,
                       transition_probability,
                       emission_probability)
      display_result(obs,result_m)



if __name__ == "__main__":
  example()
