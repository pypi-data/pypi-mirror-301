# cli.py
import click
from crt.option import crt_files, crt_temp


@click.command()
@click.option('-t',
              '--temp',
              required=False,
              type=str,
              help='main:config:setup',)
@click.argument('oth', required=False,)
@click.argument('ext', required=False,)
def main(temp, oth, ext):
    """
files: \tTo create files use 'crt' and list the names in quotes to list use the ':' sign to create folders use brackets after the name '<','>' in brackets you can specify files, after all names indicate file extensions if not specified in the names.
Example: crt "file_name1:file_name2:dir_name1<>:dir_name2<file_name>" py\n
temp: \tTo create a project use '-t' or '--temp' and specify the name of the template, by default there are the following templates: 'web-front', 'web-back', 'app', 'project', 'config'.
Example: crt -t app"""
    if temp:
        crt_temp(temp)
    else:
        crt_files(ext, oth)


if __name__ == '__main__':
    main()
