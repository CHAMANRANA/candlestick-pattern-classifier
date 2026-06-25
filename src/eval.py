import torchvision
import torch
from PIL import Image

def image_eval(model : torch.nn.Module ,
               model_weights_path : str ,
               uploaded_image) :
    
    classes = ["bearish","bullish","neutral"]

    transfroms = torchvision.transforms.Compose([
    torchvision.transforms.Resize(size=(224,224)),
    torchvision.transforms.ToTensor()
])

    model.load_state_dict(torch.load(model_weights_path))
    img = Image.open(uploaded_image).convert('RGB')
    trans_img = (transfroms(img))

    model.eval()
    with torch.inference_mode() :
        logits = model(trans_img.unsqueeze(dim=0))

    return f"The image gives {classes[torch.argmax(logits,dim=1)]} signal with a probability of {torch.softmax(logits,dim=1)}" 

