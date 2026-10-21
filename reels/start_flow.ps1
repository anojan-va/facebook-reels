# Start the flow-mcp server (Flow Studio, http://127.0.0.1:8787) with the real ffmpeg/ffprobe first on PATH.
# Chocolatey's ffprobe shim is blocked by Application Control on this PC; the real binary is allowed.
# After it starts, reopen the Flow project: node D:\Claude\reels\open_project.mjs <project-url>
$env:PATH = "C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin;$env:PATH"
Set-Location C:\Users\Anojan\flow-mcp
node dist/studio.js
