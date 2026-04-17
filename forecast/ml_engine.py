import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sales.models import SalesRecord

def train_and_predict(current_temp, current_day):
    data = SalesRecord.objects.all().values('quantity', 'temp_c', 'sale_date')
    if not data or len(data) < 5: 
        return None

    df = pd.DataFrame(data)

    df['day_of_week'] = pd.to_datetime(df['sale_date']).dt.dayofweek

    X = df[['temp_c', 'day_of_week']]
    y = df['quantity']

    model = LinearRegression()
    model.fit(X, y) 


    input_data = np.array([[current_temp, current_day]])
    prediction = model.predict(input_data)
    print(f"📊 Rows: {len(df)}")
    print(f"🌡️ Temp range: {df['temp_c'].min():.1f}°C to {df['temp_c'].max():.1f}°C")
    print(f"📈 Temp coefficient: {model.coef_[0]:.4f}")
    print(f"🎯 Prediction for {current_temp}°C: {round(prediction[0])}")
    return round(prediction[0])
