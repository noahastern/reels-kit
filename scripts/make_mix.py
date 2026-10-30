#!/usr/bin/env python3
"""Mix the voice, sound effects and music from sounds.json and put them on the rendered picture.

    python3 make_mix.py <picture> <out prefix> [--sounds sounds.json] [--target -20.5]

Writes <out prefix>-sfx.mp4 and <out prefix>-music.mp4. The voice is never limited or
compressed: everything, voice included, gets one master gain that brings the sfx version
to --target LUFS, less if either version's true peak would pass -1dBTP. File paths in
sounds.json are relative to sounds.json. See reference/sound.md for its format.
"""
import argparse, json, os, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument('picture'); ap.add_argument('out')
ap.add_argument('--sounds', default='sounds.json')
ap.add_argument('--target', type=float, default=-20.5)
args = ap.parse_args()

base = os.path.dirname(os.path.abspath(args.sounds))
d = json.load(open(args.sounds))
p = lambda f: os.path.join(base, f)
END = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', args.picture],
                           capture_output=True, text=True, check=True).stdout.strip())
mixdir = os.path.join(base, 'mix')
os.makedirs(mixdir, exist_ok=True)
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
sfx = d.get('sfx', [])
files = sorted(set(s['file'] for s in sfx))
idx = {f: i + 1 for i, f in enumerate(files)}  # 0 = voice
uses = {f: [s for s in sfx if s['file'] == f] for f in files}


def graph(with_music):
    lines, labels = [], []
    for f in files:
        n, i, stem = len(uses[f]), idx[f], re.sub(r'\W', '', os.path.basename(f).rsplit('.', 1)[0])
        outs = ''.join(f'[{stem}{k}]' for k in range(n))
        lines.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo' + (f',asplit={n}' if n > 1 else '') + outs)
        for k, s in enumerate(uses[f]):
            dur = min(s['dur'], END - s['at'])
            ad = int(round(s['at'] * 1000))
            lab = 'o_' + re.sub(r'\W', '_', s['id'])
            # delays written out literally: never through a shell variable
            lines.append(f"[{stem}{k}]atrim=start={s.get('ms', 0)}:duration={dur:.3f},asetpts=PTS-STARTPTS,"
                         f"afade=t=out:st={max(dur - 0.04, 0):.3f}:d=0.04,volume={s['vol']},adelay={ad}|{ad}[{lab}]")
            labels.append(f'[{lab}]')
    if with_music:
        m, mi = d['music'], len(files) + 1
        gain = f"volume={m['vol']}"
        if 'dip' in m:
            q = m['dip']
            g = 10 ** (q['db'] / 20)
            env = f"if(lt(t,{q['back']}),clip((t-{q['at']})/{q['down']},0,1),clip(1-(t-{q['back']})/{q['up']},0,1))"
            gain += f",volume='1-{1 - g:.4f}*{env}':eval=frame"
        fade = f",afade=t=out:st={END - m['fade_out']:.3f}:d={m['fade_out']}" if 'fade_out' in m else ''
        fade_in = f",afade=t=in:d={m['fade_in']}" if 'fade_in' in m else ''
        lines.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={m.get('ms', 0)}:duration={END},"
                     f"asetpts=PTS-STARTPTS,{gain}{fade_in}{fade}[music]")
        labels.append('[music]')
    lines.append('[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo[voice]')
    lines.append('[voice]' + ''.join(labels) + f'amix=inputs={len(labels) + 1}:normalize=0:duration=first[mix]')
    return ';\n'.join(lines)


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1])


kinds = ['sfx'] + (['music'] if d.get('music') else [])
mixes = {}
for kind in kinds:
    gfile = os.path.join(mixdir, f'mix-{kind}.txt')
    open(gfile, 'w').write(graph(kind == 'music'))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', p(d['voice'])]
    for f in files:
        cmd += ['-i', p(f)]
    if kind == 'music':
        cmd += ['-i', p(d['music']['file'])]
    cmd += ['-/filter_complex', gfile, '-map', '[mix]', '-t', f'{END:.4f}', '-c:a', 'pcm_f32le', os.path.join(mixdir, f'raw-{kind}.wav')]
    subprocess.run(cmd, check=True)
    mixes[kind] = loudness(os.path.join(mixdir, f'raw-{kind}.wav'))

gain = min(args.target - mixes['sfx'][0], -1.0 - max(tp for _, tp in mixes.values()))
print('loudness, true peak', mixes, f'-> master gain {gain:+.2f}dB')
for kind in kinds:
    wav = os.path.join(mixdir, f'mix-{kind}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(mixdir, f'raw-{kind}.wav'), '-af', f'volume={gain:.2f}dB',
                    '-c:a', 'pcm_s24le', wav], check=True)
    v = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
         '-color_range', 'tv', '-colorspace', 'bt709', '-color_trc', 'bt709', '-color_primaries', 'bt709']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', args.picture, '-i', wav, '-map', '0:v:0', '-map', '1:a:0',
                    *v, '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', f'{args.out}-{kind}.mp4'], check=True)
    print('wrote', f'{args.out}-{kind}.mp4')
