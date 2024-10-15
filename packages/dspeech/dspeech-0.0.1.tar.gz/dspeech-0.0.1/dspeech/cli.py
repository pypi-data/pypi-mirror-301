import argparse
import logging
import os
import sys
from rich.console import Console

from dspeech.stt import STT

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console = Console()

def parse_args():
    parser = argparse.ArgumentParser(
        description="DSpeech: A Command-line Speech Processing Toolkit"
    )

    parser.add_argument(
        "command", 
        choices=["transcribe", "vad", "punc", "emo", "help"], 
        help="Choose the function: transcribe, vad, punc, emo"
    )

    parser.add_argument(
        "--model", 
        default="paraformer-zh", 
        help="Model name (paraformer-zh, sensevoicesmall)"
    )

    parser.add_argument(
        "--vad-model", 
        default="fsmn-vad", 
        help="VAD model name (default: fsmn-vad)"
    )

    parser.add_argument(
        "--punc-model", 
        default="ct-punc", 
        help="Punctuation model name (default: ct-punc)"
    )

    parser.add_argument(
        "--emo-model", 
        default="emotion2vec_plus_large", 
        help="Emotion model name (default: emotion2vec_plus_large)"
    )

    parser.add_argument(
        "--device", 
        default="cuda", 
        help="Device to run the models on (default: cuda)"
    )

    parser.add_argument(
        "--file", 
        help="Audio file path for transcribing, VAD, or emotion classification"
    )

    parser.add_argument(
        "--text", 
        help="Text to process with punctuation model"
    )

    parser.add_argument(
        "--start", 
        type=float, 
        default=0, 
        help="Start time in seconds for processing audio files (default: 0)"
    )

    parser.add_argument(
        "--end", 
        type=float, 
        default=-1, 
        help="End time in seconds for processing audio files (default: end of file)"
    )

    parser.add_argument(
        "--sample-rate", 
        type=int, 
        default=16000, 
        help="Sample rate of the audio file (default: 16000)"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    if not args.command:
        console.print("[red]No command provided. Use `dspeech help` for help.")
        sys.exit(1)
    
    if args.command == "help" or args.command == "-h" or args.command == "--help" or args.command == "h" or args.command == "--h" or args.command == "-help":
        console.print("[green]DSpeech: A Command-line Speech Processing Toolkit")
        console.print("[yellow]Usage: dspeech [command] [options]")
        console.print("[yellow]Commands:")
        console.print("[yellow]  transcribe  Transcribe an audio file")
        console.print("[yellow]  vad         Perform VAD on an audio file")
        console.print("[yellow]  punc        Add punctuation to a text")
        console.print("[yellow]  emo         Perform emotion classification on an audio file")
        console.print("[blue]Options:")
        console.print("[blue]  --model      Model name (default: sensevoicesmall)")
        console.print("[blue]  --vad-model  VAD model name (default: fsmn-vad)")
        console.print("[blue]  --punc-model Punctuation model name (default: ct-punc)")
        console.print("[blue]  --emo-model  Emotion model name (default: emotion2vec_plus_large)")
        console.print("[blue]  --device     Device to run the models on (default: cuda)")
        console.print("[blue]  --file       Audio file path for transcribing, VAD, or emotion classification")
        console.print("[blue]  --text       Text to process with punctuation model")
        console.print("[blue]  --start      Start time in seconds for processing audio files (default: 0)")
        console.print("[blue]  --end        End time in seconds for processing audio files (default: end of file)")
        console.print("[blue]  --sample-rate Sample rate of the audio file (default: 16000)")
        console.print(f"[green]Example: dspeech transcribe --file audio.wav")
        sys.exit(0)

    handler = STT(
        model_name=args.model,
        vad_model=args.vad_model,
        punc_model=args.punc_model,
        emo_model=args.emo_model,
        device=args.device
    )

    if args.command == "transcribe":
        if not args.file:
            console.print("[red]Please provide an audio file for transcription.")
            sys.exit(1)
        console.print(f"[green]Transcribing {args.file}...")
        result = handler.transcribe_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]Transcription: {result}")

    elif args.command == "vad":
        if not args.file:
            console.print("[red]Please provide an audio file for VAD.")
            sys.exit(1)
        console.print(f"[green]Performing VAD on {args.file}...")
        vad_result = handler.vad_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]VAD Result: {vad_result}")

    elif args.command == "punc":
        if not args.text:
            console.print("[red]Please provide text for punctuation.")
            sys.exit(1)
        console.print(f"[green]Adding punctuation to: {args.text}")
        punc_result = handler.punc_result(args.text)
        console.print(f"[yellow]Punctuation Result: {punc_result}")

    elif args.command == "emo":
        if not args.file:
            console.print("[red]Please provide an audio file for emotion classification.")
            sys.exit(1)
        console.print(f"[green]Performing emotion classification on {args.file}...")
        emo_result = handler.emo_classify_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]Emotion Classification Result: {emo_result}")

if __name__ == "__main__":
    main()
