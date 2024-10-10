import httpx
import os
import tarfile
import asyncio
import shutil
import tempfile


def create_directory(app_dir):
    if not os.path.exists(app_dir):
        print('directory doesnt exist')
        os.makedirs(app_dir)
    else:
        print('directory exist')

async def download_repo(template):
    r = httpx.get('https://codeload.github.com/hloughrey/latitude55-templates/tar.gz/master', timeout=20)
    with open(template, 'wb') as f:
        f.write(r.content)


async def extract_specific_files(repo,template, temp_dir):
    with tarfile.open(repo, 'r') as tar:
        subdir_and_files = [
            tarinfo for tarinfo in tar.getmembers()
            if tarinfo.name.startswith(f"latitude55-templates-master/templates/{template}")
        ]
        tar.extractall(path=temp_dir, members=subdir_and_files)

def move_and_rename_app(temp_dir, template, app_dir):
    source = os.path.join(temp_dir,'latitude55-templates-master', 'templates', template)
    destination = app_dir
    for file_name in os.listdir(source):
        shutil.move(os.path.join(source, file_name), destination)

async def download_and_extract(template, app_name):
    app_dir = os.path.join(os.getcwd(), app_name) 
    temp_dir = tempfile.TemporaryDirectory()

    create_directory(app_dir)
    repo = os.path.join(temp_dir.name, 'latitude55-templates.tar.gz')

    await download_repo(repo)
    await extract_specific_files(repo, template, temp_dir.name)
    move_and_rename_app(temp_dir.name, template, app_dir)


def main():
    asyncio.run(download_and_extract('node', 'express-app'))

if __name__ == "__main__":
    main()