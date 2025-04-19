from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def TSmodel(df):
    features = ['temperature_celsius', 'humidity', 'uv_index',
                'air_quality_pm10', 'air_quality_nitrogen_dioxide',
                'air_quality_carbon_monoxide']
    X = df[features]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    n_epochs = 5
    accuracies = []

    for epoch in range(1, n_epochs + 1):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        accuracies.append(acc)

        print(f"Етап {epoch}/{n_epochs} - Точність: {acc:.2f}")

    joblib.dump(model, "air_model.pkl")
    
    return accuracies[-1]
