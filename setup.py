from setuptools import setup , find_packages

setup(
    name='motor_stage_ui',
    version='0.1',
    license='License AGPL-3.0 license',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pint'
    ],
    entry_points={
        'console_scripts': [
            'motor = motor_stage_ui.motor_stage_terminal:motor',
        ],
    },
)