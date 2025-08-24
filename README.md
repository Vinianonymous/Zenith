# Current Stage: V0.5 
## Development Goals
Currently the code in itself is morphing into a new thing, different from the structure given here, so describing each element of this system would be to count the infinite.
For the goals, it is still unclear as to where this will go.

## Overview of each module
Giving off a quick briefing on each file you see here.
- sre.py: The absolute *core* of this whole thing. SRE stands for short term engagement and refers to the daily *to-dos* or *goals*. It directly connects, per execution, to the:
- timer.py: Features a clock with an forever loop, working as a (Only, for now) stopwatch. The loop engages the
- mediahandler.py: Downloads audio from youtube URL and is used by timer.py to play a random selected audio from a media folder.
- altar.py: Uses altar.json for data, this prototype accounts for an area or pillar of life and represents how I'm Improving or worsening. It's currently separated from the rest. 
