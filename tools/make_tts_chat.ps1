param(
  [string]$Text = "Chat",
  [string]$OutFile = "assets\audio\exnulla-tts-chat.wav"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Speech

$root = Split-Path -Parent $PSScriptRoot
$outPath = Join-Path $root $OutFile
$outDir = Split-Path -Parent $outPath
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Try to pick an installed female voice (best-effort)
$voices = $synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo }
$female = $voices | Where-Object { $_.Gender -eq "Female" } | Select-Object -First 1
if ($female) { $synth.SelectVoice($female.Name) }

$synth.Rate = 0      # -10..10
$synth.Volume = 80   # 0..100

# Write WAV
$synth.SetOutputToWaveFile($outPath)
$synth.Speak($Text)
$synth.SetOutputToDefaultAudioDevice()

Write-Host "Wrote: $outPath"
Write-Host "Voice: " ($synth.Voice.Name)

