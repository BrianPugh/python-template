import re
import readline
import subprocess
from pathlib import Path


class BadResponse(Exception):
    """User gave a bad response."""


def camel_to_snake(s):
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def validate_input(prompt, validate=None):
    """Prompts user until response passes ``validate``."""
    while True:
        response = input(prompt + ": ")

        if validate is None:
            break

        try:
            validate(response)
            break
        except BadResponse as e:
            print(f'"{response}" {e}')
    return response


def git(*args):
    return subprocess.check_output(["git"] + list(args))


def main():
    def is_identifier(response):
        if not response.isidentifier():
            raise BadResponse("is not a valid python identifier.")

    def is_lower(response):
        if response.lower() != response:
            raise BadResponse("should be all lower case.")

    def good_module_name(response):
        is_identifier(response)
        is_lower(response)
        if "_" in response:
            raise BadResponse("should not contain an underscore _")
        if len(response) > 20:
            raise BadResponse("is too long (max 20 char limit).")

    developer_name = validate_input("Enter your name")

    module_name = validate_input("Python Module Name (default: app)", good_module_name)

    def good_class_name(response):
        is_identifier(response)
        if not response[0].isupper():
            raise BadResponse("first letter should be capitalized.")

    dataset_class_name = validate_input(
        "Dataset class name (default: MyDataset)", good_class_name
    )

    model_class_name = validate_input(
        "Model class name (default: MyModel)", good_class_name
    )

    replacements = {
        "YOUR_NAME_HERE": developer_name,
        "app": module_name,
        "MyDataset": dataset_class_name,
        "mydataset": dataset_class_name.lower(),
        "MyModel": model_class_name,
        "mymodel": model_class_name.lower(),
    }

    def replace(string):
        """Replace whole words only."""

        def _replace(match):
            return replacements[match.group(0)]

        # notice that the 'this' in 'thistle' is not matched
        return re.sub(
            "|".join(r"\b%s\b" % re.escape(s) for s in replacements), _replace, string
        )

    repo = Path(__file__).parent
    bootstrap_file = repo / "bootstrap.py"
    py_files = list(repo.rglob("*.py"))
    py_files.remove(bootstrap_file)
    for py_file in py_files:
        contents = py_file.read_text()
        contents = replace(contents)
        py_file.write_text(contents)
        if py_file.stem in replacements:
            dst = py_file.with_name(replacements[py_file.stem] + ".py")
            py_file.replace(dst)

    # Move the app folder
    (repo / "app").replace(repo / replacements["app"])

    # Move README_TEMPLATE.md
    (repo / "README_TEMPLATE.md").replace(repo / "README.md")

    # Delete this script
    bootstrap_file.unlink()

    subprocess.check_output(["pre-commit", "install"])
    git("add", "*")
    git("commit", "-m", "rename from template")

    print()
    print("Renaming complete. Changes commited. Please run:")
    print("    git push")
    print()


if __name__ == "__main__":
    main()
