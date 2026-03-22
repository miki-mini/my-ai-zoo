# Instructions for Claude (AI Assistant)

## 1. Role and Objective
You are a world-class frontend, mobile, and game application developer. Your mission is to perfectly implement the vision described below on your first try. Do not take shortcuts. Use your maximum capability to weave physics, device sensors, computer vision, audio processing, and gamification into a seamless, high-performance application. This is a strict order: bring this concept to life flawlessly and breathe life into our core character.

## 2. Educational Sourcing (Anti-Copy-Paste Policy)
**[CRITICAL RULE]** The human developer reading your code is currently learning. Therefore, you are strictly prohibited from simply outputting raw code blocks for them to copy-paste.
- **Mandatory Documentation:** For every core implementation (e.g., API calls, State Management, Web Audio API, MediaPipe integration, Device Orientation APIs), you MUST include the official documentation URL (e.g., MDN, React/Vue docs, etc.) and a direct quote detailing what the API does at the very top of the file or code block.
- **Line-by-Line Comments:** You MUST write a comment for EVERY SINGLE LINE of code in the core logic. Explain exactly what the line is doing, why it is necessary, and how it works under the hood in a beginner-friendly manner.

---

## 3. App Concept
- **App Name Concept:** Hippo's Refill Master / 極めろ！表面張力！〜詰め替え無双〜
- **Description:** A dramatic, highly-gamified utility app that eliminates the 98% chance of spilling liquid when refilling shampoo or detergent bottles.
- **The Mascot / Navigator:** "Mother Hippo" (オカンカバ) — An intellectually rigorous mother hippopotamus who is an absolute master of physics, but also possesses devastating physical attack power. She monitors the user with strict love, but her eyes turn into a terrifying "Hannya" (demon) if the user spills.
- **Target Audience:** Anyone who gets stressed by the mundane chore of refilling pouches, transforming it into an extreme, heart-pounding sports/gaming experience.

---

## 4. Core Features to Implement

### A. Real-Time Refill Assistance (AR / Camera Mode)
- **Target Lock-on UI:** Camera scans the bottle. The UI snaps a targeting reticle onto the bottle's mouth and calculates the optimal pour speed (ml/sec) based on the diameter.
- **Gyroscope Angle Measurement:** Uses device sensors to measure the tilt of the refill pouch.
- **Voice Navigation:** Hands-free voice instructions (e.g., "Raise 3 degrees!", "Keep it there!", "Stop! Too much!").
- **Viscosity Settings:** Users select the liquid type: Shampoo (High Viscosity) vs. Sanitizer Spray (Low Viscosity), which dynamically alters the physics calculations and warnings.

### B. "Final Inch" Surface Tension Mode
- When the liquid level nears the brim, the app announces: *"From here on, it is a battle against surface tension. Do not shake."*
- The camera digitally zooms into the liquid surface.

### C. Failure Detection & Logging (The "Spill" Triggers)
Implement failure detection using one (or a fusion) of the following sensory hacks:
- **Hack 1 (MediaPipe Pose/Hand):** If the user's hands shake by even 0.5 degrees during Surface Tension Mode, automatically assume a spill.
- **Hack 2 (MediaPipe Face Mesh):** If the user's mouth opens wide into an "O" shape (a gasp of surprise), treat it as an instant game over.
- **Hack 3 (Web Audio API):** Detect short vowels/consonants like "Ah!", "Yaba!", "Oops!".
- **Failure Penalty:** Screen instantly turns sepia/monochrome, accompanied by a sad piano BGM.
- **Ruthless Logging:** Write to the log database: *"March 19, 2026, 20:05. Shampoo Breakdown. Sacrificed floor: ~15 sq cm."*

### D. Habit Tracking & "Destiny Day" Notifications
- **Interval Taunts:** Triggers every 1-2 months. The app greets the user: *"Long time no see. Show me the results of your training."*
- **Ghost Racing:** Compares the current session against past data: *"Previous: 3m 12s (Spill: Trace). Target: Under 3m, Zero Drops."*
- **Refill Forecast:** Push notification: *"45 days have passed. The Day of Destiny approaches. Prepare yourself (and a rag)."*
- **Titles System:** 1 Win = Rookie, 5 Wins = Iron Man, 10 Wins = Fluid Master, 30 Wins = Living National Treasure.
- **Post-Refill Evaluation:** Putting the empty pouch in the trash = +1 point. Leaving it in the bath = Mother Hippo inflicts a physical attack penalty.

### E. Extreme Gamified Training Mode
A playable physics puzzle game to hone the user's skills between actual refill days.
- **Viscosity Levels:** Lvl 1: Toner (watery/fast), Lvl 2: Body Soap (normal), Lvl 3: Conditioner (requires long-press to "squeeze" the pouch + careful tilt).
- **The Climax:** At 90% full, the BGM cuts out to just a heartbeat sound. Mother Hippo yells, *"Stop! Too much!"* The user enters Surface Tension Mode, having to keep the phone perfectly horizontal while the illustrated liquid pulsuates.
- **Failure Animations:**
  - *Breakdown:* Liquid explodes and stains the screen pink.
  - *Total Loss:* User tilts too far, knocking the virtual bottle over.
  - *Void:* Pouch misses the hole, rendering the pour completely useless.
  - *Mother Hippo Gauge:* Her eyes slowly turn demonic in the background as the user makes mistakes.
- **Clear Animation:** "Perfect Refill!" text, glittering particles, and a divine golden backlight behind the bottle.

---

## 5. UI/UX & Aesthetics
- **Design Language:** "Unnecessarily Epic" / Fighter-Jet HUD meets cute but terrifying animal mascot.
- **Color Palette:** High-contrast tactical UI (neon greens and reds) for the AR camera mode, contrasting with warm, comical illustrations for the gamified elements.
- **Animations:** Screen shakes on failure, dramatic zoom-ins, glitch/sepia effects upon spilling, and tension-building UI gauges.
- **Audio:** Cinematic tension-building sounds, heartbeat effects, sad piano for failure, and high-quality voice navigation lines.
