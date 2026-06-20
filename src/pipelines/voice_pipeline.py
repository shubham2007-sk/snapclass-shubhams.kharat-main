from speechbrain.inference.speaker import EncoderClassifier
import numpy as np
import streamlit as st
import torch
import torchaudio
import soundfile as sf
import io


@st.cache_resource
def load_voice_encoder():
    return EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb"
    )


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        waveform, sample_rate = sf.read(
            io.BytesIO(audio_bytes)
        )

        waveform = torch.tensor(
            waveform,
            dtype=torch.float32
        )

        # Convert stereo to mono
        if waveform.ndim > 1:
            waveform = waveform.mean(dim=1)

        waveform = waveform.unsqueeze(0)

        # Resample to 16 kHz
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(
                sample_rate,
                16000
            )
            waveform = resampler(waveform)

        embedding = encoder.encode_batch(
            waveform
        )

        return (
            embedding.squeeze()
            .detach()
            .cpu()
            .numpy()
            .tolist()
        )

    except Exception as e:
        st.error(f"Voice recog error: {e}")
        return None


def identify_speaker(
    new_embedding,
    candidate_dict,
    threshold=0.65
):
    if new_embedding is None or not candidate_dict:
        return None, 0.0

    new_embedding = np.array(new_embedding)

    best_id = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():

        if stored_embedding is None:
            continue

        stored_embedding = np.array(stored_embedding)

        similarity = np.dot(
            new_embedding,
            stored_embedding
        ) / (
            np.linalg.norm(new_embedding)
            * np.linalg.norm(stored_embedding)
        )

        if similarity > best_score:
            best_score = similarity
            best_id = sid

    if best_score >= threshold:
        return best_id, best_score

    return None, best_score


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65
):
    try:
        embedding = get_voice_embedding(
            audio_bytes
        )

        sid, score = identify_speaker(
            embedding,
            candidates_dict,
            threshold
        )

        if sid:
            return {sid: score}

        return {}

    except Exception as e:
        st.error(f"Bulk process error: {e}")
        return {}