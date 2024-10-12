from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-audiorec-ru-fork",
    version="0.1.6",
    author="Stefan Rummer",
    author_email="djgleban1147@gmail.com",
    description="Record audio from the user's microphone in apps that are deployed to the web. (via Browser Media-API) [GitHub ☆ 160+: steamlit-audio-recorder]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BondarchukGleb42/streamlit-audio-recorder",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=0.63",
    ],
)
