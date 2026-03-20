# BMI Calculator
def calculate_bmi(weight, height):
    bmi = weight /(height ** 2)
    return bmi

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Get user input
weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))

# Calculate
bmi = calculate_bmi(weight, height)
category = classify_bmi(bmi)

# Display result
print(f"\nYour BMI is: {bmi:.2f}")
print(f"Category: {category}")
