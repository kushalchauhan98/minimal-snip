# minimal-snip
A minimal snipping tool for linux.

[![Snap Status](https://build.snapcraft.io/badge/kushalchauhan98/minimal-snip.svg)](https://build.snapcraft.io/user/kushalchauhan98/minimal-snip)

To install this snap, clone this repository and simply run:

```
snapcraft prime
sudo snap try ./prime --devmode
```

Currently, development is paused due a snapcraft bug : https://stackoverflow.com/questions/45499865/trouble-allocating-fonts-in-a-tcl-tk-based-ubuntu-snap-app

But reported on snapcraft launchpad : https://bugs.launchpad.net/snapcraft/+bug/1709060

If you want to just try how the app works, run:

```
pip install -r requirements.txt
python minimal_snip.py
```

Screenshots:

![Main Window](https://github.com/kushalchauhan98/minimal-snip/blob/master/res/1.png)

![Demo](https://github.com/kushalchauhan98/minimal-snip/blob/master/res/2.png)
