# Kinetics visual asset pipeline

## Why the previous gallery failed

The earlier README embedded 30 paths under Assets/Future/PNG/, but the PNG files had not been downloaded and committed. Markdown image tags pointing to absent files render as broken images. The updated README therefore does not embed PNG paths before those files exist.

## 100-domain PNG gallery

Install the optional dependency and run:

~~~bash
python -m pip install -e ".[gallery]"
python scripts/import_science_gallery.py
~~~

The importer queries Wikimedia Commons for the 100 catalogue domains, rejects non-images, SVGs, small images and restrictive licenses, accepts only CC0/public domain/CC BY/CC BY-SA, converts accepted images to local PNGs, and records creator, source page, license, license URL and dimensions in Assets/Future/ATTRIBUTION.json. Missing categories can be retried.

Examples:

~~~bash
python scripts/import_science_gallery.py --start 1 --end 20
python scripts/import_science_gallery.py --start 81 --end 100
python scripts/import_science_gallery.py --overwrite
~~~

Review original file pages and license terms before redistribution. Wikimedia metadata can be incomplete; verify provenance. Never use an image if its license is unclear.

## Pixel animation

Regenerate the local banner with:

~~~bash
python -m pip install -e ".[gallery]"
python scripts/build_pixel_animation.py
~~~

The currently tracked legacy GIF fails structural validation and is intentionally not embedded by the README. The generator writes Assets/Future/kinetics-science-quest.gif as a 32-frame, 640 × 240 GIF89a file and verifies its dimensions, frame count and infinite-loop metadata. Run the generator, validate the output, then commit the replacement binary. Keep the path case-sensitive.

## Validation before commit

~~~bash
python scripts/validate_visual_assets.py
~~~

Validation checks PNG integrity, GIF frame count, dimensions and attribution coverage. Do not publish the gallery as complete unless all 100 PNGs and attribution records are present.
