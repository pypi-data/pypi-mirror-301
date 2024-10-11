import speech_text_pipeline as stp

def test_transcribe_basic():
    audio_file = '/test/harvey_addidas_1min.wav'
    speaker="/test/Harvey.wav"
    spk_name='Harvey'
    
    result = stp.transcribe(audio=audio_file, speaker_audio=speaker, HF_TOKEN="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")

    assert result['metadata']['duration'] != ''
    assert result['metadata']['process_time_taken'] != ''
    assert result['metadata']['speaker_count'] != 0
    assert len(result['metadata']['speaker_names']) != 0
    assert 'Harvey' in result['metadata']['speaker_names']
    assert result['results']['channels'][0]['alternatives'][0]['transcript'] != ''
    assert len(result['results']['channels'][0]['alternatives'][0]['sentences']) != 0
    assert len(result['results']['channels'][0]['alternatives'][0]['words']) != 0