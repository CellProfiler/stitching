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
