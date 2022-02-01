def continuity_spj_func(stdin, stdout):
    _expected_sum = int(stdin.read().strip())

    output_items = [int(item.strip()) for item in stdout.read().strip().split(' ') if item]
    _actual_sum = sum(output_items)
    _actual_cnt = len(output_items)

    if _expected_sum == _actual_sum:
        return (True, 1 - (_actual_cnt - 1) / _expected_sum), 'Correct result.', 'Oh yeah, well done ^_^.'
    else:
        return (False, 0), f'Result {_expected_sum} expected but {_actual_sum} found.'


__spj__ = continuity_spj_func
