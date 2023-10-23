import os
from pathlib import Path

def get_files_from_folders_with_ending(folders, ending):
    paths = []
    for folder in folders:
        paths.extend(sorted(
            [
                Path(folder) / fname
                for fname in os.listdir(folder)
                if fname.endswith(ending)
            ]
        ))
    return paths

root_dir = Path(__file__).resolve().parent
os.chdir(root_dir)
py_files = get_files_from_folders_with_ending([root_dir], '.py')
for p in [p for p in py_files if p.stem != 'build']:
    cmd = f'bash ../tikzmake.sh {p.stem}'
    print(cmd)
    os.system(cmd)