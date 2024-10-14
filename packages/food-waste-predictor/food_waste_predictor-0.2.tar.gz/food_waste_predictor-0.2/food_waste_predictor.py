import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import argparse

# Step 1: Load and Prepare Data
data = pd.DataFrame({
    'Household Size': [2, 4, 3, 1, 5, 2, 3],
    'Food Type': ['Fruits', 'Vegetables', 'Dairy', 'Fruits', 'Vegetables', 'Dairy', 'Fruits'],
    'Amount Purchased': [3, 5, 2, 1, 7, 4, 6],
    'Amount Wasted': [0.5, 1.0, 0.3, 0.1, 1.2, 0.8, 0.9]
})

# Convert 'Food Type' to numeric using one-hot encoding
data = pd.get_dummies(data, columns=['Food Type'], drop_first=True)

# Step 2: Split Data into Features (X) and Target (y)
X = data.drop('Amount Wasted', axis=1)
y = data['Amount Wasted']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train a Simple Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: Evaluate the Model (optional for debugging)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae:.2f}')

# Step 5: Create a Prediction Function
def predict_food_waste(household_size, amount_purchased, food_type):
    # Initialize the input vector with zeros
    food_type_encoded = [0, 0]  # Two food types: Vegetables and Dairy

    # Set the food type encoding based on the input
    if food_type == 'Fruits':
        food_type_encoded = [0, 0]  # [0, 0] for Fruits (drop_first=True)
    elif food_type == 'Vegetables':
        food_type_encoded = [1, 0]  # [1, 0] for Vegetables
    elif food_type == 'Dairy':
        food_type_encoded = [0, 1]  # [0, 1] for Dairy
    else:
        raise ValueError("Invalid food type. Choose from 'Fruits', 'Vegetables', 'Dairy'.")

    # Construct the input data
    input_data = [[household_size, amount_purchased] + food_type_encoded]
    
    # Make the prediction
    predicted_waste = model.predict(input_data)
    return predicted_waste[0]

# Step 6: Command-Line Interface
def cli():
    print("Welcome to the Food Waste Prediction Tool!")

    # Get inputs from the user
    household_size = int(input("Enter Household Size (e.g., 2, 3, 4): "))
    food_type = input("Enter Food Type (choose from 'Fruits', 'Vegetables', 'Dairy'): ")
    amount_purchased = float(input("Enter Amount Purchased (in kg): "))

    # Predict and display the result
    try:
        waste = predict_food_waste(household_size, amount_purchased, food_type)
        print(f"\nPredicted Food Waste: {waste:.2f} kg")
    except ValueError as e:
        print(e)

# Run the CLI
if __name__ == "__main__":
    cli()
