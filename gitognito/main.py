import os
import shutil
import argparse
from tempfile import TemporaryDirectory

from git import Repo, Actor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="URL to the original Git repository")
    parser.add_argument("target", help="URL to the target Git repository")
    parser.add_argument("target_branch", help="Branch to push in the target repository")
    parser.add_argument("-f", "--force", action="store_true", default=False, help="Force push to the target repository")
    parser.add_argument("-a", "--author", default="Anonymous Author(s)", help="Author name to use in the final commit")
    parser.add_argument("-e", "--email", default="anon@nowhere.com", help="Email to use in the final commit")
    parser.add_argument("-m", "--message", default="Init", help="Message to use in the final commit")
    args = parser.parse_args()

    with TemporaryDirectory() as tmp_dir:
        print("cloning original repo...")
        repo = Repo.clone_from(args.source, os.path.join(tmp_dir, "original"))

        print("flattening submodules...")
        # Recursively initialize all submodules first
        for submodule in repo.submodules:
            print(submodule.path)
            submodule.update(init=True, recursive=True)

        # Remove any .git and .gitmodules
        for root, dirs, files in os.walk(repo.working_tree_dir, topdown=True):
            if ".git" in dirs:
                shutil.rmtree(os.path.join(root, ".git"))
                dirs.remove(".git")

            if ".gitmodules" in files:
                os.remove(os.path.join(root, ".gitmodules"))

        # Re-init the repo with a anonymous author
        print("anonymizing history...")
        repo = Repo.init(repo.working_tree_dir)
        repo.git.add(all=True)
        anon = Actor(args.author, args.email)
        repo.index.commit("Init", author=anon, committer=anon)

        # Push to the target repo
        print("pushing to the target repo...")
        origin = repo.create_remote("origin", args.target)
        repo.active_branch.rename(args.target_branch)
        origin.push(refspec=f"{args.target_branch}:{args.target_branch}", force=args.force)


if __name__ == "__main__":
    main()
