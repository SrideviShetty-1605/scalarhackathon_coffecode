"""
Simple wrapper for WebRTC voice activity detection.
"""

import webrtcvad

def make_vad(mode=2):
    v = webrtcvad.Vad()
    v.set_mode(mode)
    return v
