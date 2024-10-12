from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='aritmatika',
  version='0.0.7',
  description='Aritmatika adalah Paket Python untuk menyelesaikan masalah aritmatika sosial seperti untung rugi, bunga, pajak, diskon, rabat, serta bruto, netto, dan tara.',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='kelompok 6',
  author_email='mahesaputrilukman28@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Aritmatika Sosial', 
  packages=find_packages(),
  install_requires=['']
)
