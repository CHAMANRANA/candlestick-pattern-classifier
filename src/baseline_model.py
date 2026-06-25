import torch.nn as nn
import torch

class TinyVGG(nn.Module) :
    def __init__(self,num_channel:int,hidden_units : int ,output_shape : int)  :
        super().__init__()
        
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=num_channel,out_channels=hidden_units,kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(in_channels=hidden_units,out_channels=hidden_units,kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=hidden_units,out_channels=hidden_units,kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(in_channels=hidden_units,out_channels=hidden_units,kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

        self.fc1 = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=1690,out_features=output_shape))

    def forward(self,x:torch.Tensor) -> torch.Tensor :
        
        return self.fc1(self.conv2(self.conv1(x)))
        

     