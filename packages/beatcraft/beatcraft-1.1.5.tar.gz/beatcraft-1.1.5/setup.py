from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(name="beatcraft",
      version="1.1.5",
      author="Arul and friends",
      author_email="arif.akbarul@amikom.ac.id",
      description="While you are focus on the game logic, "
                  "BeatCraft help you to make an authentic music for your game",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/omayib/BeatCraft/wiki",
      packages=find_packages(),
      install_requires=[
        'click',
        'MIDIUtil',
        'pyo',
        'pygame',
        'numpy==1.26.4',
        'sounddevice',
        'mido',
        'python-rtmidi',
        'pretty_midi',
        'torch==2.1.0',
        'torchaudio==2.1.0',
        'torchtext==0.16.0',
        'torchvision==0.16.0',
        'transformers==4.45.1',
        'xformers==0.0.22.post7',
        'audiocraft==1.3.0',
        'midi2audio',
        'librosa'
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      python_requires=">=3.6")