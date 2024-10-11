#independent
import os
import time
import uuid
import datetime
import torch
import gc
import shutil

import warnings
warnings.simplefilter("ignore")

#AUDIO_DOWNLOAD
import re
import wget
import librosa
import soundfile as sf

def AUDIO_DOWNLOAD(callSid, audio_URL):

    pattern=r'^https?://[^\s/$.?#].[^\s]*$'
    if re.match(pattern, audio_URL):
      path=f"{callSid}.wav"
      audio_response = wget.download(audio_URL, path)
      AUDIO_FILENAME=audio_response
      print(f"Processing downloaded audio...")
    else:
      AUDIO_FILENAME=audio_URL
      print(f"Processing local audio...")

    signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)
    duration=round(signal.shape[0]/(sample_rate*60), 2)

    if sample_rate>8000:
        new_sr = 8000
        audio_resampled = librosa.resample(y=signal, orig_sr=sample_rate, target_sr=new_sr)
        output_file = f"{AUDIO_FILENAME.split('/')[-1].split('.')[0]}.wav"
        sf.write(output_file, audio_resampled, new_sr)
        AUDIO_FILENAME=output_file

    return AUDIO_FILENAME, duration


#STT
import json
import subprocess

def STT(AUDIO_FILENAME, device):

    command=f"whisper {AUDIO_FILENAME}  --model medium --language en --device {device} --word_timestamps True"
    data= subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.readlines()


    output_json=AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json"
    files=os.listdir(os.getcwd())
    if output_json in files:
        with open(output_json, "r") as f:
            result=json.load(f)

    word_ts_hyp={AUDIO_FILENAME.split('/')[-1].split('.')[0]:[]}
    word_hyp={AUDIO_FILENAME.split('/')[-1].split('.')[0]:[]}

    for item in result['segments']:
        for stamp in item['words']:
            word_ts_hyp[AUDIO_FILENAME.split('/')[-1].split('.')[0]].append([stamp['start'], stamp['end']])

    for item in result['segments']:
        for stamp in item['words']:
            word_hyp[AUDIO_FILENAME.split('/')[-1].split('.')[0]].append(stamp['word'])

    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".tsv"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".tsv")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".srt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".srt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".txt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".txt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".vtt"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".vtt")
    if os.path.exists(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json"):
        os.remove(AUDIO_FILENAME.split('/')[-1].split('.')[0]+".json")

    return word_hyp, word_ts_hyp

#DIARIZATION
from omegaconf import OmegaConf
from nemo.collections.asr.parts.utils.diarization_utils import OfflineDiarWithASR

def DIARIZATION(domain_type, AUDIO_FILENAME, word_hyp, word_ts_hyp, device):

    path=os.path.join(os.getcwd(), 'dia_data')
    os.makedirs(path, exist_ok=True)
    CONFIG_FILE_NAME = f"diar_infer_{domain_type}.yaml"
    CONFIG_URL = f"https://raw.githubusercontent.com/NVIDIA/NeMo/main/examples/speaker_tasks/diarization/conf/inference/{CONFIG_FILE_NAME}"

    CONFIG = wget.download(CONFIG_URL, path)

    cfg = OmegaConf.load(CONFIG)
    cfg.device=str(device)

    meta = {
        'audio_filepath': AUDIO_FILENAME,
        'offset': 0,
        'duration':None,
        'label': 'infer',
        'text': '-',
        'num_speakers': None,
        'rttm_filepath': None,
        'uem_filepath' : None
    }
    input_manifest_file_path=os.path.join(path, 'input_manifest.json')
    with open(input_manifest_file_path,'w') as fp:
        json.dump(meta,fp)
        fp.write('\n')

    cfg.diarizer.manifest_filepath = input_manifest_file_path

    pretrained_speaker_model='titanet_large'
    cfg.diarizer.manifest_filepath = cfg.diarizer.manifest_filepath
    cfg.diarizer.out_dir = path #Directory to store intermediate files and prediction outputs
    cfg.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
    cfg.diarizer.clustering.parameters.oracle_num_speakers=False

    # Using Neural VAD and Conformer ASR
    cfg.diarizer.vad.model_path = 'vad_multilingual_marblenet'
    cfg.diarizer.asr.model_path = 'stt_en_conformer_ctc_large'
    cfg.diarizer.oracle_vad = False # ----> Not using oracle VAD
    cfg.diarizer.asr.parameters.asr_based_vad = False

    asr_diar_offline = OfflineDiarWithASR(cfg.diarizer)
    asr_diar_offline.word_ts_anchor_offset = 0.12

    diar_hyp, diar_score = asr_diar_offline.run_diarization(cfg, word_ts_hyp)

    trans_info_dict = asr_diar_offline.get_transcript_with_speaker_labels(diar_hyp, word_hyp, word_ts_hyp)

    dia_json=os.path.join(path, 'pred_rttms', f"{AUDIO_FILENAME.split('/')[-1].split('.')[0]}.json")
    if os.path.exists(os.path.join(os.getcwd() ,AUDIO_FILENAME)):
        with open(dia_json) as f:
            diarized_transcription=json.load(f)

    try:
        shutil.rmtree(path)
    except Exception as e:
        print('error: ', e)

    return diarized_transcription

#SPEAKER MATCH FUNCTIONS
import numpy as np
from pyannote.audio import Model, Inference

#SIMILARITY MATCH
def SPEAKER_EMBEDDINGS_SIMILARITY(agent_audio_embeddings, audio2_embeddings):
    X=min(agent_audio_embeddings.shape[0], audio2_embeddings.shape[0])

    dot_product = np.dot(agent_audio_embeddings[:X, :].flatten(), audio2_embeddings[:X, :].flatten())
    norm_vec1 = np.linalg.norm(agent_audio_embeddings)
    norm_vec2 = np.linalg.norm(audio2_embeddings)

    sim_idx=dot_product / (norm_vec1 * norm_vec2)

    return sim_idx

#AUDIO CLIPPING
def AUDIO_CLIPPING(directory_name, speaker, duration, audio_array, sample_rate):
    start_time = duration[0]
    end_time = duration[-1]

    start_sample = librosa.time_to_samples(start_time, sr=sample_rate)
    end_sample = librosa.time_to_samples(end_time, sr=sample_rate)

    segment = audio_array[start_sample:end_sample]

    segmented_audio=os.path.join(directory_name, speaker+'.wav')
    sf.write(segmented_audio, segment, sample_rate)

#MAIN SPEAKER MATCHING FUNCTION
def SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, agent_audio_URL, device, HF_TOKEN=None):

    pattern=r'^https?://[^\s/$.?#].[^\s]*$'
    if re.match(pattern, agent_audio_URL):
        agent_audio= wget.download(agent_audio_URL, os.getcwd())
        print("Processing downloaded speaker audio")
    else:
        agent_audio=os.path.join(os.getcwd(), agent_audio_URL)
        print("Processing local speaker audio")

    agent_name=agent_audio.split('/')[-1].split('.')[0]
    agent_speaker=""

    if HF_TOKEN:
        model = Model.from_pretrained("pyannote/embedding", HF_TOKEN=HF_TOKEN)
    else:
        model = Model.from_pretrained("pyannote/embedding")
    inference = Inference(model)
    inference.to(device)

    #extracting speaker segments
    list_of_spk={}
    for sentence in diarized_transcription['sentences']:
        spk=sentence['speaker']
        s_t=float(sentence['start_time'])
        e_t=float(sentence['end_time'])
        current_spk_duration=e_t-s_t

        if spk in list(list_of_spk.keys()):
            spk_duration=list_of_spk[spk][-1]-list_of_spk[spk][0]
            if current_spk_duration>spk_duration:
                list_of_spk[spk]=[s_t, e_t]
            else:
                pass
        else:
            list_of_spk[spk]=[s_t, e_t]

    # print(f"\nlist of spk: {list_of_spk}\n")

    #saving clipped audios in audio dir
    directory_name=os.path.join(os.getcwd(), 'spk_audio_clippings')
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    audio_array, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)

    for speaker in list(list_of_spk.keys()):
        AUDIO_CLIPPING(directory_name, speaker, list_of_spk[speaker], audio_array, sample_rate)

    #getting most similar speaker with agent
    agent_audio_embeddings=inference(agent_audio).data
    # print(f"agent audio embeddings: {type(agent_audio_embeddings)}")
    similarity_index=-100
    for audio2 in os.listdir(directory_name):
        audio2_embeddings=inference(os.path.join(directory_name, audio2)).data

        sim_index=SPEAKER_EMBEDDINGS_SIMILARITY(agent_audio_embeddings, audio2_embeddings)
        # print(f"similarity index of {agent_audio.split('/')[-1].split('.')[0]} with {audio2.split('/')[-1].split('.')[0]} is: {sim_index}")
        if sim_index>similarity_index:
            agent_speaker=audio2.split('/')[-1].split('.')[0]
            similarity_index=sim_index


    #changing speaker name with agent name
    for sentence in diarized_transcription['sentences']:
        if sentence['speaker']==agent_speaker:
            sentence['speaker']=agent_name

    for word in diarized_transcription['words']:
        if word['speaker']==agent_speaker:
            word['speaker']=agent_name

    try:
        shutil.rmtree(directory_name)
        # shutil.rmtree(agent_audio_path)
        # if os.path.exists(os.path.join(os.getcwd() ,AUDIO_FILENAME)):
        #   os.remove(os.path.join(os.getcwd() ,AUDIO_FILENAME))
    except Exception as e:
        print('Audio clippings and agent audio not removed due to error: ', e)

    return diarized_transcription

#DIRECTORY CLEAN
def clean_directory(directory_path):

    """
    Removes any json aur wav file from mentioned directory
    """

    decision=input("This function will remove all the jsons and wav files from mentioned directory, would you like to proceed: [y/n]:\n")
    if decision.lower()=='y':
        files=list(directory_path)
        files_to_remove=[]
        for f in files:
            if 'wav' in str(f):
                files_to_remove.append(f)
            if 'json' in str(f):
                files_to_remove.append(f)
        for item in files_to_remove:
            if os.path.exists(os.path.join(os.getcwd(), item)):
                os.remove(os.path.join(os.getcwd(), item))

        print(f"These files are removed from directory {directory_path}: {files_to_remove}")
    
    elif decision.lower()=='n':
        print("Files not removed")
    else:
        print("Invalid input process aborted")


#MAIN
def transcribe(audio: str, speaker_audio: str=None, HF_TOKEN: str=None, tag: dict={"message": "speech text pipeline run"}):

    """
    The main function to transcribe and diarize given audio.

    Parameters:
    - audio (str): Expects a string input representing the path/link to the audio file.
    - speaker_audio (str, optional): Expects a string input representing the path/link to an additional speaker audio file.
    - HF_TOKEN (str, optional): Expects a string input representing the Hugging Face token.
    - tag (dict, optional): Expects a dictionary input containing additional metadata for tagging, defaulting to {"message": "speech text pipeline run"}.
    """

    domain_type="meeting"
    callSid=str(uuid.uuid4())
    output={
            "metadata": {
            "request_id": "",
            "created_at": "",
            "duration":"",
            "language":"en",
            "process_time_taken":"",
            "audio":"",
            "model_info": {"transcription_model":"medium",
                            "diarization":{"VAD": "vad_multilingual_marblenet",
                                            "speaker_embedings": "titanet_large"}}
            },
            "results": {"channels": [{"alternatives":[{"transcript": "",
                                                        "confidence": 0,
                                                        "sentences": [],
                                                        "words":[]}]}]}
    }

    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Processing on {device}")

    if os.path.exists(os.path.join(os.getcwd(), 'dia_data')):
        shutil.rmtree(os.path.join(os.getcwd(), 'dia_data'))

    t1=time.time()

    #SUBPROCESS-1
    try:
        AUDIO_FILENAME, duration=AUDIO_DOWNLOAD(callSid, audio)

    except Exception as e:

        return_json={"status": f"No process completed for callSid: {callSid}", "return_message": f"Error in downloading audio: {e}"}
        return return_json

    #SUBPROCESS-2
    try:
        word_hyp, word_ts_hyp=STT(AUDIO_FILENAME, device)
        print(f"Audio transcribed")

    except Exception as e:
        return_json={"status": f"Process completed till audio download for callSid: {callSid}", "return_message": f"Error in transcribing: {e}"}
        return return_json

    #SUBPROCESS-3
    try:
        diarized_transcription=DIARIZATION(domain_type, AUDIO_FILENAME, word_hyp, word_ts_hyp, device)
        print("Audio diarized")

    except Exception as e:
        return_json={"status": f"Process completed till transcribing for callSid: {callSid}", "return_message": f"Error in diarizing: {e}"}
        return return_json

    #SUBPROCESS-4
    if speaker_audio!=None:
        try:
            if HF_TOKEN:
                diarized_transcription=SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, speaker_audio, device, HF_TOKEN)
                print("Speaker audio processed and matched succefully")
            else:
                diarized_transcription=SPEAKER_MATCHING(AUDIO_FILENAME, diarized_transcription, speaker_audio, device)
                print("Speaker audio processed and matched succefully")
        except Exception as e:
          return_json={"status": f"Process completed till diarizing for callSid: {callSid}", "return_message": f"Error in Speaker matching: {e}"}
          return return_json

    speaker_names=set()
    for sentence in diarized_transcription['sentences']:
      speaker_names.add(sentence['speaker'])

    #SUBPROCESS-5
    try:

        output['metadata']['tag']=tag
        output['metadata']['request_id']+=callSid
        output['metadata']['created_at']+=str(datetime.datetime.now())
        output['metadata']['duration']+=str(duration)+' mins'
        output['metadata']['process_time_taken']+=str(round(time.time()-t1,2))+' secs'
        output['metadata']['audio']+=audio
        output['metadata']['speaker_count']=diarized_transcription['speaker_count']
        output['metadata']['speaker_names']=list(speaker_names)
        output['results']['channels'][0]['alternatives'][0]['transcript']=diarized_transcription['transcription']
        output['results']['channels'][0]['alternatives'][0]['confidence']=0.94
        output['results']['channels'][0]['alternatives'][0]['sentences']=diarized_transcription['sentences']
        output['results']['channels'][0]['alternatives'][0]['words']=diarized_transcription['words']

    except Exception as e:

        return_json={"status": f"Process completed till Speaker matching for callSid: {callSid}", "return_message": f"Error in filling data: {e}"}

        return return_json

    torch.cuda.empty_cache()
    gc.collect()

    print("process completed")
    return output