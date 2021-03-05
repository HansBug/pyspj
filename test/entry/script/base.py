def _spj_func(stdin, stdout, fxxk=None):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    if not fxxk:
        outputs = stdout.read().strip().split(' ', maxsplit=2)
        if len(outputs) >= 1:
            _result = int(outputs[0])
        else:
            return False, 'No output found.'

        if _result == _correct_sum:
            return True, 'Correct result.'
        else:
            return False, 'Result {correct} expected but {actual} found.'.format(
                correct=repr(_correct_sum), actual=repr(_result)
            )
    else:
        return False, 'Result error because {value} detected in fxxk.'.format(value=repr(fxxk))


__spj__ = _spj_func

_another_value = 233
