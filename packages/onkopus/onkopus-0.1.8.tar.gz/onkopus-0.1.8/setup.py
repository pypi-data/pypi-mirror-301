import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setuptools.setup(
    name="onkopus",
    version="0.1.8",
    author="Nadine S. Kurz",
    author_email="nadine.kurz@bioinf.med.uni-goettingen.de",
    description="Biomarker interpretation framework to analyze and interpret genetic alterations in cancer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['./onkopus/onkopus'],
    url="https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus",
    packages=setuptools.find_packages(),
    install_requires=['pyliftover','matplotlib','numpy','pandas','plotly','requests','scikit-learn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.6',
    license="GPLv3"
)