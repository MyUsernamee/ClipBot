
import torch
import clip

model, preprocess = clip.load("ViT-B/32") # Only run once

def compareImages(images1, images2, device="cuda"):

    # Convert images to tensors if they are not already
    if not isinstance(images1, torch.Tensor):
        images1 = [preprocess(image).unsqueeze(0).to(device) for image in images1]
        images1 = torch.cat(images1, dim=0)
    if not isinstance(images2, torch.Tensor):
        images2 = [preprocess(image).unsqueeze(0).to(device) for image in images2]
        images2 = torch.cat(images2, dim=0)

    # Encode the images
    images1 = model.encode_iamge(images1)
    images2 = model.encode_iamge(images2)

    # Normalize the images
    images1 = images1 / images1.norm(dim=1, keepdim=True)
    images2 = images2 / images2.norm(dim=1, keepdim=True)

    # cosine similarity as logits
    logit_scale = model.logit_scale.exp()
    logits_per_image = logit_scale * images1 @ images2.t()

    # cosine similarity as probabilities
    probs_per_image = torch.softmax(logits_per_image, dim=-1)

    return probs_per_image

def embedImage(image, device="cuda"):

    # Convert image to tensor if it is not already
    if not isinstance(image, torch.Tensor):
        image = preprocess(image).unsqueeze(0).to(device)

    # Encode the image
    image = model.encode_iamge(image)

    return image