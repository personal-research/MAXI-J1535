import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor

wh1 = False

if wh1: 
    plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
else: 
    plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

sns.set_context("paper") #font_scale=
sns.set_palette('deep')
seaborn_colors = sns.color_palette('deep')

plt.rcParams['font.family'] = 'serif'
plt.rcParams["mathtext.fontset"] = "dejavuserif"

#bi_cm = LinearSegmentedColormap.from_list("Custom", [seaborn_colors[0], (1,1,1), seaborn_colors[3]], N=20)

def regression_pipeline(source:str, models:list, model_names:list,
                        qpo_path:str, context_path:str, repository_path:str,
                        qpo_preprocess_dict:dict, context_preprocess_dict:dict,
                        model_hyperparameter_dictionaries:list,spectrum:bool=False,
                        model_comparison_statistic:str='mae', k:int=10, repetitions:int=2, fold:int=0, wh1=wh1,
                        units:dict={'frequency':'Hz'}):

    r''' 
    model_comparison_statistic : str
        either 'mae' or 'mse' 

    '''

    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml import collection
    from qpoml.plotting import plot_model_comparison
    from qpoml.utilities import compare_models

    #plt.rcParams["mathtext.fontset"] = "dejavuserif"
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')

    # 1: Preparation for Pipeline # 

    model_n = len(models)

    all_gridsearch_scores = []
    source_observation_counts = []

    alphabet = [str(chr(letter)).upper() for letter in range(97,123)] 

    if repository_path[-1]!='/':
        repository_path!='/'

    qpo_path = f'{repository_path}{qpo_path}' 
    context_path = f'{repository_path}{context_path}'

    # 2: Source-wise Machine Learning #

    n_total_qpos = len(pd.read_csv(qpo_path).index)
    n_test = int(n_total_qpos/k)
    n_train = n_total_qpos-n_test

    fold_performances = []
    gridsearch_scores = []

    # 2.1: Machine Learning for Each Model # 

    for model_index, model in enumerate(models):

        model_name = model_names[model_index]

        notation_string = f'[{model_name}][{source}][{spectrum}]'

        collec = collection()
        collec.load(qpo_csv=qpo_path, context_csv=context_path,
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

        # 2.1.1: GridSearch # 

        scores, _, _, best_params = collec.gridsearch(model=model, parameters=model_hyperparameter_dictionaries[model_index])

        column_names = list(best_params.keys())
        columns = [[i] for i in list(best_params.values())]

        best_configuration_df = pd.DataFrame()

        for temp_index in range(len(column_names)):
            best_configuration_df[column_names[temp_index]] = columns[temp_index]

        if source.replace('_',' ') == 'GRS 1915+905': 
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/GRS_1915+105/{notation_string}_BestParams.csv', index=False)
        else: 
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}_BestParams.csv', index=False)
        
        # 2.1.2: k-fold on Best Configuration # 

        collec.evaluate(model=model, evaluation_approach='k-fold', folds=k, repetitions=repetitions, hyperparameter_dictionary=best_params) # evaluate-approach???

        # 2.1.3: Save and Plot Performance Across Folds # 

        statistics = collec.get_performance_statistics()

        fold_performance_df = pd.DataFrame.from_dict(statistics)
        fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
        if source.replace('_',' ') == 'GRS 1915+905': 
            temp_path = f'{repository_path}final-push/output/pipeline/GRS_1915+105/{notation_string}_k-fold.csv'
        else: 
            temp_path = f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}_k-fold.csv'
        
        fold_performance_df.to_csv(temp_path, index=False)

        fold_performances.append(list(fold_performance_df[model_comparison_statistic]))

        # 2.1.4: Plot Results Regression from 10th Fold # 
        fig, ax = plt.subplots(figsize=(4,4))

        collec.plot_results_regression(feature_name='frequency', which=[0], ax = ax, fold=fold)
        temp_path = f'{repository_path}manuscript/figures/individual/figure_6/{notation_string}[results_regression][fold={fold}]'
        plt.savefig(f'{temp_path}.pdf')
        plt.savefig(f'{temp_path}.png', dpi=200)
        plt.close()

        # 2.1.5: Plot Feature Importances from fold-th Fold # 
        fig, ax = plt.subplots(figsize=(6,6))
        
        collec.plot_feature_importances(model=model, fold=fold, kind='tree-shap', style='box', ax=ax, save_path=imps_path)
        
        temp_path = None 

        if source.replace('_',' ') == 'GRS 1915+105':
            temp_path = f'{repository_path}manuscript/figures/individual/figure_8/{notation_string}[feature_importances][fold={fold}]'
        else: 
            temp_path = f'{repository_path}manuscript/figures/individual/figure_9/{notation_string}[feature_importances][fold={fold}]'    
        
        plt.savefig(f'{temp_path}.pdf')
        plt.savefig(f'{temp_path}.png', dpi=200)
        plt.close()

    # 2.2: All-Models One Source Results # 

    # 2.2.1: Plot Performances for all Models #
    fig, ax = plt.subplots()
    print(model_names, len(fold_performances))
    plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax, cut=0)
    temp_path = f'{repository_path}manuscript/figures/individual/figure_4/[{notation_string}][model-comparison]'
    plt.savefig(f'{temp_path}.pdf') 
    plt.savefig(f'{temp_path}.png', dpi=200) 
    plt.close()
    
    # ignore
    sns.set_context(font_scale=0.7)
    fig, ax = plt.subplots()
    print(model_names, len(fold_performances))
    plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax)
    temp_path = f'{repository_path}manuscript/figures/individual/figure_4/{notation_string}[model_comparison:no-cut]'
    plt.savefig(f'{temp_path}.pdf') 
    plt.savefig(f'{temp_path}.png', dpi=200) 
    plt.close()

    # 2.2.2: Pairwise Statistical Model Comparison # 
    first_model_names, second_model_names = ([], []) 
    t_values, p_values = ([], []) 
    first_better_probabilities, second_better_probabilities = ([], []) 

    for i, first_score_list in enumerate(fold_performances):
        first_name = model_names[i]
        for j in range(i+1, model_n):
            print(i,j)

            second_score_list = fold_performances[j]

            second_name = model_names[j]

            first_model_names.append(first_name)
            second_model_names.append(second_name)

            t, p = compare_models(first_score_list, second_score_list, n_train=n_train, n_test=n_test, approach='frequentist')
            first_better, second_better, _, _ = compare_models(first_score_list, second_score_list, n_train=n_train, n_test=n_test, approach='bayesian')
        
            t_values.append(t)
            p_values.append(p)
            first_better_probabilities.append(first_better)
            second_better_probabilities.append(second_better)

        temp_columns = [first_model_names, second_model_names, t_values, p_values, first_better_probabilities, second_better_probabilities]
        temp_names = ['First Model Name', 'Second Model Name', 't', 'p', '% Chance First Better', '% Chance Second Better']
        
        pairwise_results_df = pd.DataFrame()
        for i in range(len(temp_columns)): 
            pairwise_results_df[temp_names[i]] = temp_columns[i]
        
        temp_path = f'{repository_path}manuscript/tables/{notation_string}[pairwise-comparison]'
        
        pairwise_results_df.to_csv(f'{temp_path}.csv', index=False)
        pairwise_results_df.to_latex(f'{temp_path}.tex', index=False, float_format="%.2f")

        # 2.3: Prepare for Step 3 # 

        all_gridsearch_scores.append(gridsearch_scores)

def classification_pipeline(source:str, models:list, model_names:list,repository_path:str,
                            scalar_context_path:str, qpo_path:str, 
                            model_hyperparameter_dictionaries:list,
                            context_preprocess_dictionary:dict, wh1=wh1, fold:int=0,
                            k:int=10, repetitions:int=2, spectrum:bool=False): 
    
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml import collection
    from qpoml.utilities import roc_and_auc
    from qpoml.plotting import plot_roc

    # 1. Preparation for Pipeline #
    
    all_gridsearch_scores = []
    source_observation_counts = []

    if repository_path[-1]!='/':
        repository_path+='/'
    
    qpo_path = f'{repository_path}{qpo_path}' 
    context_path = f'{repository_path}{context_path}'

    # 2: Source-wise Machine Learning #

    n_total_qpos = len(pd.read_csv(qpo_path).index)
    print('Number of QPOs:', n_total_qpos)

    gridsearch_scores = []

    # MAKE GRID SEARCH SCORES PLOT? # 

    source_observation_counts.append(len(pd.read_csv(scalar_context_path).index))
    print('Source Observation Counts', source_observation_counts)

    for model_index, model in enumerate(models):

        model_name = model_names[model_index]

        notation_string = f'[{model_name}][{source}][{spectrum}]'

        collec = collection()
        collec.load(qpo_csv=qpo_path, context_csv=scalar_context_path, context_preprocess=context_preprocess_dictionary, approach='classification', units={'frequency':'hz'})
        
        scores, _, _, best_params = collec.gridsearch(model=model, parameters=model_hyperparameter_dictionaries[model_index])

        column_names = list(best_params.keys())
        columns = [[i] for i in list(best_params.values())]

        best_configuration_df = pd.DataFrame()

        for temp_index in range(len(column_names)):
            best_configuration_df[column_names[temp_index]] = columns[temp_index]

        if source.replace('_',' ') == 'MAXI J1535-571':
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}[BestParams].csv', index=False)
        gridsearch_scores.append(scores)
        
        collec.evaluate(model=model, evaluation_approach='k-fold', folds=k, stratify=True, repetitions=repetitions, hyperparameter_dictionary=best_params)

        # .1 Confusion Matrix # 


        if wh1: 
            plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
        else: 
            plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

        sns.set_context('paper')
        fig, ax = plt.subplots(figsize=(4,4))
        y_set = list(set(np.array(collec.y_test).flatten()))
        cm_labels = None
        cm_type = None
        if len(y_set) == 2:
            labels = ['No QPO', 'QPO']
            cm_type = 'binary'

        else: 
            labels = [f'{counter} QPO' for counter in y_set]
            cm_type = 'multinomial'

        collec.plot_confusion_matrix(fold=fold, ax=ax, labels=labels)

        cm_path = f'{repository_path}manuscript/figures/individual/figure_7/{notation_string}[confusion_matrix:type={cm_type}]'
        fig.tight_layout()
        plt.savefig(f'{cm_path}.pdf')
        plt.savefig(f'{cm_path}.png', dpi=200)

        plt.clf()
        plt.close()

        # .2 ROC Curve # 
        if cm_type == 'binary':
            fig, ax = plt.subplots(figsize=(4,4))
            if wh1: 
                plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
            else: 
                plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
            sns.set_context('paper')
            fpr, tpr, std_tpr, auc, std_auc = collec.roc_and_auc()
            plot_roc(fpr=fpr, tpr=tpr, std_tpr=std_tpr, auc=auc, ax=ax, std_auc=std_auc)

            roc_path = f'{repository_path}manuscript/figures/individual/figure_7/{notation_string}[ROC]'
            fig.tight_layout()
            plt.savefig(f'{roc_path}.pdf')
            plt.savefig(f'{roc_path}.png', dpi=200)

        # .3 Feature Importances # 

        fig, ax = plt.subplots(figsize=(4,4))
        if wh1: 
            plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
        else: 
            plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
        
        sns.set_context('paper')
        collec.plot_feature_importances(model, fold=fold, style='box', ax=ax, kind='tree-shap')
        fi_path = f'{repository_path}manuscript/figures/individual/figure_9/{notation_string}[Feature-Importances]'
        fig.tight_layout()
        plt.savefig(f'{fi_path}.pdf')
        plt.savefig(f'{fi_path}.png', dpi=200)

        # save predictions, etc. 
        statistics = pd.DataFrame(collec.get_performance_statistics())
        if source.replace('_',' ') == 'MAXI J1535-571':
            pd.DataFrame(statistics).to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}[Performance_stats].csv', index=False)

model_hyperparameter_dictionaries = [{'normalize':[True, False]},
                                     {'min_samples_split':[4,6], 'min_samples_leaf':[3]}, 
                                     {'min_samples_split': [4,6], 'min_samples_leaf':[1]},
                                     {'min_samples_split':[4,6], 'min_samples_leaf':[1]}, 
                                     {'n_estimators':[500,1000], 'eta':[0.1]}]
print('starting')

# ROUND ONE: GRS REGRESSION # 

regression_pipeline(source='GRS 1915+905', 
                    models=[LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor(), ExtraTreesRegressor(), XGBRegressor()], 
                    model_names=['Linear', 'DT', 'RF', 'ET', 'XGBoost'], 
                    qpo_path='final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv', 
                    context_path='final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv', 
                    qpo_preprocess_dict={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}, 
                    context_preprocess_dict={'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}, 
                    model_hyperparameter_dictionaries=model_hyperparameter_dictionaries)

# ROUND FOUR: MAXI CLASSIFICATION, SCALAR INPUT

classification_pipeline(source='MAXI J1535-571', 
                        models=[RandomForestClassifier(), LogisticRegression()], 
                        model_names=['Random Forest', 'Logistic Regression'], 
                        scalar_context_path='final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv', 
                        qpo_path='final-push/data/pipeline/classification/MAXI_J1535-571_QPO-Input.csv',
                        model_hyperparameter_dictionaries=[{'n_estimators':[50,100,200]}, 
                                                           {'penalty':['l2'], 'C':[1, 5]}], 
                        context_preprocess_dictionary={'A':'normalize', 'B':'normalize', 'C':'normalize', 'D':'normalize', 'E':'normalize', 'F':'normalize', 'G':'normalize'}, 
                        )