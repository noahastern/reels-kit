"""Waveform helpers for cutting talking-head footage on the voice, not the transcript."""
import subprocess
import numpy as np

SR = 48000
HOP = 0.001  # 1ms envelope resolution
WIN = 0.010  # 10ms RMS window


def load(path, sr=SR):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def envelope(x, sr=SR):
    """RMS in dB every 1ms, full band and above ~3kHz (catches s, f, t, breaths)."""
    hop, win = int(HOP * sr), int(WIN * sr)
    # crude high-pass: first difference twice (~+12dB/oct), fine for finding sibilant tails
    hf = np.diff(x, n=2, prepend=[0, 0])
    n = (len(x) - win) // hop
    idx = np.arange(n) * hop
    c = np.concatenate([[0], np.cumsum(x.astype(np.float64) ** 2)])
    ch = np.concatenate([[0], np.cumsum(hf.astype(np.float64) ** 2)])
    full = 10 * np.log10((c[idx + win] - c[idx]) / win + 1e-12)
    high = 10 * np.log10((ch[idx + win] - ch[idx]) / win + 1e-12)
    return full, high


class Voice:
    def __init__(self, path):
        self.x = load(path)
        self.full, self.high = envelope(self.x)
        self.floor = np.percentile(self.full, 8)
        self.hfloor = np.percentile(self.high, 8)
        self.speech = np.percentile(self.full, 75)

    def t2i(self, t):
        return int(round(t / HOP))

    def voiced(self, i, margin_full=12, margin_high=10):
        return (self.full[i] > self.floor + margin_full) or (self.high[i] > self.hfloor + margin_high)

    def quietest(self, t0, t1):
        a, b = self.t2i(t0), self.t2i(t1)
        k = a + int(np.argmin(self.full[a:b]))
        return k * HOP

    def onset(self, t_from, t_limit):
        """First voiced ms at or after t_from (searching forward to t_limit)."""
        for i in range(self.t2i(t_from), self.t2i(t_limit)):
            if all(self.voiced(j) for j in range(i, i + 15)):  # 15ms of sound, not a click
                # walk back to where it first rose out of the floor (soft starts)
                k = i
                while k > 0 and (self.full[k] > self.floor + 6 or self.high[k] > self.hfloor + 5):
                    k -= 1
                return k * HOP
        return None

    def offset(self, t_from, t_limit):
        """Last voiced ms at or before t_from (searching backward to t_limit)."""
        for i in range(self.t2i(t_from), self.t2i(t_limit), -1):
            if all(self.voiced(j) for j in range(i - 15, i)):
                k = i
                while k < len(self.full) - 1 and (self.full[k] > self.floor + 6 or self.high[k] > self.hfloor + 5):
                    k += 1
                return k * HOP
        return None

    def level(self, t0, t1):
        a, b = self.t2i(t0), self.t2i(t1)
        return float(np.max(self.full[a:b]))
