from setuptools import setup, find_packages

setup(
    name="EdgeText",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'pillow',
        'pytesseract',
        'pyinstaller',
        # Tambahkan dependensi lainnya di sini
    ],
    entry_points={
        'console_scripts': [
            'run-edge-text = run:main',  # Gantilah `run:main` dengan fungsi utama kamu
        ],
    },
)
