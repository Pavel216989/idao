import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import KFold


def train_lgb(train_df: pd.DataFrame, test_df: pd.DataFrame,
              train_features: list, categorical_features: list, 
              hyper_parameters: dict, n_folds: int = 5):
    """
    Train Lightgbm model using k-folds cross-validation for stacking method.
    :param train_df: Train Dataframe
    :param test_df: Test Dataframe
    :param train_features: names of training features
    :param categorical_features: names of categorical features
    :param hyper_parameters: lightgbm hyperparameters
    :param n_folds: number of folds for k-folds
    :return: y_validation, validation_predictions, mean_predictions
    """
    
    kf = KFold(n_splits = n_folds, random_state = 41, shuffle = True)
    
    validation_predictions = []
    test_predictions = []
    y_validation = []
    
    for train_index, test_index in kf.split(train_df):

        X_train, X_val = train_df.loc[train_index], train_df.loc[test_index]
        y_train, y_val = train_df.label[train_index], train_df.label[test_index]
        y_validation.extend(y_val)

        train_data = lgb.Dataset(X_train[train_features+categorical_features], 
                             label=y_train, weight=X_train.weight, 
                             feature_name=train_features+categorical_features, 
                             categorical_feature=categorical_features)

        model = lgb.train(hyper_parameters, train_data)
        # predictions on validation set
        prediction = model.predict(X_val[train_features+categorical_features])
        validation_predictions.extend(prediction)
        # predictions on test set
        prediction_test = model.predict(test_df[train_features+categorical_features])
        test_predictions.extend(list(prediction_test))
        
    # Average test_predictions
    test_predictions = np.array(test_predictions)
    mean_predictions = test_predictions.mean(axis=0)
    
    return y_validation, validation_predictions, mean_predictions