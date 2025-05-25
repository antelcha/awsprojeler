
import argparse
import os
import pandas as pd
import xgboost as xgb
import joblib

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_round', type=int, default=100)
    parser.add_argument('--max_depth', type=int, default=6)
    parser.add_argument('--eta', type=float, default=0.1)
    parser.add_argument('--subsample', type=float, default=0.8)
    parser.add_argument('--colsample_bytree', type=float, default=0.8)
    parser.add_argument('--objective', type=str, default='reg:squarederror')
    
    parser.add_argument('--model_dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Veriyi yükle
    train_data = pd.read_csv(os.path.join(args.train, 'train.csv'), header=None)
    
    # Target ve features
    y = train_data.iloc[:, 0]
    X = train_data.iloc[:, 1:]
    
    # XGBoost training
    dtrain = xgb.DMatrix(X, label=y)
    
    params = {
        'objective': args.objective,
        'max_depth': args.max_depth,
        'eta': args.eta,
        'subsample': args.subsample,
        'colsample_bytree': args.colsample_bytree
    }
    
    model = xgb.train(params, dtrain, num_boost_round=args.num_round)
    
    # Model kaydet
    model.save_model(os.path.join(args.model_dir, 'xgboost-model'))

if __name__ == '__main__':
    main()
