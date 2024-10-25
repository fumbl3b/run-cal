# setup.py

from setuptools import setup, find_packages

setup(
    name="workout_calendar",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'generate-calendar=calendar_tool.calendar_gen:main',
        ],
    },
    install_requires=[
        'pandas',
        'icalendar',
    ],
    description="Generate monthly workout calendars and export them to Google Calendar.",
    author="Harry Winkler",
    author_email="harry@fumblebee.site",
    url="https://github.com/fumbl3b/run-cal",  # Replace with your actual repo URL
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
