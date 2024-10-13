from setuptools import setup, find_packages

setup(
    name='ASL_Alpnum_Recognizer',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,  # This will include any files listed in MANIFEST.in
    install_requires=[
        'tensorflow',  # Add other dependencies as needed
        'numpy',
        'opencv-python',
        'cvzone',
        'mediapipe',
        'h5py',
    ],
    entry_points={
        'console_scripts': [
            'run_webcam=SignLangASL_Recognizer.recognize:SignLanguageRecognizer.run_webcam',
        ],
    },
    description='A package for recognizing American Sign Language using hand detection.',
    author='Mahedra Kumar Reddy Kakarla',
    author_email='mahendrakumarreddykakarla@gmail.com',
    url='https://github.com/BBB2912/ASL_Alpnum_Recognizer.git',  # Your project repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
