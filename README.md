# Signal Viewer
This is a desktop GUI for viewing *edf* signal files and *wav* audio files and providing basic controls for playing, pausing, scrolling, zooming and saving pdf reports for the uploaded signals alongside spectrograms.

There is a built-in equalizer for audio files along with saving the equalized audio.

Multiple signals can be viewed simultaneously by uploading an edf file, then the GUI automatically syncs the plots.

# Setup

1. From the command line create a virtual environment and activate.
```
> python -m venv .venv
> .venv\Scripts\activate
```

2. Install dependencies.
```
> pip install -r requirements.txt
```

3. Run the app.
```
> python app.py
```

There are sample files in the repo *SampleECG.edf*  and *demo.wav* for trying out.
