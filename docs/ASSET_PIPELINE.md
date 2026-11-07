# Kinetics animation asset pipeline

## One visual asset

Kinetics intentionally maintains one visual asset in the repository:

`Assets/Future/kinetics-science-quest.gif`

It is an original, colourful, continuously looping science animation generated from Python drawing primitives. No static logo, scientific-photo gallery, PNG collection, decorative SVG, placeholder image or external image download is part of this pipeline.

## Regenerate

On Termux or desktop Python:

~~~bash
python -m pip install Pillow
python scripts/build_pixel_animation.py
python scripts/validate_visual_assets.py
~~~

The builder creates a 48-frame, 480 × 270 GIF with an infinite loop. It combines an original pixel-art science rover, animated molecular orbits, a DNA helix, a glowing research portal, parallax stars and a moving progress track.

## Automated build

The GitHub Actions workflow `.github/workflows/science-gallery.yml` is retained as the animation build workflow. It regenerates the GIF, validates the single-asset policy, and commits only the README and animation when they change. It does not download scientific images.

## Validation

~~~bash
python scripts/validate_visual_assets.py
~~~

Validation checks GIF decoding, dimensions, frame count, infinite-loop metadata, the README embed, and ensures that no other image-format files are present in the repository.
