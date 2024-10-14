from tqdm import tqdm


def eval_def_acc(is_clean_lst, dataset):
    tp, tn, fp, fn = 0, 0, 0, 0
    for idx, is_clean in enumerate(tqdm(is_clean_lst, desc="counting results")):
        *_, is_poison, pre_label = dataset[idx]

        # true positive, poison sample classified as poison sample
        if is_poison == 1 and is_clean == 0:
            tp += 1
        # true negative, clean sample classified as clean sample
        elif is_poison == 0 and is_clean == 1:
            tn += 1
        # false positive, clean sample classified as poison sample
        elif is_poison == 0 and is_clean == 0:
            fp += 1
        # false negative, poison sample classified as clean sample
        else:
            fn += 1

    acc = (tp + tn) / (tp + tn + fp + fn)
    pre = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * pre * recall / (pre + recall) if (pre + recall) > 0 else 0
    print("tp, tn, fp, fn: ", tp, tn, fp, fn)
    print("acc, pre, recall, f1: ", acc, pre, recall, f1)
    results = {}
    results["tp"] = tp
    results["tn"] = tn
    results["fp"] = fp
    results["fn"] = fn
    results["acc"] = acc
    results["pre"] = pre
    results["recall"] = recall
    results["f1"] = f1
    return results

def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res