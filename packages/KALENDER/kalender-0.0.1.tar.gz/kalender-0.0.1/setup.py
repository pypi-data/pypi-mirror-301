from setuptools import setup, find_packages

setup(
    name='KALENDER', # name of packe which will be package dir below project
    version='0.0.1',
    url='https://github.com/zlfaaasyyy/KALENDER.git',
    author='KELOMPOK 3 ALGO A',
    author_email='syauqiyahzalfa2006@gmail.com',
    description='Kalender adalah salah satu package Python yang menyediakan berbagai fungsi terkait penanggalan. Package ini membantu kita untuk bekerja dengan kalender, menentukan hari libur, dan sebagainya. Beberapa fitur utamanya adalah menampilkan bulan atau tahun dalam bentuk kalender, menentukan hari dalam minggu untuk tanggal tertentu, dan menghitung hari kerja.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)