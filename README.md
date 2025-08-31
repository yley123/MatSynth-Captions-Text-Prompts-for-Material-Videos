# Rerendered MatSynth Captions (LLM-VL)

Captions generated from our re-rendered videos based on MatSynth assets, using a vision-language model (LLM-VL). This repository provides the original captions and a cleaned variant, plus a small script to reproduce the cleaning.

Data license: CC BY 4.0 | Code license: MIT | DOI: see "How to Cite"

---

## What's Inside

    [REPO_NAME]/
    ├─ captions_v1.csv           # Original captions (one record per line)
    ├─ captions_v1_clean.csv     # Cleaned captions (see rules below)
    ├─ clean_captions_exact.py   # Reproducible cleaning script
    ├─ README.md
    ├─ LICENSE                   # Data: CC BY 4.0; Code: MIT
    └─ CITATION.cff              # Citation metadata for this resource

Note on source data:
- Data source link: MatSynth project — [https://huggingface.co/datasets/gvecchio/MatSynth]

---

## Data Format

Each row corresponds to one video.

| Column     | Description                                   |
|------------|-----------------------------------------------|
| folder     | Material/category folder name                 |
| video_file | File name                                     |
| video_path | Original absolute path                        |
| caption    | Text prompt / description                     |

Example header:

    folder,video_file,video_path,caption

---

## Generation Pipeline (Brief)

1) Re-rendering (based on MatSynth assets)
- Renderer and version: Mitsuba 3.6.4
- Resolution / FPS: 1024 / 30

2) Captioning (LLM-VL)
- Model and version: Qwen2-VL

3) Post-processing
- Remove entire sentences that contain the standalone words "light", "lighting", or "illumination" (case-insensitive). Standalone means neither side is a letter, digit, underscore, or hyphen; thus "light-colored", "daylight", "highlight", "lights", "back-lighting" are kept.

---

## Reproduce the Cleaned File

    python scripts/clean_captions_exact.py \
      -i data/captions_v1.csv \
      -o data/captions_v1_clean.csv \
---

## Quick Start

    import pandas as pd
    df = pd.read_csv("data/captions_v1_clean.csv")
    print(df.head())

---

## License

- Captions (data): CC BY 4.0 — sharing and adaptation permitted with attribution.
- Scripts (code): MIT — permissive; keep copyright and license notices.

If you want downstream users to acknowledge this release, keep CC BY 4.0 for the data.

---

## How to Cite This Resource


BibTeX:

    @dataset{xue2025_rerendered_matsynth_captions,
      author  = {Bowen Xue, Zheng Zeng, Milos Hasan, Zahra Montazeri},
      title   = {Rerendered MatSynth Captions (LLM-VL)},
      year    = {2025},
      version = {1.0.0},
      doi     = {},
      url     = {https://github.com/yley123/MatSynth-Captions-Text-Prompts-for-Material-Videos}
    }

---



