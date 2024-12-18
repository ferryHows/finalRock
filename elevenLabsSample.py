from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="e75347c1353dd3083be81b47c4705fd6", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="Hello!",
  voice="Rachel", # try Nicole
  model="eleven_multilingual_v2"
)
play(audio)