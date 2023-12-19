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


# если считаем верхнюю границу, то знак ПЛЮС, если нижнюю, то МИНУС (+1, -1)
def beta_borders(b, t, sample_variance_y_pow2_s, sample_variance_x_pow2, r, n, sign=1):
    # beta_yx_1 = b_yx - t * ((pow(sample_variance_y_pow2_s, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)) / (
    #             pow(sample_variance_x_pow2_s, 1 / 2) * pow(n - 2, 1 / 2)))
    numerator = pow(sample_variance_y_pow2_s, 1 / 2) * pow(1 - pow(r, 2), 1 / 2)
    denominator = pow(sample_variance_x_pow2, 1 / 2) * pow(n - 2, 1 / 2)

    return b + sign * t * (numerator / denominator)


def fullRegressionProblem(x_i, y_i, n_ij):
    n_i_sum = [10, 12, 24, 8, 6]
    n_j_sum = [5, 6, 11, 25, 9, 4]
    n = 60  # измерять из входных данных

    # print('n_i_sum :',n_i_sum)
    # print('n_j_sum :',n_j_sum)
    # print(n)

    m = len(n_ij[0])  # длина столбца

    x_average = calculate_var_average(x_i, n_i_sum) / n  # X с чертой X среднее
    y_average = calculate_var_average(y_i, n_j_sum) / n  # Y с чертой Y среднее

    print('X average:', x_average)
    print('Y average:', y_average, '\n')

    xy_average = calculate_xy_average(x_i, y_i, n_i_sum, n_j_sum, n_ij) / n  # ХУ с чертой ХУ среднее
    print('XY_average:', xy_average, '\n')

    x_pow2_average = calculate_var_average(x_i, n_i_sum, 2) / n  # Y2 с чертой Y в квадрате среднее
    y_pow2_average = calculate_var_average(y_i, n_j_sum, 2) / n  # X2 с чертой X в квадрате среднее

    print('Y^2_average: ', y_pow2_average, '\t', 'X^2_average: ', x_pow2_average, '\n')

    selective_correlation_moment_m = xy_average - x_average * y_average  # выборочный корреляционный момент (ковариация)
    print('Selective_correlation_moment (M): ', selective_correlation_moment_m, '\n')

    sample_variance_x_pow2_s = x_pow2_average - pow(x_average, 2)  # sample_variance_x_pow2_s выборочная дисперсия
    sample_variance_y_pow2_s = y_pow2_average - pow(y_average, 2)  # sample_variance_y_pow2_s выборочная дисперсия
    print('Sample_variance_x_pow2 (S^2_x): ', sample_variance_x_pow2_s, '\t', 'Sample_variance_y_pow2 (S^2_Y): ',
          sample_variance_y_pow2_s, '\n')

    b_yx = selective_correlation_moment_m / sample_variance_x_pow2_s  # b_yx - коэффициент линейной регрессии y по х
    b_xy = selective_correlation_moment_m / sample_variance_y_pow2_s  # b_xy - коэффициент линейной регрессии x по y
    print('b_yx :', b_yx, '\t', 'b_xy :', b_xy, '\n')

    # Yx=Y_avg+Byx(X-X_avg)
    # Xy=X_avg+Bxy(Y-Y_avg)

    # r=(xy_average-X_avg*Y_avg)/(pow(sample_variance_x_pow2_s,1/2)*pow(sample_variance_y_pow2_s,1/2))# Коэффициент корреляции

    r = pow(abs(b_xy * b_yx), 1 / 2)  # Коэффициент корреляции другая формула
    # Заметная корреляция -0.65, Умеренная - 0.4, слабая -0.2
    print('r: ', r, '\n')

    # Определяем t(1-alpha;n-2) по таблице t=2.01 для P=0.95 и n = 50
    t = 2.01

    # beta_yx будет в следующих границах
    beta_yx_down = beta_borders(b_yx, t, sample_variance_y_pow2_s, sample_variance_x_pow2_s, r, n, -1)
    beta_yx_up = beta_borders(b_yx, t, sample_variance_y_pow2_s, sample_variance_x_pow2_s, r, n)
    # beta_yx_down < beta_yx < beta_yx_up
    print('beta_yx_down: ', beta_yx_down, '\t', 'beta_yx_up: ', beta_yx_up, '\n')

    # beta_xy будет в следующих границах
    beta_xy_down = beta_borders(b_xy, t, sample_variance_x_pow2_s, sample_variance_y_pow2_s, r, n, -1)
    beta_xy_up = beta_borders(b_xy, t, sample_variance_x_pow2_s, sample_variance_y_pow2_s, r, n)
    # beta_xy_down < beta_xy < beta_xy_up
    print('beta_xy_down :', beta_xy_down, '\t', 'beta_xy_up :', beta_xy_up, '\n')

    z = (1 / 2) * (math.log(abs((1 + r) / (1 - r)), math.exp(1)))  # z-преобразование
    print('z: ', z, '\n')

    # selective_correlation_moment_m будет в следующих границ
    mathematical_expectation_m_down = z - t / (pow(n - 3, 1 / 2))  # Мат. ожидание (нижняя граница)
    mathematical_expectation_m_up = z + t / (pow(n - 3, 1 / 2))  # Мат. ожидание (верхняя граница)
    print('mathematical_expectation_m_down :', mathematical_expectation_m_down,
          '\t',
          'mathematical_expectation_m_up :', mathematical_expectation_m_up, '\n'
          )

    # p будет в следующих границ
    p_1 = (math.exp(mathematical_expectation_m_down) - math.exp(-mathematical_expectation_m_down)) / (
            math.exp(mathematical_expectation_m_down) + math.exp(
        -mathematical_expectation_m_down))  # Генеральный коэффициент корреляции(нижняя граница)
    p_2 = (math.exp(mathematical_expectation_m_up) - math.exp(-mathematical_expectation_m_up)) / (
            math.exp(mathematical_expectation_m_up) + math.exp(
        -mathematical_expectation_m_up))  # Генеральный коэффициент корреляции(верхняя граница)
    print('p_1 :', p_1, 'p_2 :', p_2)

    Yi_avg = []  # Yi с чертой групповое среднее
    Xi_avg = []  # Xi с чертой групповое среднее

    for i in range(len(n_j_sum)):
        Xi_avg.append(0)
        for j in range(len(n_i_sum)):
            Xi_avg[i] += x_i[j] * n_ij[j][i]
            # print('X' + str(i+1) + ':', Xi[j], nij[j][i])
        Xi_avg[i] = Xi_avg[i] / n_j_sum[i]
        # print('n_j_sum',n_j_sum[i])

    print('Xi_avg :', Xi_avg)
    for i in range(len(n_i_sum)):
        Yi_avg.append(0)
        for j in range(len(n_j_sum)):
            # print('Y' + str(i+1) + ':', Yi[j], nij[i][j])
            Yi_avg[i] += y_i[j] * n_ij[i][j]
        Yi_avg[i] = Yi_avg[i] / n_i_sum[i]

    print('Yi_avg :', Yi_avg)

    # Yi_avg=[0.7,2.1,3.5,4.9,6.3,7.7]#Yi с чертой групповое среднее
    # Xi_avg = [2.25,6.75,11.25,15.75,20.25]#Xi с чертой групповое среднее

    б2_iy = 0  # Не знаю название переменной, напиши если знаешь)
    б2_ix = 0  # Не знаю название переменной, напиши если знаешь)

    for i in range(len(n_j_sum)):
        б2_ix += pow((Xi_avg[i] - x_average), 2) * n_j_sum[i]
        # print(Xi_avg[i],n_j_sum[i])
    for i in range(len(n_i_sum)):
        # print(Yi_avg[i], n_i_sum[i])
        б2_iy += pow((Yi_avg[i] - y_average), 2) * n_i_sum[i]

    б2_iy = б2_iy / n
    б2_ix = б2_ix / n
    print('б2_iy', б2_iy, 'б2_ix', б2_ix)

    nyx = pow(б2_iy / sample_variance_y_pow2_s, 1 / 2)  # Корреляционное отношение y по x
    nxy = pow(б2_ix / sample_variance_x_pow2_s, 1 / 2)  # Корреляционное отношение x по y
    print('nyx :', nyx, 'nxy :', nxy)

    Yxi = []  # Не знаю название переменной, напиши если знаешь)
    Xyj = []  # Не знаю название переменной, напиши если знаешь)
    for i in range(len(n_i_sum)):
        Yxi.append(0)
        Yxi[i] += y_average + b_yx * (x_i[i] - x_average)
    for j in range(len(n_j_sum)):
        Xyj.append(0)
        Xyj[j] += x_average + b_xy * (y_i[j] - y_average)
    print('Yxi :', Yxi, 'Xyi :', Xyj)  # проверить, нет ли ошибки, сравнить с заданными x y

    б2_x = 0  # Не знаю название переменной, напиши если знаешь)
    б2_y = 0  # Не знаю название переменной, напиши если знаешь)

    for i in range(len(Xyj)):
        б2_x += pow(Xyj[i] - x_average, 2) * n_j_sum[i]
        print(Xyj[i], n_j_sum[i])
    for j in range(len(Yxi)):
        б2_y += pow(Yxi[j] - y_average, 2) * n_i_sum[j]
    б2_x = б2_x / n
    б2_y = б2_y / n
    print('б2_x :', б2_x, 'б2_y :', б2_y)

    # Rxy - множественный коэффициент корелляционного значения
    Ryx = pow(б2_y / sample_variance_y_pow2_s, 1 / 2)  # Не знаю название переменной, напиши если знаешь)
    Rxy = pow(б2_x / sample_variance_x_pow2_s, 1 / 2)  # Не знаю название переменной, напиши если знаешь)
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
