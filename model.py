import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision.models as models
import torchvision.utils as tvutils

import utils

class ContentLoss(nn.Module):
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.loss = F.mse_loss(self.target, self.target )

    def forward(self, input):
        self.loss = F.mse_loss(input, self.target)
        return input

class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = utils.gram_matrix(target_feature).detach()
        self.loss = F.mse_loss(self.target, self.target)

    def forward(self, input):
        G = utils.gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input
        
class NST_Model():
    def __init__(self, style_img, content_img, input_img,
                 cnn=models.vgg19(pretrained=True).features.eval(),
                 mean=[0.485, 0.456, 0.406],
                 std=[0.229, 0.224, 0.225],
                 imsize=512,
                 content_layers=['conv_4'],
                 style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']):
    
        self.mean = mean
        self.std = std
        self.imsize = imsize
        
        self.normalization = utils.Normalization(self.mean, self.std)
        self.loader = utils.loader
        self.gram_matrix = utils.gram_matrix
        
        self.cnn = cnn
        self.content_layers = content_layers
        self.style_layers = style_layers
        
        self.style_img = style_img
        self.content_img = content_img
        self.input_img = input_img
        
        self.style_img = self.loader(self.style_img, self.imsize)
        self.content_img = self.loader(self.content_img, self.imsize)
        self.input_img = self.loader(self.input_img, self.imsize)
        self.optimizer = utils.get_input_optimizer(self.input_img)
        
    def get_style_model_and_losses(self):
        content_losses = []
        style_losses = []
        
        model = nn.Sequential(self.normalization)
        
        i = 0
        for layer in self.cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            elif isinstance(layer, nn.BatchNorm2d):
                name = 'bn_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

            model.add_module(name, layer)

            if name in self.content_layers:
                target = model(self.content_img).detach()
                content_loss = ContentLoss(target)
                model.add_module("content_loss_{}".format(i), content_loss)
                content_losses.append(content_loss)

            if name in self.style_layers:
                target_feature = model(self.style_img).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module("style_loss_{}".format(i), style_loss)
                style_losses.append(style_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses
        
    async def run_style_transfer(self, num_steps=150, style_weight=100000,
                           content_weight=1):
                            
        model, style_losses, content_losses = self.get_style_model_and_losses()
        optimizer = self.optimizer
        
        run = [0]
        while run[0] <= num_steps:

            def closure():
                self.input_img.data.clamp_(0, 1)

                optimizer.zero_grad()

                model(self.input_img)

                style_score = 0
                content_score = 0

                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss
            
                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                run[0] += 1
                if run[0] % 50 == 0:
                    print("run {}:".format(run))
                    print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                        style_score.item(), content_score.item()))
                    print()

                return style_score + content_score

            optimizer.step(closure)

        self.input_img.data.clamp_(0, 1)
        tvutils.save_image(self.input_img, 'images/output.jpg')

        return self.input_img
