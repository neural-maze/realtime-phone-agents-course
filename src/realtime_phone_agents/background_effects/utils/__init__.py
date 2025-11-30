from typing import List, Tuple

import numpy as np
from pydub import AudioSegment

AudioChunk = Tuple[int, np.ndarray]  # (sample_rate, samples)


def load_audio_chunks(
    path: str, target_rate: int = 16000, chunk_ms: int = 100
) -> List[AudioChunk]:
    """
    Load an audio file and split it into float32 [-1, 1] chunks suitable
    for the voice pipeline.
    """
    audio = AudioSegment.from_file(path).set_channels(1).set_frame_rate(target_rate)

    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= 32768.0  # normalize int16 to float32

    samples_per_chunk = int((target_rate * chunk_ms) / 1000)
    chunks: List[AudioChunk] = []

    for i in range(0, len(samples), samples_per_chunk):
        chunk = samples[i : i + samples_per_chunk]
        if len(chunk) == 0:
            continue
        chunks.append((target_rate, chunk))

    return chunks
