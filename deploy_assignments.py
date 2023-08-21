import shutil
from pathlib import Path
import argparse
import subprocess


def is_project_folder(folder: Path):
    return folder.is_dir() and folder.name.startswith("project-")


def copy_files_and_merge(src: Path, dest: Path):
    for item in src.iterdir():
        if item.is_file():
            dest_file = dest / item.name
            shutil.copyfile(item, dest_file)
        elif item.is_dir():
            dest_dir = dest / item.name
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(item, dest_dir, dirs_exist_ok=True)


def process_solution_and_stubs(hw_folder: Path, target_folder: Path):
    solution_folder = hw_folder / "solution"
    stubs_folder = hw_folder / "assignment"

    if solution_folder.is_dir():
        copy_files_and_merge(solution_folder, target_folder)

    # copy the stubs second so they overwrite the solutions
    if stubs_folder.is_dir():
        copy_files_and_merge(stubs_folder, target_folder)


def copy_files(src: Path, dest: Path):
    dest.mkdir(exist_ok=True, parents=True)

    for folder in src.iterdir():
        if folder.name.startswith('.') or folder.name in ['updates']:
            continue

        if is_project_folder(folder):
            target_hw_folder = dest / folder.relative_to(src)
            target_hw_folder.mkdir(parents=True, exist_ok=True)
            
            process_solution_and_stubs(folder, target_hw_folder)

            # Copy other files
            for other_file in folder.glob('*.*'):
                shutil.copyfile(other_file, target_hw_folder / other_file.name)

        elif folder.is_dir():
            target_subfolder = dest / folder.relative_to(src)
            copy_files(folder, target_subfolder)

        elif folder.is_file():
            shutil.copyfile(folder, dest / folder.name)



def git_pull(dest: Path):
    subprocess.run('git pull --no-rebase', check=True, shell=True, cwd=dest)


def git_push(dest: Path, message: str):
    subprocess.run(f'git add .', check=True, shell=True, cwd=dest)
    subprocess.run(f'git commit -am "{message}"', check=True, shell=True, cwd=dest)
    subprocess.run('git push', check=True, shell=True, cwd=dest)


def main(src: Path, dest: Path, message: str):
    
    git_pull(dest)
    copy_files(src, dest)
    git_push(dest, message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reproduce folder structure and merge files.")
    parser.add_argument("commit_message", type=str, default='copy from source repo', nargs='?', help="Git commit message")
    parser.add_argument("--target-folder", type=Path, help="The target folder", 
                        default=Path(__file__).parent.parent / 'byu-cs312-content-public')
    parser.add_argument("--root-folder", type=Path, help="The root folder (defaults to current directory)",
                        default=Path(__file__).parent)
    args = parser.parse_args()

    root_folder = args.root_folder.resolve()
    target_folder = args.target_folder.resolve()

    main(root_folder, target_folder, args.commit_message)
