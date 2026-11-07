# Kinetics visual asset pipeline

## Why the previous gallery failed

The earlier README embedded 30 paths under Assets/Future/PNG/, but the PNG files had not been downloaded and committed. Markdown image tags pointing to absent files render as broken images. The updated README therefore does not embed PNG paths before those files exist.

## 100-domain PNG gallery

The Termux downloader runs the repository's Python importer and publishes the finished assets:

~~~bash
pkg install -y git python python-pillow
bash scripts/termux_download_gallery.sh
~~~

The importer queries Openverse's openly licensed multi-provider image index first and falls back to Wikimedia Commons. Openverse results are restricted to public-domain, CC0, CC BY and CC BY-SA licenses suitable for commercial reuse; non-commercial and no-derivatives licenses are excluded. It rejects SVGs, non-images and source files whose shortest side is below 1024 pixels. Accepted originals are centre-cropped to square and saved as 1024 × 1024 PNGs.

Each attribution record contains the original image URL, source/landing page, title, creator, provider, license, license URL, source dimensions and downloaded-file SHA-256. Downloads resume safely: a local image is skipped only when its recorded checksum matches; missing, legacy or corrupted files are reacquired. The Termux publisher requires exactly 100 unique domain images and 100 valid attribution records before it commits and pushes anything.

Openverse is an index of openly licensed media from multiple providers, not a guarantee that every search result is scientifically appropriate. Inspect the original source page and image relevance before treating the gallery as editorially approved. If a domain has no suitable qualifying result, the downloader stops rather than inserting a placeholder; rerun it later to retry missing domains.

## Pixel animation

Regenerate the local banner with:

~~~bash
python -m pip install Pillow
python scripts/build_pixel_animation.py
~~~

The currently tracked legacy GIF fails structural validation and is intentionally not embedded by the README. The generator writes Assets/Future/kinetics-science-quest.gif as a 32-frame, 320 × 120 GIF and verifies its dimensions, frame count and infinite-loop metadata. Run the generator, validate the output, then commit the replacement binary. Keep the path case-sensitive.

## Validation before commit

~~~bash
python scripts/validate_visual_assets.py
~~~

Validation checks PNG integrity, GIF frame count, dimensions and attribution coverage. Do not publish the gallery as complete unless all 100 PNGs and attribution records are present.
