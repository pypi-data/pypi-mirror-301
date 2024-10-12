# cli.py
import click
from crt.option import crt_files, crt_temp, fill_code_is_exist, fill_temp, temp_is_exist


@click.command()
@click.option('-t',
              '--temp',
              required=False,
              type=str,
              help='main:config:setup',)
@click.argument('oth', required=False,)
@click.argument('ext', required=False,)
@click.argument('f', required=False,)
def main(temp, oth, ext, f):
    """
files: \tTo create files use 'crt' and list the names in quotes to list use the ':' sign to create folders use brackets after the name '<','>' in brackets you can specify files, after all names indicate file extensions if not specified in the names.
Example: crt "file_name1:file_name2:dir_name1<>:dir_name2<file_name>" py\n
temp: \tTo create a project use '-t' or '--temp' and specify the name of the template, by default there are the following templates: 'web-front', 'web-back', 'app', 'project', 'config'.
Example: crt -t app"""
    if temp:
        json_temp = temp_is_exist(temp)
        if json_temp:
            crt_temp(json_temp)
            if oth:
                print(123123)
                d_fill = fill_code_is_exist(temp)
                if d_fill:
                    fill_temp(d_fill)
                else:
                    print("No File Filling Template")
        else:
            print(
                f"no such template name '{temp}'\nby default there are the following templates: 'web-front', 'web-back', 'app', 'project', 'config'")

    else:
        if not oth:
            print('Use "--help"')
        else:
            crt_files(ext, oth)


if __name__ == '__main__':
    main()
