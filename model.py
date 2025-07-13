# except for the docstrings and this comment, this file did not have any changes from upstream

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    """
    A simple two-layer fully connected neural network used as a Q-function approximator.
    Originally taken from the upstream repo with minimal/no changes.

    Args:
        input_size (int): Dimensionality of the input features.
        hidden_size (int): Number of hidden neurons.
        output_size (int): Number of output actions.
    """
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Forward pass through the network using ReLU activation.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output Q-values for each possible action.
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Save the model's parameters to disk.

        Args:
            file_name (str): Filename for saving the model.
        """
        model_folder_path = './modelsaves'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    """
    Trainer class for the Q-learning model using the Bellman equation.
    Based on the original implementation from the upstream repo.

    Args:
        model (nn.Module): The Q-network to train.
        lr (float): Learning rate.
        gamma (float): Discount factor.
    """
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Perform one training step using the Bellman equation.

        Args:
            state (np.ndarray or torch.Tensor): Current state(s).
            action (np.ndarray or torch.Tensor): Actions taken.
            reward (np.ndarray or torch.Tensor): Rewards received.
            next_state (np.ndarray or torch.Tensor): Resulting state(s).
            done (bool or list of bool): Done flag(s) indicating terminal state.
        """
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
