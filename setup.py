from setuptools import setup

setup(name='minimal-snip',
      version='1.0',
      description='A Minimal Snipping Tool for Linux',
      author='Kushal Chauhan',
      author_email='kushalchauhan98@gmail.com',
      url='https://github.com/kushalchauhan98/minimal-snip/',
      py_modules=['minimal_snip'],
      data_files=[('icons', ['icons/close-hover.ppm',
                             'icons/close.ppm',
                             'icons/hide-hover.ppm',
                             'icons/hide.ppm',
                             'icons/save-hover.ppm',
                             'icons/save.ppm',
                             'icons/show-hover.ppm',
                             'icons/show.ppm'])],
      scripts=['scripts/minimal-snip'],
      install_requires=['pyscreenshot', 'Pillow']
     )
