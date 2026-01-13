import os, shutil
from block_transformations import markdown_to_html_node
from pathlib import Path

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, base_path)



def generate_page(from_path, template_path, to_path, base_path):
    from_path = os.path.join(os.getcwd(), from_path)
    template_path = os.path.join(os.getcwd(), template_path)
    to_path = os.path.join(os.getcwd(), to_path)
    to_path_dir = os.path.dirname(to_path) 

    if to_path_dir and not os.path.exists(to_path_dir):
        os.makedirs(to_path_dir)

    try:

        with open(from_path, 'r') as raw_md:
            md_content = raw_md.read()
        with open(template_path, 'r') as tmp:
            template_content = tmp.read()

        node = markdown_to_html_node(md_content)
        content = node.to_html()
        title = extract_title(md_content)
        
        html = template_content.replace("{{ Title }}", title)
        html = html.replace("{{ Content }}", content)
        html = template_content.replace('href="/', f'href="{base_path}')
        html = template_content.replace('src="/', f'src="{base_path}')
        
        with open(to_path, 'w') as file:
            file.write(html)

    except Exception as e:
        print('ERROR: GENERATE PAGE IN MAIN.PY')
        print(e)


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        line = line.lstrip()
        if line.startswith('# '):
            return line.lstrip('#').strip()
    raise Exception('HEADER NOT FOUND')



def copy_files(from_path, to_path, root='/'):
    print(f"--- MOVING FILES FROM {from_path} TO {to_path} ---")
    to_path = os.path.join(root, to_path)
    from_path = os.path.join(root, from_path)

    if not os.path.exists(from_path):
        raise Exception(f"mv_files: {from_path} doesn't exists")
    

    if os.path.exists(to_path):
        shutil.rmtree(to_path) 

    os.mkdir(to_path)    
    copy_files_recursive(from_path, to_path)


def copy_files_recursive(from_path, to_path):

    files = os.listdir(from_path)

    for file in files:
        file_path = os.path.join(from_path, file)

        if os.path.isfile(file_path):
            print(f"copying {file}: {file_path} -> {to_path}")
            shutil.copy(file_path, to_path)
        else:
            subfolder = os.path.join(to_path, file)
            print(f"\n ---subfolder {file}--- \n")
            if not os.path.exists(subfolder):
                os.mkdir(subfolder)
            copy_files_recursive(file_path, subfolder)

    print(f"done with {files}")
