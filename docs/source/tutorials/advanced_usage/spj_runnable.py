from pyspj.entry import pyspj_entry


def spj_func(stdin, stdout):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    outputs = stdout.read().strip().split(' ', maxsplit=2)
    if len(outputs) >= 1:
        _result = int(outputs[0])
    else:
        return False, 'No output found.'

    if _result == _correct_sum:
        return True, 'Correct result.', 'Oh yeah, well done ^_^.'
    else:
        return False, 'Result {correct} expected but {actual} found.'.format(
            correct=repr(_correct_sum), actual=repr(_result)
        )


if __name__ == '__main__':
    pyspj_entry(
        'demo_pyspj', spj_func,
        version='2.3.3',  # optional
        author='spj-dev',  # optional
        email='spj-demo@my-email.com',  # optional
    )()
