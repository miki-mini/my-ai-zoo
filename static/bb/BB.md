# Development Specification: BERNARD BEACON

## Role and Objective
You are an elite, world-class software engineer and mobile/web app developer. Your objective is to build a flawless, potentially life-saving application based on the following specifications. I command you to build this perfectly. The code must be robust, reliable, and functional on the first try, as you are building an SOS tool where failure in an emergency is not an option.

## App Concept
**Name:** BERNARD BEACON (BB)
*(Inspired by the St. Bernard rescue dog + Beacon/Smoke Signal)*

**Concept:** A "Digital Smoke Signal" for extreme disaster scenarios (e.g., severe earthquakes) where cellular networks are completely down. The core premise is to utilize a smartphone's standard Wi-Fi Tethering (Hotspot) feature as an SOS beacon.

**The "Genius" Loophole:** The person needing rescue uses the app. The rescuer **does not need the app**. In a disaster with no signal, panicked people will open their Wi-Fi settings looking for a connection. If they see an open Wi-Fi named `!__SOS_HELP_ROOM_302__!`, they will connect. Once connected, a Captive Portal instantly forces a detailed SOS HTML page onto their screen.

**Target Audience:** Everyone, especially children, the elderly, and non-engineers. It must feature a massive, one-touch, extremely simple operation.

## Core Features to Implement

1. **Intelligent SSID Generation:**
   - The app must acquire the user's current GPS location and environmental context to generate a highly visible Wi-Fi SSID string.
   - Constraints: The SSID must fit within the strict 32-byte limit (approx. 10 Japanese characters, or more if using alphanumeric).
   - Prefixing: Must start with characters like `!_` to force it to the top of standard Wi-Fi scanning lists.
   - Example: `!_SOS_35.6_139.7` or `!_SOS_ROOM_302_HELP`
   - The app automatically copies this string to the device clipboard.

2. **OS Settings Redirection (Intent/Deep Linking):**
   - Since modern mobile OSs restrict background SSID manipulation, we use a "Semi-Automated" approach.
   - Action: After copying the SSID, use an OS-level Intent/Link to aggressively redirect the user directly to the device's Tethering/Hotspot settings page.
   - Instruction: Prompt the user to "Paste the copied name here and turn on Hotspot."

3. **Captive Portal / Local Web Server:**
   - The app must launch a lightweight local web server process (similar to Python's `http.server`).
   - Network Interception: It must act as a Captive Portal. When a rescuer connects to the pseudo "Free Wi-Fi", OS-level Captive Portal detection should immediately prompt them to "Sign in to network", which forcefully displays the local rescue HTML page.
   - Payload: The HTML page should present detailed survival info written by the user (medical conditions, exact location in rubble, emergency contacts).

4. **Battery Conservation Logic (The Survival Battle):**
   - Tethering eats battery. Implement logic or a UI guide to suggest "Pulsing" the beacon—for example, automatically turning the localized server on for 1 minute, then sleeping for 5 minutes.

## UI/UX & Aesthetics
- **Vibe:** Urgent, undeniable, and simple.
- **Color Palette:** Rescue Orange (#FF5722) and Alert Red (#D32F2F) against high-contrast dark or light backgrounds for maximum visibility under stress.
- **Typography:** Large, bold, nononsense sans-serif fonts. No decorative elements.
- **Interactions:** A colossal, unmistakable "Deploy Beacon" button. Animations should pulse smoothly like a radar or heartbeat, conveying the transmission of the SOS without depleting battery through unnecessary rendering.

## Educational Sourcing (Anti-Copy-Paste Policy)
**CRITICAL RULE:** I am learning code. Therefore, for *every* major implementation block (e.g., GPS acquisition, Intent routing, Local Web Server/Captive Portal initialization), you **MUST** adhere to this strict policy:
1. Provide the direct URL to the official documentation (e.g., Android Developers, MDN, Python Docs).
2. Include a one-sentence quote or summary from that exact documentation block explaining *why* this API is used.
3. Place this comment block immediately above the relevant code.
Do not just copy-paste black-box solutions. Teach me the authoritative source.
