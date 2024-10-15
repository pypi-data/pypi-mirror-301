import os
import logging
import numpy as np
from funasr import AutoModel
from time import perf_counter
from rich.console import Console
console = Console()

import torch
import soundfile
import torchaudio
from dspeech.base_handler import BaseHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

class STT():
    def __init__(
        self,
        model_name="paraformer-zh", #"paraformer-zh",
        device="cuda",
        gen_kwargs={},
        vad_model="fsmn-vad", #"fsmn-vad",
        punc_model="ct-punc", #"ct-punc",
        emo_model="emotion2vec_plus_large",
    ):
        console.print(f"[green] Model Name: {model_name}")
        console.print(f"[green] Device: {device}")
        console.print(f"[green] VAD Model: {vad_model}")
        console.print(f"[green] Punctuation Model: {punc_model}")
        try:
            self.DSPEECH_HOME = os.environ["DSPEECH_HOME"]
        except KeyError:
            console.print("[red]Please set DSPEECH_HOME in your environment variables.")
            console.print("[red]export DSPEECH_HOME=/path/to/dspeech")

        model_name = f"{self.DSPEECH_HOME}/{model_name}"
        self._check_model(model_name)
        if vad_model:
            vad_model = f"{self.DSPEECH_HOME}/{vad_model}"
            self._check_model(vad_model)
        if punc_model:
            punc_model = f"{self.DSPEECH_HOME}/{punc_model}"
            self._check_model(punc_model)
        if emo_model:
            emo_model = f"{self.DSPEECH_HOME}/{emo_model}"
            self._check_model(emo_model)

        self.device = device
        if vad_model is not None:
            self.vad_model = AutoModel(model=vad_model, device=device, disable_update=True)
        if punc_model is not None:
            self.punc_model = AutoModel(model=punc_model, device=device, disable_update=True)
        if emo_model is not None:
            self.emo_model = AutoModel(model=emo_model, device=device, disable_update=True)
        self.model = AutoModel(model=model_name,
                        device=device,disable_update=True,
                        vad_model=None,
                        punc_model=None,
                        )
        self.warmup()

    def _check_model(self, _path):
        if not os.path.exists(_path):
            console.print(f"[red]Model {_path} not found.")
            console.print("[red]Please check the path.")
            console.print("[red]Please set DSPEECH_HOME in your environment variables.")
            console.print("[red]export DSPEECH_HOME=/path/to/dspeech")
            console.print("[green] You can download the model by:")
            console.print("[green] 1. export HF_ENDPOINT=https://hf-mirror.com")
            console.print("[green] 2. huggingface-cli download --resume-download <model_id> --local-dir $DSPEECH_HOME/<model_name>")
            raise FileNotFoundError
        else:
            console.print(f"[green]Model {_path} found in {self.DSPEECH_HOME}")
    
    def _load_file(self, file_path, start=0, end=-1, sample_rate=16000, channel=0):
        """Extracts audio from file_path based on start, end, and sample_rate.

        Args:
            file_path (str): file path to the audio file
            start (float): start time in seconds, default 0
            end (float): end time in seconds, default -1 (end of file)
            sample_rate (int): sample rate of the audio
            channel (int): channel of the audio file, default 0 (-1 for all channels)
        """
        audio, sr = torchaudio.load(file_path)
        if sr != sample_rate:
            # resample by torchaudio
            transform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=sample_rate)
            audio = transform(audio)
            sr = sample_rate
            console.print(f"[yellow]Resampled audio to {sample_rate} Hz")
        
        if channel != -1:
            audio = audio[channel, :]
        else:
            # merge all channels to mono, by taking mean
            audio = audio.mean(dim=0)
        audio = audio.reshape(-1)
        logger.debug(f"Loaded audio with shape {audio.shape} and sample rate {sr}")
        logger.debug(f"start: {start}, end: {end}")
        logger.debug(f"audio length: {len(audio)/sr}")
        if end == -1:
            end = len(audio) / sr
            console.print(f"[yellow]End time not provided, setting end to {end}")
        start = int(start * sr)
        end = int(end * sr)
        audio = audio[start:end]
        console.print(f"[green]Start: {start}, End: {end}")
        console.print(f"[green]Loaded audio with shape {audio.shape} and sample rate {sample_rate}")
        return audio


    def warmup(self):
        logger.info(f"Warming up {self.__class__.__name__}")
        # 2 warmup steps for no compile or compile mode with CUDA graphs capture
        n_steps = 1
        dummy_input = np.array([0] * 512, dtype=np.float32)
        for _ in range(n_steps):
            _ = self.model.generate(dummy_input)[0]["text"].strip()

    def vad(self, audio_data):
        logger.debug("performing VAD...")
        res = self.vad_model.generate(input=audio_data)
        _ = res[0]["value"]
        return _

    def vad_file(self, audio_path, start=0, end=-1, sample_rate=16000):
        logger.debug(f"performing VAD on {audio_path}")
        audio_data = self._load_file(audio_path, start, end, sample_rate)
        res = self.vad_model.generate(input=audio_data)
        _ = res[0]["value"]
        return _

    def punc_result(self, text):
        logger.debug(f"performing punctuation on {text}")
        res = self.punc_model.generate(input=text)
        return res[0]["text"]

    def emo_classify(self, audio_data):
        logger.debug("performing emotion classification...")
        res = self.emo_model.generate(audio_data, output_dir=None, granularity="utterance", extract_embedding=False)
        return res[0]

    def emo_classify_file(self, audio_path, start=0, end=-1, sample_rate=16000):
        logger.debug(f"performing emotion classification on {audio_path}")
        audio_data = self._load_file(audio_path, start, end, sample_rate)
        res = self.emo_model.generate(audio_data, output_dir=None, granularity="utterance", extract_embedding=False)
        return res[0]

    def transcribe(self, spoken_prompt):
        logger.debug("infering paraformer...")
        pred_text = (
            self.model.generate(spoken_prompt,)[0]["text"].strip()#.replace(" ", "") # hotword="STT/hot_word.txt"
        )
        try:
            torch.mps.empty_cache()
        except Exception as e:
            logger.debug(f"Error emptying cache: {e}")
            # empty for windows
            torch.cuda.empty_cache()
        logger.debug("finished paraformer inference")
        yield pred_text

    def transcribe_file(self, audio_path, start=0, end=-1, sample_rate=16000):
        logger.debug(f"transcribing file: {audio_path}")
        audio_data = self._load_file(audio_path, start, end, sample_rate)
        pred_text = self.model.generate(audio_data)[0]["text"].strip()
        try:
            torch.mps.empty_cache()
        except Exception as e:
            logger.debug(f"Error emptying cache: {e}")
            # empty for windows
            torch.cuda.empty_cache()
        console.print(f"[yellow]{pred_text}")
        return pred_text

    # TODO: streaming
    def transcribe_streaming(self, spoken_prompt,
            chunk_size=[0, 10, 5],
            encoder_chunk_look_back=4,
            decoder_chunk_look_back=1):
        cache = {}
        chunk_stride = chunk_size[1] * 960 # 600ms
        total_chunk_num = int(len((spoken_prompt)-1)/chunk_stride+1)
        for i in range(total_chunk_num):
            speech_chunk = spoken_prompt[i*chunk_stride:(i+1)*chunk_stride]
            is_final = i == total_chunk_num - 1
            res = self.model.generate(input=speech_chunk, cache=cache,
                    is_final=is_final,
                    chunk_size=chunk_size,
                    encoder_chunk_look_back=encoder_chunk_look_back,
                    decoder_chunk_look_back=decoder_chunk_look_back)
            yield res
    
    # TODO: streaming
    def transcribe_file_streaming(self, audio_path,
            chunk_size=[0, 10, 5],
            encoder_chunk_look_back=4,
            decoder_chunk_look_back=1):
        speech, sample_rate = soundfile.read(wav_file)
        chunk_stride = chunk_size[1] * 960 # 600ms
        cache = {}
        total_chunk_num = int(len((speech)-1)/chunk_stride+1)
        for i in range(total_chunk_num):
            speech_chunk = speech[i*chunk_stride:(i+1)*chunk_stride]
            is_final = i == total_chunk_num - 1
            res = self.model.generate(input=speech_chunk, cache=cache,
                    is_final=is_final,
                    chunk_size=chunk_size,
                    encoder_chunk_look_back=encoder_chunk_look_back,
                    decoder_chunk_look_back=decoder_chunk_look_back)
            yield res

if __name__ == "__main__":
    handler = STT(model_name="sensevoicesmall")
    # test streaming
    wav_file = "/home/zhaosheng/Documents/dspeech/output.wav"
    # for text in handler.transcribe_file_streaming(wav_file):
    #     print(text)
    r  = handler.transcribe_file(wav_file)
    print(r) # 内容文本（没有标点符号）

    punch_r = handler.punc_result(r)
    print(punch_r) # 内容文本（有标点符号）

    emo_r = handler.emo_classify_file(wav_file)
    print(emo_r)
    # {'key': 'output', 'labels': ['生气/angry', '厌恶/disgusted', '恐惧/fearful', '开心/happy', '中立/neutral', '其他/other', '难过/sad', '吃惊/surprised', '<unk>'], 'scores': [0.002443524543195963, 0.0005927020683884621, 0.000142281613079831, 0.0011242007603868842, 0.8432592153549194, 4.7565237764501944e-05, 0.15228582918643951, 0.0001042649382725358, 3.884194370584737e-07]}

    vad_r = handler.vad_file(wav_file)
    print(vad_r)
    # [[600, 3050], [3840, 9090], [9590, 17300], [17650, 22120], [23470, 27460], [28490, 31400], [31680, 34530], [34860, 52200], [52480, 53710], [53990, 60030], [60310, 66860], [67140, 71060], [71380, 91250], [91530, 95980], [97220, 106620], [108010, 111670], [112060, 117940], [118220, 125550], [126020, 131180], [131710, 138530], [139130, 140120], [142060, 143080]]