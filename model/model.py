
# ! pip3 install torch


import torch
import torch.nn as nn
import torch.optim as optim



# Pseudo data
years = [2018, 2018, 2019, 2019, 2020, 2020]
months = [1, 2, 3, 4, 5, 6]
temperatures = [23.5, 24.7, 18.2, 20.5, 22.1, 25.0]
accidents = [10, 15, 8, 12, 11, 13]

# Convert the lists to PyTorch tensors
X = torch.tensor(list(zip(years, months, temperatures)), dtype=torch.float32)
y = torch.tensor(accidents, dtype=torch.float32)

# Standardize the input features
X_mean = torch.mean(X, dim=0)
X_std = torch.std(X, dim=0)
X_standardized = (X - X_mean) / X_std




# Define the model
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(3, 1)  # 3 input features and 1 output

    def forward(self, x):
        return self.linear(x)



# Initialize the model
model = LinearRegression()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)




# Train the model
num_epochs = 1000

for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_standardized)
    loss = criterion(outputs, y)

    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}')
        



# inference
new_data = torch.tensor([[2023, 7, 27.3]], dtype=torch.float32) # 27.3 degrees on July 2023
standardized_new_data = (new_data - X_mean) / X_std
predicted = model(standardized_new_data)

# Print the predicted amount of accidents
print(f'Predicted amount of accidents: {predicted.item():.2f}')
