from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'ninept',         
  packages = find_packages(),
  version = '0.1',      
  license='apache-2.0',        
  description = 'Python module providing access to a shared large language modell',   
  author = 'Simon Klüttermann',                   
  author_email = 'Simon.Kluettermann@cs.tu-dortmund.de',      
  url = 'https://github.com/psorus/ninept',   
  download_url = 'https://github.com/psorus/ninept/archive/v_01.tar.gz',    
  keywords = ['llm'],   
  install_requires=[            
      "requests",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)

          #'tensorflow==2.11.*',
          #'numpy',
          #'scikit-learn',
          #'tqdm',
