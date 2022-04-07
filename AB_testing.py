import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, \
    mannwhitneyu, pearsonr, spearmanr, kendalltau, kruskal, \
    f_oneway
from statsmodels.stats.proportion import proportions_ztest

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: '%.5f' % x)

test_group = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")
control_group = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")

test_group.head()
control_group.head()

test_group.describe().T
control_group.describe().T

df = pd.concat([test_group, control_group], axis=1)

df.columns = ['test_Impression', 'test_Click', 'test_Purchase', 'test_Earning',
              'control_Impression', 'control_Click', 'control_Purchase', 'control_Earning']

# Adım 1: Hipotezi tanımlayınız.
# H0: M1 = M2
# H1: M1 != M2

# Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz
df[["test_Purchase", "control_Purchase"]].mean()

#########################################################
# Hipotez Testinin Gerçekleştirilmesi
#########################################################

# Normallik Varsayımı :

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = shapiro(df["test_Purchase"])
print(f"test_stat: {test_stat}, pvalue: {pvalue}")  # p > 0.05 H0 REDDEDİLEMEZ
test_stat, pvalue = shapiro(df["control_Purchase"])
print(f"test_stat: {test_stat}, pvalue: {pvalue}")  # p > 0.05 H0 REDDEDİLEMEZ

# Varyans Homojenliği :

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.

# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını
# Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu?
# Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = levene(df["test_Purchase"], df["control_Purchase"])
print(f"test_stat: {test_stat}, pvalue: {pvalue}")  # p > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = ttest_ind(df["test_Purchase"], df["control_Purchase"],
                              equal_var=True)
print(f"test_stat: {test_stat}, pvalue: {pvalue}")  # p > 0.05 H0 REDDEDİLEMEZ
# H0: M1 = M2 -     control ve test grubu arasında istatistiksel olarak anlamlı fark yoktur

# Görev 4: Sonuçların Analizi

# Varsayımlar sağlandığı için parametrik t tesi kullandım.
# %95 ihtimalle average bidding'in maximum bidding'den
# daha fazla gelir getirmediğini söyleyebiliriz
