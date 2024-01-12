from greytheory import GreyTheory
grey = GreyTheory()


# GM0N
gm0n = grey.gm0n

gm0n.add_outputs([1., 1., 1., 1., 1., 1.], "x1")
gm0n.add_patterns([.75, 1.22, .2, 1., 1., 1.], "x2")
gm0n.add_patterns([.5, 1., .7, .66, 1., .5], "x3")
gm0n.add_patterns([1., 1.09, .4, .33, .66, .25], "x4")
gm0n.add_patterns([.25, .99, 1., .66, .33, .25], "x5")

gm0n.analyze()

# Looks GM0N the results as below:
gm0n.print_analyzed_results()
gm0n.print_influence_degrees()

# GM1N
gm1n = grey.gm1n

gm1n.add_outputs([2., 11., 1.5, 2., 2.2, 3.], "x1")
gm1n.add_patterns([3., 13.5, 1., 3., 3., 4.], "x2")
gm1n.add_patterns([2., 11., 3.5, 2., 3., 2.], "x3")
gm1n.add_patterns([4., 12., 2., 1., 2., 1.], "x4")
gm1n.add_patterns([1., 10., 5., 2., 1., 1.], "x5")

gm1n.analyze()

# Looks GM1N the results as below:
gm1n.print_analyzed_results()
gm1n.print_influence_degrees()

# GM11
gm11 = grey.gm11

# To try customized alpha for IAGO of Z.
gm11.alpha = 0.5
gm11.convolution = False # Convolutional forecasting of GM11.
gm11.stride = 1 
gm11.length = 4

# gm11.add_pattern(533.0, "x1")
# gm11.add_pattern(665.0, "x2")
# gm11.add_pattern(655.0, "x3")
# gm11.add_pattern(740.0, "x4")

gm11.add_pattern(223.3, "a1")
gm11.add_pattern(227.3, "a2")
gm11.add_pattern(230.5, "a3")
gm11.add_pattern(238.1, "a4")
gm11.add_pattern(242.9, "a5")
gm11.add_pattern(251.1, "a6")

gm11.forecast()

# To record last forecasted result.
last_forecasted_results = gm11.forecasted_outputs

# To clean all forecasted results. 
gm11.clean_forecasted()

# In next iteration of forecasting, we wanna continue use last forecasted results to do next forecasting, 
# but if we removed gm11.forecasted_outputs list before,  
# we can use continue_forecasting() to extend / recall the last forecasted result come back to be convolutional features. 
gm11.continue_forecasting(last_forecasted_results)


# Looks GM11 the results for example as below:
gm11.print_forecasted_results()

"""
# multiprocessing examples:
# for GM0N, GM1N
queue = []
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())
queue.append(gm0n.deepcopy())

grey.run.gm0n(queue)

for gm in queue:
    gm.print_influence_degrees()

# for GM11
gm11_queue = []
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())
gm11_queue.append(gm11.deepcopy())

grey.run.gm11(gm11_queue)

for gm in gm11_queue:
    gm.print_forecasted_results()

"""


# import numpy as np
# # Deng’s grey relational grade.
# # Developed in Python 3.7, Numpy 1.18.1.
# # Programmer: Wanli Xie, Date: 2020/12/2.
# # This code is based on the grey correlation degree in [1].
# # [1] S. F. Liu, Y. J. Yang, J. Forrest, Grey Data Analysis: Methods, Models and Applications, Springer-Verlag, Singapore.,2017.
# index1 = [3439, 4002, 4519, 4995, 5566];# Reference sequence
# index2 = [341, 409, 556, 719, 903];# Comparative sequences
# index3 = [183, 196, 564, 598, 613];# Comparative sequences
# index4= [3248, 3856, 6029, 7358, 8880];# Comparative sequences
# x=np.array([index1,index2,index3,index4]);
# normalization_x=np.multiply(x,(1/(np.tile(np.array(x[:,0]),(x.shape[1],1)))).T)# Normalized by initial value.
# ck=normalization_x[0,:]
# cp=normalization_x[1:,:]
# t=cp-np.tile(ck,(cp.shape[0],1))
# Maximum=abs(t).max().max()
# Minimum=abs(t).min().min()
# ksi=((Minimum+0.5*Maximum)/(abs(t)+0.5*Maximum))
# GCC=np.sum(ksi,axis=1)/ksi.shape[1]#Grey relational grade.
# print(GCC)

