from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


def train_model(X_train, y_train):
    """Train Logistic Regression model"""
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate ML model"""
    predictions = model.predict(X_test)

    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    return predictions, report, matrix