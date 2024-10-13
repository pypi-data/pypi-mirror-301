import torch


def get_optimizer(client_optimizer, params, **kwargs):
    if client_optimizer == "adam":
        optimizer = torch.optim.Adam(params, **kwargs)
    elif client_optimizer == "sgd":
        optimizer = torch.optim.SGD(params, **kwargs, momentum=0.9)
    elif client_optimizer == "adamw":
        optimizer = torch.optim.AdamW(params, **kwargs)
    else:
        raise NotImplementedError(
            "Optimizer %s not supported." % client_optimizer)
    return optimizer


def get_lr_scheduler(lr_scheduler, optimizer, args):
    if lr_scheduler == "StepLR":
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer, step_size=20, gamma=0.1)
    elif lr_scheduler == "CosineAnnealingLR":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, args.epochs)
    else:
        raise NotImplementedError(
            "LearningRate Scheduler %s not supported." % lr_scheduler
        )
    return scheduler


def adjust_learning_rate(optimizer, epoch, lr):
		if epoch < 2:
			lr = lr
		elif epoch < 20:
			lr = 0.1  * lr
		elif epoch < 30:
			lr = 0.01 * lr 
		else:
			lr = 0.01 * lr
		print('epoch: {}  lr: {:.4f}'.format(epoch, lr))
		for param_group in optimizer.param_groups:
			param_group['lr'] = lr