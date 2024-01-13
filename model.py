import torch
import torch.nn as nn
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, save_folder):
        super(Linear_QNet, self).__init__()
        self.hidden_size = hidden_size
        self.linear_in = nn.Linear(input_size, hidden_size[0])
        self.linear_out = nn.Linear(hidden_size[-1], output_size)
        self.save_folder = save_folder

    def forward(self, x):
        x = F.relu(self.linear_in(x))
        prev_size = self.hidden_size[0]
        for size in self.hidden_size[1:]:
            linear = nn.Linear(prev_size, size)
            prev_size = size
            x = linear(x)

        x = self.linear_out(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = self.save_folder
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

