"""Render the cut from the raw clip and shots.json: whole frames, a 4ms fade at every join.

    python3 render_cut.py <raw clip> cut-tight.mov shots.json

Re-encodes to 8-bit H.264 (crf 12, a keyframe every second so HyperFrames can seek)
with PCM audio. Rotation metadata (phones, some cameras) is applied on decode.
"""
import json, subprocess, sys
from fractions import Fraction

raw, out, shots_path = sys.argv[1], sys.argv[2], sys.argv[3]
shots = json.load(open(shots_path, encoding='utf-8'))
probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                        '-of', 'default=nw=1:nk=1', raw], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stdout.split()[0]
fps = Fraction(probe)
sr = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
                         '-of', 'default=nw=1:nk=1', raw], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stdout.split()[0])
gop = str(round(fps))


def sample(frame):
    return round(frame * sr / fps)


parts, labels = [], []
for k, s in enumerate(shots):
    a, b = s['src_in'], s['src_out']
    dur = (sample(b) - sample(a)) / sr
    parts.append(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{k}]")
    parts.append(f"[0:a]atrim=start_sample={sample(a)}:end_sample={sample(b)},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.004,afade=t=out:st={dur - 0.004:.6f}:d=0.004[a{k}]")
    labels.append(f"[v{k}][a{k}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(shots)}:v=1:a=1[v][a]"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-filter_complex', graph, '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-g', gop, '-keyint_min', gop,
                '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                '-c:a', 'pcm_s24le', out], check=True)
print('wrote', out, f'({sum(s["src_out"] - s["src_in"] for s in shots)} frames at {fps})')
