import sys
from pathlib import Path
import os
from setuptools import find_packages, setup

# Get the project root directory
root_dir = Path(__file__).parent

# Add the package directory to the Python path
package_dir = root_dir / "study_friend"
sys.path.append(str(package_dir))

# CUDA-device check
CUDA_DEVICE = os.environ.get('CUDA_PATH') is not None

# Read the requirements from the requirements.txt file
requirements_path = root_dir / "requirements.txt"
with open(requirements_path) as fid:
    # exclude mlx-vlm only on CUDA-device
    requirements = [l.strip() for l in fid.readlines()  if not l.startswith("mlx-vlm")   or not CUDA_DEVICE]
    # exclude bitsandbytes on non-CUDA device
    requirements = [l.strip() for l in requirements  if not l.startswith("bitsandbytes") or CUDA_DEVICE]

# Setup configuration
setup(
    name="study_friend",
    version="1.0.0",
    description="AI tools to help you study better. No need of internet.",
    long_description=open(root_dir / "README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author_email="marcosangio03@gmail.com",
    author="Sangiorgi Marco",
    url="https://github.com/sangioai/study-friend",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(where=root_dir),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "study_friend.query = study_friend.query:main",
            "study_friend.convert = study_friend.convert:main"
        ]
    },
)
