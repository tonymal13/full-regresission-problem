import math


def calculate_var_average(var_i, n, power=1):  # вычисление среднего значения по переменной
    var_average = 0  # var c чертой var среднее

    for i in range(len(var_i)):
        var_average += math.pow(var_i[i], power) * n[i]
        # print(var_i[i], n[i])

    return var_average


def calculate_xy_average(x_i, y_i, n_i, n_j, n_ij):
    xy_average = 0  # ХУ с чертой ХУ среднее
    for i in range(len(n_i)):
        # print(xy_average)
        for j in range(len(n_j)):
            # print(x_i[i], y_i[j], n_ij[i][j])
            xy_average += (x_i[i] * y_i[j] * n_ij[i][j])

    return xy_average


def fullRegressionProblem(x_i, y_i, n_ij):
    n_j = [5, 6, 11, 25, 9, 4]
    n_i = [10, 12, 24, 8, 6]
    n = 60

    # print('n_i :',n_i)
    # print('n_j :',n_j)
    # print(n)

    m = len(n_ij[0])  # длина столбца

    x_average = calculate_var_average(x_i, n_i) / n  # X с чертой X среднее
    y_average = calculate_var_average(y_i, n_j) / n  # Y с чертой Y среднее

    print('X average:', x_average)
    print('Y average:', y_average)

    xy_average = calculate_xy_average(x_i, y_i, n_i, n_j, n_ij) / n # ХУ с чертой ХУ среднее
    print('xy_average:', xy_average)

    x_pow2_average = calculate_var_average(x_i, n_i, 2) / n  # Y2 с чертой Y в квадрате среднее
    y_pow2_average = calculate_var_average(y_i, n_j, 2) / n  # X2 с чертой X в квадрате среднее

    print('y_pow2_average: ', y_pow2_average, '\n', 'x_pow2_average: ', x_pow2_average)

    selective_correlation_moment_m = xy_average - x_average * y_average  # выборочный корреляционный момент (ковариация)
    print('selective_correlation_moment_m :', selective_correlation_moment_m)

    sample_variance_x_pow2 = x_pow2_average - pow(x_average, 2)  # sample_variance_x_pow2 выборочная дисперсия
    sample_variance_y_pow2 = y_pow2_average - pow(y_average, 2)  # sample_variance_y_pow2 выборочная дисперсия
    print('sample_variance_x_pow2 :', sample_variance_x_pow2, '\n', 'sample_variance_y_pow2 :', sample_variance_y_pow2)

    byx = selective_correlation_moment_m / sample_variance_x_pow2  # byx - коэффициент линейной регрессии y по х
    bxy = selective_correlation_moment_m / sample_variance_y_pow2  # bxy - коэффициент линейной регрессии x по y
    print('byx :', byx, '\n', 'bxy :', bxy)

    # Yx=Y_avg+Byx(X-X_avg)
    # Xy=X_avg+Bxy(Y-Y_avg)

    # r=(xy_average-X_avg*Y_avg)/(pow(sample_variance_x_pow2,1/2)*pow(sample_variance_y_pow2,1/2))# Коэффициент корреляции

    r = pow(abs(bxy * byx), 1 / 2)  # Коэффициент корреляции другая формула
    # Заметная корреляция -0.65, Умеренная - 0.4, слабая -0.2
    print('r :', r)

    # Определяем t(1-alpha;n-2) по таблице t=2.01 для P=0.95 и n = 50
    t = 2.01

    # beta yx будет в следующих границах
    beta_yx_1 = byx - t * ((pow(sample_variance_y_pow2, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (pow(sample_variance_x_pow2, 1 / 2) * pow(n - 2, 1 / 2)))
    beta_yx_2 = byx + t * ((pow(sample_variance_y_pow2, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (pow(sample_variance_x_pow2, 1 / 2) * pow(n - 2, 1 / 2)))
    # beta_yx_1 <beta yx<beta_yx_2
    print('beta_yx_1 :', beta_yx_1, 'beta_yx_2 :', beta_yx_2)

    # beta xy будет в следующих границах
    beta_xy1 = bxy - t * ((pow(sample_variance_x_pow2, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (pow(sample_variance_y_pow2, 1 / 2) * pow(n - 2, 1 / 2)))
    beta_xy_2 = bxy + t * ((pow(sample_variance_x_pow2, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (pow(sample_variance_y_pow2, 1 / 2) * pow(n - 2, 1 / 2)))
    # beta_xy_1 <beta xy<beta_xy_2
    print('beta_xy_1 :', beta_xy1, 'beta_xy_2 :', beta_xy_2)

    z = (1 / 2) * (math.log(abs((1 + r) / (1 - r)), math.exp(1)))  # z-преобразование
    print('z :', z)

    # selective_correlation_moment_m будет в следующих границ
    M_1 = z - t / (pow(n - 3, 1 / 2))  # Мат. ожидание (нижняя граница)
    M_2 = z + t / (pow(n - 3, 1 / 2))  # Мат. ожидание
    print('M_1 :', M_1, 'M_2 :', M_2)

    # p будет в следующих границ

    p_1 = (math.exp(M_1) - math.exp(-M_1)) / (
            math.exp(M_1) + math.exp(-M_1))  # Генеральный коэффициент корреляции(нижняя граница)
    p_2 = (math.exp(M_2) - math.exp(-M_2)) / (
            math.exp(M_2) + math.exp(-M_2))  # Генеральный коэффициент корреляции(верхняя граница)
    print('p_1 :', p_1, 'p_2 :', p_2)

    Yi_avg = []  # Yi с чертой групповое среднее
    Xi_avg = []  # Xi с чертой групповое среднее

    for i in range(len(n_j)):
        Xi_avg.append(0)
        for j in range(len(n_i)):
            Xi_avg[i] += x_i[j] * n_ij[j][i]
            # print('X' + str(i+1) + ':', Xi[j], nij[j][i])
        Xi_avg[i] = Xi_avg[i] / n_j[i]
        # print('n_j',n_j[i])

    print('Xi_avg :', Xi_avg)
    for i in range(len(n_i)):
        Yi_avg.append(0)
        for j in range(len(n_j)):
            # print('Y' + str(i+1) + ':', Yi[j], nij[i][j])
            Yi_avg[i] += y_i[j] * n_ij[i][j]
        Yi_avg[i] = Yi_avg[i] / n_i[i]

    print('Yi_avg :', Yi_avg)

    # Yi_avg=[0.7,2.1,3.5,4.9,6.3,7.7]#Yi с чертой групповое среднее
    # Xi_avg = [2.25,6.75,11.25,15.75,20.25]#Xi с чертой групповое среднее

    б2_iy = 0  # Не знаю название переменной, напиши если знаешь)
    б2_ix = 0  # Не знаю название переменной, напиши если знаешь)

    for i in range(len(n_j)):
        б2_ix += pow((Xi_avg[i] - x_average), 2) * n_j[i]
        # print(Xi_avg[i],n_j[i])
    for i in range(len(n_i)):
        # print(Yi_avg[i], n_i[i])
        б2_iy += pow((Yi_avg[i] - y_average), 2) * n_i[i]

    б2_iy = б2_iy / n
    б2_ix = б2_ix / n
    print('б2_iy', б2_iy, 'б2_ix', б2_ix)

    nyx = pow(б2_iy / sample_variance_y_pow2, 1 / 2)  # Корреляционное отношение y по x
    nxy = pow(б2_ix / sample_variance_x_pow2, 1 / 2)  # Корреляционное отношение x по y
    print('nyx :', nyx, 'nxy :', nxy)

    Yxi = []  # Не знаю название переменной, напиши если знаешь)
    Xyj = []  # Не знаю название переменной, напиши если знаешь)
    for i in range(len(n_i)):
        Yxi.append(0)
        Yxi[i] += y_average + byx * (x_i[i] - x_average)
    for j in range(len(n_j)):
        Xyj.append(0)
        Xyj[j] += x_average + bxy * (y_i[j] - y_average)
    print('Yxi :', Yxi, 'Xyi :', Xyj)

    б2_x = 0  # Не знаю название переменной, напиши если знаешь)
    б2_y = 0  # Не знаю название переменной, напиши если знаешь)

    for i in range(len(Xyj)):
        б2_x += pow(Xyj[i] - x_average, 2) * n_j[i]
        print(Xyj[i], n_j[i])
    for j in range(len(Yxi)):
        б2_y += pow(Yxi[j] - y_average, 2) * n_i[j]
    б2_x = б2_x / n
    б2_y = б2_y / n
    print('б2_x :', б2_x, 'б2_y :', б2_y)

    # Rxy - множественный коэффициент корелляционного значения
    Ryx = pow(б2_y / sample_variance_y_pow2, 1 / 2)  # Не знаю название переменной, напиши если знаешь)
    Rxy = pow(б2_x / sample_variance_x_pow2, 1 / 2)  # Не знаю название переменной, напиши если знаешь)
    print('Ryx :', Ryx, 'Rxy :', Rxy)

    Fyx = (pow(nyx, 2) * (n - m)) / ((1 - pow(nyx, 2)) * (m - 1))  # Уровень значимости
    Fxy = (pow(nxy, 2) * (n - m)) / ((1 - pow(nxy, 2)) * (m - 1))  # Уровень значимости
    print('Fyx :', Fyx, 'Fxy :', Fxy)

    # По таблице находим теоретическое значение уровня значимости F(0,05;4;45), если наше значение больше то значимо)

    if (0 < r < Ryx < nyx < 1):
        print('Hell yeah')
    else:
        print('(')


fullRegressionProblem([2.25, 6.75, 11.25, 15.75, 20.25], [0.7, 2.1, 3.5, 4.9, 6.3, 7.7],
                      [[4, 4, 2, 0, 0, 0], [1, 2, 8, 1, 0, 0], [0, 0, 1, 20, 3, 0], [0, 0, 0, 4, 3, 1],
                       [0, 0, 0, 0, 3, 3],
                       [0, 0, 0, 1, 3]])
# fullRegressionProblem([47,59,71,83,95],[13.35,15.85,18.35],[[3,1,0],[2,3,0],
#                                                             [0,11,1],[0,2,4],[0,0,3]])
# fullRegressionProblem([2.25, 6.75, 11.25, 15.75, 20.25], [0.7, 2.1, 3.5, 4.9, 6.3, 7.7],
#                       [[4, 4,2, 0, 0, 0], [1, 2, 8,1, 0, 0], [0, 0, 1, 20,3, 0], [0, 0, 0, 4,3, 1], [0, 0,0, 0, 3, 3],
#                        [0, 0, 0, 1, 3]])
