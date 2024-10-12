from setuptools import setup, find_packages

setup(
    name='inc-counter',
    version='0.7',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'inc-counter': ['templates/*.html',
                        'static/**/*', ],  # Include all HTML files in the templates directory
    },
    install_requires=[
        'flask',
        'flask_cors',
        # Add other dependencies here (e.g., React-related packages if needed)
    ],
    entry_points={
        'console_scripts': [
            'start-counter=inc_counter.app:main',  # This command will run the main() function in inc_counter/app.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: OS Independent',
    ],
)
