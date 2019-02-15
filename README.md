# idao
International Data Analysis Olympiad - online round

## Short description:
Stacking 2 lightgbm models

## Instruction:
the files are sorted by the order of opening them

### 1)concat_closest_hits_features
#### input: raw dataset
#### description: adds new features that reflect closest hits
#### output: concatenated dataset: raw dataset + new features 
### 2)LGBM
#### input: concatenated dataset
#### description: lightgbm model with data converted to lightgbm Dataset, 5-fold for crossvalidation.
#### HyperParameters:{'random_state':42, 'max_depth':7, 'objective':'binary', 'learning_rate':0.2,'num_leaves':64,'min_data_in_leaf':15, 'num_iterations':90}
#### New features: P-PT, P-PT/P, nan_MatchedHit(if MatchedHit_X and MatchedHit_Y feature is a missing value - Boolean), abs_MatchedHit(absolute value of MatchedHit_X and MatchedHit_Y).
#### Categorical features: encoded by lightgbm
#### output: prediction for validation set and for private test set

### 3)LGBM_dummies

#### input: concatenated dataset
#### description: lightgbm model. Uses 5-fold for crossvalidation. 
#### HyperParameters:{'random_state':42, 'max_depth':9, 'objective':'binary', 'learning_rate':0.2,'num_leaves':128,'min_data_in_leaf':15, 'num_iterations':90}
#### New features: P-PT, P-PT/P, nan_MatchedHit(if MatchedHit_X and MatchedHit_Y feature is a missing value - Boolean), #### abs_MatchedHit(absolute value of MatchedHit_X and MatchedHit_Y), dummies
#### Categorical features: one-hot-encoding
#### output: prediction for validation set and for private test set

### 4)Main

#### input: predictions for validation and private test sets
#### description: logistic regression algorithm that trains on the predictions of lightgbm models for validation set and predicts the label for the test set
#### output: prediction for private test set
