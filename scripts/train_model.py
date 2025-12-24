import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load dataset
df = pd.read_csv("data/seo_dataset.csv")

# Features and target
X = df.drop(columns=["SEO_Score"])
y = df["SEO_Score"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = lgb.LGBMRegressor()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))

# Save model
joblib.dump(model, "models/seo_model.joblib")
print("Model saved to models/seo_model.joblib")
