from qpoml import collection
import matplotlib.pyplot as plt  
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Lasso, LinearRegression
import seaborn as sns

spectrum_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt'
qpo_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/qpo_summary_for_qpoml.txt'

collection_one = collection()
context_preprocess = {'net_count_rate':'normalize','gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}
collection_one.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',
                    context_preprocess=context_preprocess,
                    qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

regr = ExtraTreesRegressor()
collection_one.evaluate(model=regr, model_name='ExtraTreesRegressor', evaluation_approach='k-fold', folds=20)

collection_two = collection()
collection_two.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',
                    context_preprocess=context_preprocess,
                    qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

regr = Lasso(alpha=0.1)
collection_two.evaluate(model=regr, model_name='LASSO', evaluation_approach='k-fold', folds=20)

collection_three = collection()
collection_three.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',
                    context_preprocess=context_preprocess,
                    qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

regr = LinearRegression()
collection_three.evaluate(model=regr, model_name='LinearRegression', evaluation_approach='k-fold', folds=20)

# PLOTTING # 

sns.set_style('darkgrid')
sns.set_context("paper", font_scale=0.5) #font_scale=
sns.set_palette('deep')

fig, ax = plt.subplots(figsize=(6,6))

collection_one.plot_correlation_matrix(ax=ax)

plt.tight_layout()

plt.savefig('./final-push/src/organize/with count rate/correlation_matrix_no_red_chi.png', dpi=150)

sns.set_style('darkgrid')
sns.set_context("paper", font_scale=0.5) #font_scale=
sns.set_palette('deep')

fig, axs = plt.subplots(5,2, figsize=(8,20))
                             
for i in range(0,5):
    collection_one.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_one.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i+5)

plt.tight_layout()
plt.savefig('./final-push/src/organize/with count rate/extra_trees_results_regression_no_red_chi.png', dpi=150)

sns.set_style('darkgrid')
sns.set_context("paper", font_scale=0.5) #font_scale=
sns.set_palette('deep')

fig, axs = plt.subplots(5,2, figsize=(8,20))
                             
for i in range(0,5):
    collection_two.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_two.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i+5)

plt.tight_layout()
plt.savefig('./final-push/src/organize/with count rate/lasso_results_regression_no_red_chi.png', dpi=150)

sns.set_style('darkgrid')
sns.set_context("paper", font_scale=0.5) #font_scale=
sns.set_palette('deep')

fig, axs = plt.subplots(5,2, figsize=(8,20))
                             
for i in range(0,5):
    collection_three.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_three.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i+5)

plt.tight_layout()
plt.savefig('./final-push/src/organize/with count rate/linear_regression_results_regression_no_red_chi.png', dpi=150)
