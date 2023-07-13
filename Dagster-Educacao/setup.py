from setuptools import find_packages, setup

setup(
    name="education_model",
    packages=find_packages(exclude=[""]),
    install_requires=[
        "dagster",
        "dagstermill",
        "papermill-origami>=0.0.8",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
