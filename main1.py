# In[]

import whisper
from whisper.utils import get_writer

# In[]

model = whisper.load_model("base")


# In[]
audio_file = "a.mp3"   

# IN[]

result = model.transcribe(audio_file)

# In[]

print("Transcription:")
print(result["text"])
# %%
