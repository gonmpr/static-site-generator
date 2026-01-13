import sys, os
from gencontent import copy_files, generate_pages_recursive 

def main():
    if len(sys.argv) > 2:
        raise Exception('Usage: ./main.py [root_path]: default "/"')

    print('###################')
    print('Moving files...')
    print('###################')
    print()

    base_path = sys.argv[1]
    current_dir = os.getcwd()

    template = 'template.html'
    copy_from = 'static'
    make_from = 'content'

    build_to = 'docs'

    copy_files(copy_from, build_to, current_dir)

    print('###################')
    print('Generating content...')
    print('###################')
    print()

    generate_pages_recursive(make_from, template, build_to, base_path)







if __name__ == '__main__':
    main()
