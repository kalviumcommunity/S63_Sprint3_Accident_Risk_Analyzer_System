# Phase 4 - Machine Learning Model

## Scope
- Split encoded dataset into features and target
- Train RandomForestClassifier
- Predict and evaluate model accuracy
- Save model artifact for later use

## Run
python 04_Machine_Learning/run_phase4_model_training.py

## Outputs
- data/models/accident_random_forest_model.joblib
- 04_Machine_Learning/model_evaluation.txt

## Notes
- If the encoded dataset is missing, the runner regenerates it from MongoDB using the Phase 3 preprocessing utilities.
- Because the dataset is very small, a 50/50 train-test split is used for a more balanced evaluation.
