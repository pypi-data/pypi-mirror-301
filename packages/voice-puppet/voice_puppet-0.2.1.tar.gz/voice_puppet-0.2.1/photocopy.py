import voice_puppet
import sys

voice_puppet.load_tts()

source = sys.argv[1]
text = sys.argv[2]

for i in range(10):
    output = f"output_{i:03}.wav"
    voice_puppet.tts.tts_to_file(
        text=text, file_path=output, speaker_wav=source, language="en"
    )
    source = output
