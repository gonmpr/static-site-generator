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
    copy_files('static', 'public', current_dir)

    print('###################')
    print('Generating content...')
    print('###################')
    print()

    generate_pages_recursive('content', 'template.html', 'public')







if __name__ == '__main__':
    main()
