# Not Needed but keep for future reference
def calc_bias(count_dict):
    bias_dict = {}
    norm_bias_dict = {}
    total_files = sum(count_dict.values())
    count = len(count_dict)

    for k, v in count_dict.items():
        bias_dict[k] = total_files / v

    total_bias = sum(bias_dict.values())

    for i, j in bias_dict.items():
        norm_bias_dict[i] = j / total_bias * count

    return norm_bias_dict
