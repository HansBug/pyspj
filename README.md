# pyspj 

A light-weighted special support utils.

一个基于tmodule改进的超轻量版spj支持工具链。

## 安装

源代码安装

```shell
git clone git@gitlab.buaaoo.top:oo_system/judge/pyspj.git
cd pyspj
pip install .
```

卸载

```shell
pip uninstall pyspj
```

## 开始使用

### 命令行使用

pyspj可以通过命令行进行spj判定，命令行帮助信息如下

```
Usage: pyspj [OPTIONS]

Options:
  -v, --version                   Show package's version information.
  -i, --input TEXT                Input content of special judge.
  -o, --output TEXT               Output content of special judge
  -I, --input_file FILE           Input file of special judge (if -i is given,
                                  this will be ignored).

  -O, --output_file FILE          Output file of special judge (if -o is
                                  given, this will be ignored).

  -t, --type [free|simple|continuity]
                                  Type of the final result.  [default: free]
  -s, --spj TEXT                  Special judge script to be used.  [required]
  -p, --pretty                    Use pretty mode to print json result.
  -h, --help                      Show this message and exit.
```

一个简单的使用示例，设有如下的spj脚本`test_spj.py`

```python
import io


def spj_func(stdin: io.StringIO, stdout: io.StringIO):
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


__spj__ = spj_func

```

我们可以执行如下命令行进行判定

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj:spj_func
```

意为从`test_spj`包中导入`spj_func`进行使用，输出结果为

```
{"correctness": true, "detail": "Oh yeah, well done ^_^.", "message": "Correct result."}
```

此外，由于该脚本中定义了`__spj__`变量，故可以采用简单的命令行

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj
```

效果与上面等价。

然而在实际情况中，可能会存在文件较大且多行等不适合直接在命令行中表述的情况，故我们支持从文件载入输入输出。

例如设有文件`test_input.txt`

```
1 2 3 4 5
```

以及文件`test_output.txt`

```
15
```

故可以执行命令

```shell
pyspj -I test_input.txt -O test_output.txt -s test_spj
```

输出结果为

```
{"correctness": true, "detail": "Oh yeah, well done ^_^.", "message": "Correct result."}
```

而且实际上，文件和命令方式可以混用，例如可以使用`-I`指定文件输入，并用`-o`指定命令输出，一样可以进行正常的检查。

在命令行使用中，如果想要更加清晰的多行排版的话，可以使用`-p`选项，例如

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj -p
```

输出结果为

```json
{
    "correctness": true,
    "detail": "Oh yeah, well done ^_^.",
    "message": "Correct result."
}
```

不仅如此，考虑到一些复杂的动态情况，pyspj可以支持动态载入数值。

例如将脚本改为

```python
import io


def spj_func(stdin: io.StringIO, stdout: io.StringIO, fxxk=None):
    inputs = [int(item.strip()) for item in stdin.read().strip().split(' ') if item]
    _correct_sum = sum(inputs)

    if not fxxk:
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
    else:
        return False, 'Result error because {value} detected in fxxk.'.format(value=repr(fxxk))


__spj__ = spj_func

```

添加了一个`fxxk`参数，则可以调用命令行

```shell
pyspj -i '1 2 3 4 5' -o '15' -s test_spj -p -V fxxk=2
```

输出为

```
{
    "correctness": false,
    "detail": "Result error because '2' detected in fxxk.",
    "message": "Result error because '2' detected in fxxk."
}
```

注意：

* **附加参数建议保有默认值**，不然将在命令行中未配置时出现调用错误
* 附加参数载入后**默认均为字符串格式**，如果需要转换请在脚本内手动转换

### 脚本使用

pyspj还支持直接在脚本中进行原生调用，例如程序如下

```python
from pyspj import execute_spj_from_string

if __name__ == '__main__':
    result = execute_spj_from_string('test_spj', '1 2 3 4 5', '15')
    print(result.to_json())

```

输出结果为

```
{'correctness': True, 'message': 'Correct result.', 'detail': 'Oh yeah, well done ^_^.'}
```

也一样支持文件导入，程序如下

```python
from pyspj import execute_spj_from_file

if __name__ == '__main__':
    result = execute_spj_from_file('test_spj', 'test_input.txt', 'test_output.txt')
    print(result.to_json())

```

输出同上。

值得注意的是，脚本使用中，**上述两个函数均不支持文件和字符串的混用**。如果需要支持混用的话，请使用`execute_spj`函数进行DIY。举例如下

```python
import codecs
import io

from pyspj import execute_spj

if __name__ == '__main__':
    with codecs.open('test_input.txt') as stdin, \
            io.StringIO('15') as stdout:
        result = execute_spj('test_spj', stdin, stdout)
    print(result.to_json())

```

输出结果同上，等价于混用命令。

此外该部分也支持附加参数，例如对于上述脚本（指带有附加参数的），执行如下

```python
import codecs
import io

from pyspj import execute_spj

if __name__ == '__main__':
    with codecs.open('test_input.txt') as stdin, \
            io.StringIO('15') as stdout:
        result = execute_spj('test_spj', stdin, stdout, arguments={'fxxk': 2})
    print(result.to_json())

```

输出结果为

```
{'correctness': False, 'message': 'Result error because 2 detected in fxxk.', 'detail': 'Result error because 2 detected in fxxk.'}
```

