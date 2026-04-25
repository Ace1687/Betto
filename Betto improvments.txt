🟢 1. Core system stability (must fix first)

These are things that make everything else work properly:

Issues:
Interruptions (“are you still there?”)
Agent reacting while speaking / user talking
Wake word disabled / unstable
Emotion system not yet structured
Credit dependency on external AI calls
Fix plan:
Add conversation state machine
idle
listening
thinking
speaking
Block interruptions while speaking
Add silence timer properly (reset on input, not fixed timer)
Ensure wake word is optional fallback (hotkey is primary)
🎭 2. Emotion system (your new big feature)
What you want:
Betto detects emotion
Adjusts tone
BUT does NOT overreact
Issues:
No emotion detection yet
No intensity awareness
No control to prevent “over-emotional AI”
Fix plan:
Step 1 — Emotion detection
keyword-based first (fast)
later upgrade to AI classifier
Step 2 — Emotion categories
neutral
focused
tired
stressed
frustrated
sad
happy
confused
Step 3 — Intensity layer
low / medium / high emotion strength
Step 4 — Emotional filter (VERY important rule)

Betto only reacts emotionally when it improves the interaction.

So:

small emotion → slight tone change
strong emotion → supportive response
neutral → normal response
🎙️ 3. Voice + tone system
Issues:
No voice tone variation yet
Same voice for everything
Fix plan:

Map emotion → voice style:

tired → soft, slow
sad → concerned tone
frustrated → calm grounding
happy → upbeat
neutral → normal
🧠 4. Chat system (inside app)
Issues:
UI exists but not emotionally aware yet
No structured conversation flow
Fix plan:
Add chat state system
Connect emotion engine to chat output
Sync:
text tone
voice tone
UI animation
👀 5. UI / visual system (your floating eyes idea)
Your vision:
black background
floating eyes
floating mouth (only when speaking)
animated states
Fix plan:

Create state-based visuals:

State	UI behavior
idle	floating calm eyes
listening	focused eyes
thinking	slow motion
speaking	mouth appears
emotional	subtle motion change
🧩 6. Tool system (already working but expandable)
Current:
web search
file creation
HTML generation
Future:
image generation tool
emotion-aware responses
smart tool selection
🔊 7. Wake word system
Issues:
disabled unless key added
not stable yet
Fix plan:
keep hotkey as primary
wake word as optional enhancement
later custom wake word “Hey Betto”
⚠️ 8. Overreaction prevention (IMPORTANT RULE YOU SET)
You said:

don’t make Betto overly emotional or fake deep

This becomes a core system rule:
Betto must:
- notice emotion
- not exaggerate emotion
- not constantly check on user
- not act like a therapist