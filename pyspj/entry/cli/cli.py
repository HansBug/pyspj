import json

import click
from click.core import Context, Option

from .exception import _raise_exception_with_exit_code
from .values import _load_from_values
from ..script import execute_spj
from ..script.decorator import stdin_string_support, stdin_file_trans, stdout_string_support, stdout_file_trans
from ...config.meta import __TITLE__, __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__
from ...models.general import ResultType


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool) -> None:
    """
    Print version information of cli
    :param ctx: click context
    :param param: current parameter's metadata
    :param value: value of current parameter
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    click.echo('Developed by {author}, {email}.'.format(author=__AUTHOR__, email=__AUTHOR_EMAIL__))
    ctx.exit()


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('-i', '--input', 'input_content', type=str, help='Input content of special judge.')
@click.option('-o', '--output', 'output_content', type=str, help='Output content of special judge')
@click.option('-I', '--input_file', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Input file of special judge (if -i is given, this will be ignored).')
@click.option('-O', '--output_file', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Output file of special judge (if -o is given, this will be ignored).')
@click.option('-V', '--value', type=str, multiple=True,
              help='Attached values for special judge (do not named as "stdin" ot "stdout".')
@click.option('-t', '--type', 'result_type',
              type=click.Choice([item.lower() for item in ResultType.__members__.keys()]),
              help='Type of the final result.', default=ResultType.FREE.name.lower(), show_default=True)
@click.option('-s', '--spj', type=str, required=True,
              help='Special judge script to be used.')
@click.option('-p', '--pretty', type=bool, is_flag=True,
              help='Use pretty mode to print json result.')
def cli(input_content, output_content,
        input_file, output_file, value, result_type,
        spj, pretty):
    if not input_content and not input_file:
        _raise_exception_with_exit_code(1, 'Either -i or -I should be given.')
    if not output_content and not output_file:
        _raise_exception_with_exit_code(1, 'Either -o or -O should be given.')

    _execute_func = execute_spj
    if input_content:
        _execute_func = stdin_string_support(_execute_func)
        _input = input_content
    else:
        _execute_func = stdin_file_trans(_execute_func)
        _input = input_file

    if output_content:
        _execute_func = stdout_string_support(_execute_func)
        _output = output_content
    else:
        _execute_func = stdout_file_trans(_execute_func)
        _output = output_file

    result_type = ResultType.loads(result_type)
    result = _execute_func(
        spj=spj, type_=result_type,
        stdin=_input, stdout=_output,
        arguments=_load_from_values(list(value)),
    )

    print(json.dumps(result.to_json(), indent=4 if pretty else None, sort_keys=True))
