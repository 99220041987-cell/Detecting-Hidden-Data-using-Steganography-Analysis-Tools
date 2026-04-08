
# Detecting Hidden Data using Steganography Analysis Tools

Python-based steganalysis tool to detect hidden data in images using LSB extraction, chi-square testing, and entropy analysis.

## Features
- Extracts LSB planes for R/G/B channels
- Computes chi-square statistics on LSB distributions
- Measures entropy to flag suspicious randomness
- Outputs a clear analysis report

## Requirements
- Python 3.8+
- Pillow
- NumPy

Install dependencies:
```bash
pip install pillow numpy
