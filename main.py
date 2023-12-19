import math
def fullRegressionProblem(Xi,Yi,nij):

    nj=[5,6,11,25,9,4]
    ni=[10,12,24,8,6]
    n=60

    # print('ni :',ni)
    # print('nj :',nj)
    # print(n)

    m=len(nij[0])

    X_avg=0 #X с чертой Х среднее
    Y_avg=0 #Y с чертой У среднее
    for i in range(len(Xi)):
        X_avg+=Xi[i]*ni[i]
        # print(Xi[i],ni[i])

    for i in range(len(Yi)):
        Y_avg+=Yi[i]*nj[i]
        # print(Yi[i],nj[i])
    X_avg=X_avg/n
    Y_avg=Y_avg/n
    print('X_avg :',X_avg)
    print('Y_avg :',Y_avg)

    XY_avg=0# ХУ с чертой ХУ среднее
    for i in range(len(ni)):
        for j in range(len(nj)):
            # print(Xi[i],Yi[j],nij[i][j])
            XY_avg+=(Xi[i]*Yi[j]*nij[i][j])

    XY_avg=XY_avg/n
    print('XY_avg :',XY_avg)

    Y2_avg=0# Y2 с чертой Y в квадрате среднее
    X2_avg=0# Х2 с чертой Х в квадрате среднее
    for i in range(len(Xi)):
        X2_avg+=((pow(Xi[i],2))*ni[i])
        # print(Xi[i],ni[i])
    for i in range(len(Yi)):
        Y2_avg += ((pow(Yi[i], 2)) * nj[i])
        # print(Xi[i], ni[i])
    Y2_avg=Y2_avg/n
    X2_avg=X2_avg/n

    print('Y2_avg :',Y2_avg,'X2_avg :',X2_avg)

    S2_X=X2_avg-pow(X_avg,2)#S2_X выборочная дисперсия
    S2_Y=Y2_avg-pow(Y_avg,2)#S2_Y выборочная дисперсия
    print('S2_X :',S2_X,'S2_Y :',S2_Y)


    M=XY_avg-X_avg*Y_avg#M выборочный корреляционный момент (ковариация)
    print('M :',M)

    byx=M/S2_X# byx- коэффициент линейной регрессии y по х
    bxy=M/S2_Y# bxy- коэффициент линейной регрессии x по y
    print('byx :',byx,'bxy :',bxy)

    #Yx=Y_avg+Byx(X-X_avg)
    #Xy=X_avg+Bxy(Y-Y_avg)

    # r=(XY_avg-X_avg*Y_avg)/(pow(S2_X,1/2)*pow(S2_Y,1/2))# Коэффициент корреляции

    r=pow(abs(bxy*byx),1/2)# Коэффициент корреляции другая формула
    # Заметная корреляция -0,65 , Умеренная - 0.4 , слабая -0.2
    print('r :',r)

    #Определяем t(1-alpha;n-2) по таблице t=2.01 для P=0.95 и n = 50
    t=2.01

    # beta yx будет в следующих границах
    beta_yx_1=byx-t*((pow(S2_Y,1/2)*pow(1-pow(r,2),1/2))/(pow(S2_X,1/2)*pow(n-2,1/2)))
    beta_yx_2=byx+t*((pow(S2_Y,1/2)*pow(1-pow(r,2),1/2))/(pow(S2_X,1/2)*pow(n-2,1/2)))
    #beta_yx_1 <beta yx<beta_yx_2
    print('beta_yx_1 :',beta_yx_1,'beta_yx_2 :',beta_yx_2)

    # beta xy будет в следующих границах
    beta_xy1=bxy-t*((pow(S2_X,1/2)*pow(1-pow(r,2),1/2))/(pow(S2_Y,1/2)*pow(n-2,1/2)))
    beta_xy_2 = bxy + t * ((pow(S2_X, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (pow(S2_Y, 1 / 2) * pow(n - 2, 1 / 2)))
    # beta_xy_1 <beta xy<beta_xy_2
    print('beta_xy_1 :',beta_xy1,'beta_xy_2 :',beta_xy_2)

    z=(1/2)*(math.log(abs((1+r)/(1-r)),math.exp(1)))#z-преобразование
    print('z :',z)

    #M будет в следующих границ
    M_1=z-t/(pow(n-3,1/2))#Мат. ожидание (нижняя граница)
    M_2=z+t/(pow(n-3,1/2))#Мат. ожидание
    print('M_1 :',M_1,'M_2 :',M_2)

    # p будет в следующих границ

    p_1=(math.exp(M_1)-math.exp(-M_1))/(math.exp(M_1)+math.exp(-M_1))#Генеральный коэффициент корреляции(нижняя граница)
    p_2=(math.exp(M_2)-math.exp(-M_2))/(math.exp(M_2)+math.exp(-M_2))#Генеральный коэффициент корреляции(верхняя граница)
    print('p_1 :',p_1,'p_2 :',p_2)

    Yi_avg=[]#Yi с чертой групповое среднее
    Xi_avg=[]#Xi с чертой групповое среднее

    for i in range(len(nj)):
        Xi_avg.append(0)
        for j in range(len(ni)):
            Xi_avg[i]+=Xi[j]*nij[j][i]
            # print('X' + str(i+1) + ':', Xi[j], nij[j][i])
        Xi_avg[i] = Xi_avg[i] / nj[i]
        # print('nj',nj[i])

    print('Xi_avg :', Xi_avg)
    for i in range(len(ni)):
        Yi_avg.append(0)
        for j in range(len(nj)):
            # print('Y' + str(i+1) + ':', Yi[j], nij[i][j])
            Yi_avg[i] +=Yi[j]*nij[i][j]
        Yi_avg[i] = Yi_avg[i] / ni[i]

    print('Yi_avg :', Yi_avg)

    # Yi_avg=[0.7,2.1,3.5,4.9,6.3,7.7]#Yi с чертой групповое среднее
    # Xi_avg = [2.25,6.75,11.25,15.75,20.25]#Xi с чертой групповое среднее

    б2_iy=0#Не знаю название переменной, напиши если знаешь)
    б2_ix=0#Не знаю название переменной, напиши если знаешь)

    for i in range(len(nj)):
        б2_ix += pow((Xi_avg[i] - X_avg), 2) * nj[i]
        # print(Xi_avg[i],nj[i])
    for i in range(len(ni)):
        # print(Yi_avg[i], ni[i])
        б2_iy+=pow((Yi_avg[i]-Y_avg),2)*ni[i]

    б2_iy=б2_iy/n
    б2_ix = б2_ix / n
    print('б2_iy',б2_iy,'б2_ix',б2_ix)

    nyx=pow(б2_iy/S2_Y,1/2)# Корреляционное отношение y по x
    nxy = pow(б2_ix / S2_X, 1 / 2)  # Корреляционное отношение x по y
    print('nyx :',nyx,'nxy :',nxy)

    Yxi=[]#Не знаю название переменной, напиши если знаешь)
    Xyj = []  # Не знаю название переменной, напиши если знаешь)
    for i in range(len(ni)):
        Yxi.append(0)
        Yxi[i]+=Y_avg+byx*(Xi[i]-X_avg)
    for j in range(len(nj)):
        Xyj.append(0)
        Xyj[j] += X_avg + bxy * (Yi[j] - Y_avg)
    print('Yxi :',Yxi,'Xyi :',Xyj)

    б2_x=0#Не знаю название переменной, напиши если знаешь)
    б2_y=0#Не знаю название переменной, напиши если знаешь)

    for i in range(len(Xyj)):
        б2_x+= pow(Xyj[i]-X_avg,2)*nj[i]
        print(Xyj[i],nj[i])
    for j in range(len(Yxi)):
        б2_y += pow(Yxi[j] - Y_avg, 2) * ni[j]
    б2_x=б2_x/n
    б2_y = б2_y / n
    print('б2_x :',б2_x,'б2_y :',б2_y)


    #Rxy - множественный коэффициент корелляционного значения
    Ryx=pow(б2_y/S2_Y,1/2)#Не знаю название переменной, напиши если знаешь)
    Rxy=pow(б2_x/S2_X,1/2)#Не знаю название переменной, напиши если знаешь)
    print('Ryx :',Ryx,'Rxy :',Rxy)

    Fyx=(pow(nyx,2)*(n-m))/((1-pow(nyx,2))*(m-1))#Уровень значимости
    Fxy = (pow(nxy, 2) * (n - m)) / ((1 - pow(nxy, 2)) * (m - 1))  # Уровень значимости
    print('Fyx :',Fyx,'Fxy :',Fxy)

    #По таблице находим  теоретическое значение уровня значимости F(0,05;4;45), если наше значение больше то значимо)

    if(0<r<Ryx<nyx<1):
        print('Hell yeah')
    else:
        print('(')

fullRegressionProblem([2.25, 6.75, 11.25, 15.75, 20.25], [0.7, 2.1, 3.5, 4.9, 6.3, 7.7],
                      [[4, 4,2, 0, 0, 0], [1, 2, 8,1, 0, 0], [0, 0, 1, 20,3, 0], [0, 0, 0, 4,3, 1], [0, 0,0, 0, 3, 3],
                       [0, 0, 0, 1, 3]])
# fullRegressionProblem([47,59,71,83,95],[13.35,15.85,18.35],[[3,1,0],[2,3,0],
#                                                             [0,11,1],[0,2,4],[0,0,3]])
# fullRegressionProblem([2.25, 6.75, 11.25, 15.75, 20.25], [0.7, 2.1, 3.5, 4.9, 6.3, 7.7],
#                       [[4, 4,2, 0, 0, 0], [1, 2, 8,1, 0, 0], [0, 0, 1, 20,3, 0], [0, 0, 0, 4,3, 1], [0, 0,0, 0, 3, 3],
#                        [0, 0, 0, 1, 3]])
