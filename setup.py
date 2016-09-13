import setuptools

setuptools.setup(
    data_files=[
        (
            'stitching_data',
            [
                "data/example.cif"
            ]
        )
    ],
    entry_points={
        "console_scripts": [
            "stitching=stitching.__main__:__main__",
        ]
    },
    install_requires=[
        "bioformats",
        "click",
        "javabridge",
        "numpy",
        "scikit-image"
    ],
    dependency_links=[
        "https://github.com/CellProfiler/python-bioformats/master"
    ],
    license="BSD",
    name="stitching",
    packages=setuptools.find_packages(
        exclude=[
            "docs",
            "tests"
        ]
    ),
    url="https://github.com/CellProfiler/stitching",
    version="1.0.0"
)
