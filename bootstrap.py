# Only use builtin libraries for this script
import re
import readline
import subprocess
from datetime import date
from pathlib import Path


class BadResponse(Exception):
    """User gave a bad response."""


def check_and_install_poetry():
    try:
        subprocess.check_output(["which", "poetry"])
        return
    except subprocess.CalledProcessError:
        pass

    subprocess.check_output(
        "curl -sSL https://install.python-poetry.org | python3 - --preview",
        shell=True,
    )


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


def good_class_name(response):
    is_identifier(response)
    if not response[0].isupper():
        raise BadResponse("first letter should be capitalized.")


def main():
    check_and_install_poetry()

    replacements: dict[str, str] = {
        "CURRENT_YEAR_HERE": str(date.today().year),
    }
    replacements["YOUR_NAME_HERE"] = validate_input("Enter your name")
    replacements["pythontemplate"] = validate_input(
        "Python Module Name", good_module_name
    )

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
    (repo / "pythontemplate").replace(repo / replacements["pythontemplate"])

    # Move README_TEMPLATE.rst
    (repo / "README_TEMPLATE.rst").replace(repo / "README.rst")

    subprocess.check_output(["poetry", "install"])
    subprocess.check_output(["poetry", "run", "python", "-m", "pre_commit", "install"])
    git("add", "*")
    git("commit", "-m", "bootstrap from template")

    print()
    print("Bootstrapping complete. Changes commited. Please run:")
    print("    git push")
    print()

    # Delete this script
    bootstrap_file.unlink()


if __name__ == "__main__":
    main()
