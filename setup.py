from setuptools import setup, find_packages

setup(
    name="motor_stage_ui",
    version="1.0",
    license="License AGPL-3.0 license",
    author="Rasmus Partzsch",
    packages=find_packages(),
    package_data={
        "": ["motor_stage_ui/configuration.yaml"],
    },
    include_package_data=True,
    install_requires=["Click", "pint", "coloredlogs", "PyQt5", "pyserial", "pyyaml"],
    entry_points={
        "console_scripts": [
            "motor = motor_stage_ui.motor_stage_terminal:motor",
            "motorgui = motor_stage_ui.motor_stage_gui:main",
        ],
    },
)
