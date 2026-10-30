"""List the jump cuts in a finished cut: frames that differ from the one before far more than their neighbours do.

    python3 find_jump_cuts.py cut.mov [--ratio 4]

Decodes the video small and grayscale, so it's quick even on 4K.
"""
import argparse, subprocess
from fractions import Fraction
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('--ratio', type=float, default=4.0)
args = ap.parse_args()

fps = Fraction(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                               '-of', 'default=nw=1:nk=1', args.video], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stdout.split()[0])
W, H = 90, 160
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', args.video, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True, check=True).stdout
frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W).astype(np.float32)
diff = np.r_[0, np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))]
for i in range(1, len(diff)):
    around = np.r_[diff[max(1, i - 6):i], diff[i + 1:i + 7]]
    if len(around) and diff[i] > args.ratio * max(np.median(around), 0.5):
        print(f'frame {i}  {float(i / fps):.3f}s  (diff {diff[i]:.1f}, neighbours {np.median(around):.1f})')
