import os
import re
import shutil
from sys import argv

from setuptools import setup, find_packages, Command

from compiler.api import compiler as api_compiler
from compiler.errors import compiler as errors_compiler


# Read requirements
with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

# Read version
with open("hasnain/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

# Read long description
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

# Custom Clean Command
class Clean(Command):
    DIST = ["./build", "./dist", "./hasnain.egg-info"]
    API = [
        "hasnain/errors/exceptions", "hasnain/raw/functions", "hasnain/raw/types", "hasnain/raw/base",
        "hasnain/raw/all.py"
    ]

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("all", None, "Clean all generated files"),
    ]

    def initialize_options(self):
        self.dist = None
        self.api = None
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clean.DIST)

        if self.api:
            paths.update(Clean.API)

        if self.all or not paths:
            paths.update(Clean.DIST + Clean.API)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print(f"Skipping {path}")
            else:
                print(f"Removing {path}")


# Generate Command if needed (optional)
class Generate(Command):
    description = "Generate necessary files"

    user_options = [
        ("api", None, "Generate API files"),
    ]

    def initialize_options(self):
        self.api = None

    def finalize_options(self):
        pass

    def run(self):
        if self.api:
            errors_compiler.start()
            api_compiler.start()


# Start API and errors compiler if building
if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    api_compiler.start()
    errors_compiler.start()

# Setup configuration
setup(
    name="hasnain",
    version=version,
    description="Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hasnainkk-07/hasnain",
    download_url="https://github.com/hasnainkk-07/hasnain/releases/latest",
    author="Hasnain Khan",
    author_email="hasnainkk98075@gmail.com",
    license="LGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords="telegram chat messenger mtproto api client library python",
    project_urls={
        "Tracker": "https://github.com/hasnainkk-07/hasnain/issues",
        "Source": "https://github.com/hasnainkk-07/hasnain",
    },
    python_requires="~=3.7",
    packages=find_packages(exclude=["compiler*", "tests*", "hasnain/raw*"]),
    zip_safe=False,
    install_requires=requires,
    cmdclass={
        "clean": Clean,
        "generate": Generate,
    }
)
