from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
	Extension(
		"projection.functions",
		["projection/functions.pyx"],
		extra_compile_args=['-fopenmp', '-O3', '-g0', '-Wno-unreachable-code'],
		extra_link_args=['-fopenmp'],
		include_dirs=[numpy.get_include()],
		define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
	)
]

setup(
	name="projectionSVD",
	version="0.1",
	description="Projection into SVD space",
	author="Jonas Meisner",
	packages=["projection"],
	entry_points={
		"console_scripts": ["projectionSVD=projection.main:main"]
	},
	python_requires=">=3.7",
	install_requires=[
		"cython",
		"numpy"
	],
	ext_modules=cythonize(extensions),
	include_dirs=[numpy.get_include()]
)
