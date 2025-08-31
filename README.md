# MatSynth-Captions: Text Prompts for Material Videos

**Summary.** This repository releases text captions for the MatSynth dataset videos to support material understanding, retrieval, and generation research. We provide both the original captions and a cleaned variant that removes sentences containing the *standalone* words **light**, **lighting**, or **illumination** (case-insensitive), as requested by collaborators.

## What's Inside
- `data/captions_v1.csv`: Original captions.
- `data/captions_v1_clean.csv`: Cleaned captions (removes sentences with standalone `light|lighting|illumination`, keeps `light-colored`, `daylight`, `highlight`, etc.). Also guarantees “one record per line”.
- `scripts/clean_captions_exact.py`: Reproducible cleaning script.

## Data Format
Each row corresponds to one video:
- `folder` — material/category folder name
- `video_file` — filename (e.g., `btf_sequence.mp4`)
- `video_path` — original absolute path (optional for release)
- `caption` — the text description

> Example header: `folder,video_file,video_path,caption`

## Reproducing the Cleaned File
```bash
python scripts/clean_captions_exact.py \
  -i data/captions_v1.csv \
  -o data/captions_v1_clean.csv \
  -c caption \
  --drop-empty
