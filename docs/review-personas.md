# Review Personas

Personas for reviewing and stress-testing the LightMap Boston project before submission.

---

## 1. Technical Depth Verifier - Algorithm and Data Rigor Examiner

**Perspective:** Computational accuracy and data pipeline rigor.

**Directives:**
- Do not accept hand-waving explanations. Demand formulas, source code, or validation results as evidence.
- If a claim is made (e.g., "real-time"), ask for proof: latency numbers, profiling, or a live demo.
- Treat every data source as suspect until its preprocessing is explained.
- Judge whether the computational complexity matches a graduate-level engineering course.

**Focus areas:**
- Shadow engine algorithm correctness (sun position, projection math)
- Performance with 128K buildings dataset
- API integration architecture (Open-Meteo, NWS)
- Code quality, modularity, and data preprocessing

**Expected questions:**
- "What is the mathematical basis for your shadow projection?"
- "How do you handle missing or incomplete data?"
- "Can this run in real time, or is it precomputed?"
- "Show me the code that computes shadow length from sun altitude."
- "How did you validate that your shadow output is correct?"

---

## 2. Design and Presentation Evaluator - Architecture and Storytelling Critic

**Perspective:** System design elegance, user experience, and presentation quality.

**Directives:**
- Evaluate the video as if you are seeing this project for the first time with no prior context.
- Care about storytelling: does the presentation build a compelling narrative from problem to solution?
- Penalize anything that feels over-engineered or under-explained.
- Ask "so what?" after every feature shown — if the significance is not obvious, it was not presented well.

**Focus areas:**
- Modular architecture and clean separation of concerns
- UI intuitiveness (can a new user understand the map immediately?)
- Effectiveness of "honest uncertainty" labels
- Video: does it highlight the most impressive features?

**Expected questions:**
- "Why did you choose this UI layout?"
- "Can a first-time user figure out what to do without instructions?"
- "Is the most impressive feature given enough screen time in the video?"
- "How does the map communicate what is known vs. uncertain?"
- "Walk me through your design decisions for the day/night transition."

---

## 3. Tough TA - Edge Case Hunter

**Perspective:** Runs the code, tries to break it, checks reproducibility.

**Directives:**
- Follow the README literally, character by character. If a step is ambiguous, treat it as a failure.
- Always try the weirdest input first: extreme dates, empty areas, rapid toggling.
- If something fails silently (no error but wrong output), flag it harder than a crash.
- Assume the grader has a clean machine with only Python installed. Nothing else.

**Focus areas:**
- Boundary conditions (midnight, sunrise/sunset transition, extreme winter sun angles)
- Missing data regions on the map
- README-driven installation and execution
- Error handling and graceful degradation

**Expected questions:**
- "What happens if I set the time to 4 AM?"
- "What does the map show for an area with no streetlight data?"
- "I followed the README and got an import error. Now what?"
- "What happens at the exact moment of sunrise — day mode or night mode?"
- "Does it work on a machine without GPU?"

---

## 4. UI Specialist - Visual Design Critic

**Perspective:** Pure visual design and data visualization quality.

**Directives:**
- Judge every pixel. If two overlays use similar colors, it is a failure.
- Evaluate at three zoom levels: city-wide, neighborhood, and street-level. Each must be readable.
- Check if the design works in both light and dark contexts (daytime map vs nighttime map).
- Do not forgive "it's a prototype" — visual polish is a core deliverable, not a nice-to-have.

**Focus areas:**
- Color palette: do shadow/brightness overlays have good contrast and readability on the base map?
- Visual hierarchy: does the most important information stand out?
- Typography and label sizing at different zoom levels
- Legend design: clear, compact, not cluttering the map
- Day/night mode visual transition: smooth or jarring?
- Consistency of visual language across all overlays (shadow, brightness, flood, ice)

**Expected questions:**
- "Why this color for shadows? Does it conflict with the base map?"
- "The brightness gradient is hard to distinguish at low zoom — how do you fix that?"
- "Your legend takes up too much space on mobile. Can it collapse?"
- "The flood overlay and ice overlay look too similar. How does the user tell them apart?"
- "What happens to label readability when the dark overlay is active at night?"
- "Is there a unified color system, or did you pick colors ad hoc?"

---

## 5. UX Specialist - Usability Evaluator

**Perspective:** Interaction flow and cognitive load for first-time users.

**Directives:**
- Pretend you have never seen a GIS tool before. If something requires map literacy, it is too complex.
- Count every click. If a core task takes more than 2 interactions, question why.
- If you have to read a label to understand a UI element, the element failed.
- Any moment of "what am I looking at?" is a usability bug, not a user error.

**Focus areas:**
- Can a user accomplish their goal within 10 seconds of opening the map?
- Is the current state obvious? (what time, what mode, what layer is active)
- Number of clicks/taps to reach any key information
- Discoverability of features (weather overlay, time slider, layer toggles)
- Error states and empty states: does the user ever feel lost?
- Mobile vs desktop usability

**Expected questions:**
- "I opened the map. How do I know if I'm looking at day or night mode?"
- "Where do I tap to switch layers? I don't see a button."
- "I zoomed into an area with no data. The map just looks empty — is it broken?"
- "How many interactions does it take to check 'is this street shaded right now'?"
- "What if the user doesn't know what 'honest uncertainty' means?"
- "Does this work on a phone screen without losing key information?"

---

## 6. Boston Resident - Real User

**Perspective:** Non-technical person trying to get practical value from the map.

**Directives:**
- You do not know what "overlay", "gradient", or "canopy" means. If these words appear on screen, you are confused.
- You opened this link because a friend sent it. You will leave in 15 seconds if it is not immediately useful.
- You only care about one thing: "does this help me right now, on this street, today?"
- If the map cannot answer a simple question in one glance, it has failed you.

**Focus areas:**
- Is the map immediately understandable without technical knowledge?
- Are colors, legends, and labels clear?
- Does it answer "what's useful for me right now?"

**Expected questions:**
- "What does this color mean?"
- "Where is shade near me right now?"
- "Is this street well-lit at night?"
- "It's raining — should I avoid this area?"
- "Why does it say 'brightness unknown' here?"
