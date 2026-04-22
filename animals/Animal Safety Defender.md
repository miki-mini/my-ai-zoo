# Role and Objective
You are an elite AI developer and coding mentor. I am entrusting you with the implementation of a perfect, flawless web-based game. Your mission is to write the ultimate code that I can learn from. Do not give me mediocre code; I demand excellence. Read the requirements carefully, implement them with absolute precision, and act as my strict but brilliant teacher!

# App Concept
**Name:** Animal Safety Defender
**Inspiration:** A respectful homage to the legendary "Space Invaders" by Tomohiro Nishikado.
**Worldview:** A retro-style arcade game where adorable animals defend themselves against their real-world dietary enemies (toxic foods and dangers).
**Target Audience:** Gamers and pet owners who want to learn about animal safety while enjoying a challenging, nostalgic arcade experience.
**Aesthetics & Audio:** 8-bit / 16-bit pixel art style (dot pictures). The game must feature completely original synth/chiptune sound effects and music to avoid any copyright issues.

# Core Features to Implement

## General Game Mechanics
- **Player Movement:** Player controls an animal at the bottom of the screen, moving strictly left and right.
- **Shooting System:** Player shoots projectiles upwards to destroy descending "Invaders" (toxic foods).
- **Collision Detection:** If an Invader reaches the bottom or touches the Player, adverse effects occur.
- **Progression:** The game consists of 3 distinct, progressively harder stages.

## Level 1: The Dog 🐶
- **Player Avatar:** A cute dog (e.g., Shiba Inu or Golden Retriever).
- **Invaders (Toxic Foods):** Chocolate 🍫 (Poisoning), Onion 🧅 (Blood disease), Grapes 🍇 (Kidney disease).
- **Special Entity (UFO equivalent):** "Bone-in Meat" (🍖) occasionally flying across the top of the screen.
  - **Reward:** Shooting it down grants a temporary "3x Attack Power" boost.
- **Penalty:** If hit by food, the dog cries "My tummy hurts~ 😢", losing 1 Life.

## Level 2: The Cat 🐈
- **Player Avatar:** A cute cat.
- **Regular Invaders:** Lily flowers 💐 (Highly toxic), Grapes 🍇, Chocolate 🍫, Raw Squid 🦑 (Causes paralysis/weakness).
- **Trap Invaders (Deceptive):** Milk 🥛 (Lactose intolerance -> Diarrhea), Excessive Tuna 🐟 (Mercury poisoning / Yellow fat disease).
- **Special Entity:** "Silvervine / Matatabi".
  - **Reward:** Catching it (or shooting it) grants a temporary "Invincibility Barrier".
  - **Trivia Feature:** Upon gaining it, display a UI message: *"Did you know? Matatabi isn't just for intoxication! A 2021 study revealed cats rub it to act as a natural mosquito repellent! A true survival strategy!"*

## Level MAX: The Boss Rabbit 🐇
- **Player Avatar:** The "Boss" Rabbit.
- **Difficulty:** Bullet Hell (Danmaku) / Extreme Difficulty. Enemies spawn relentlessly in high volumes.
- **Invaders:** Bread/Cookies/Sweets (Destroys gut bacteria rapidly), Potato Skins/Sprouts (Contains deadly solanine), Onion/Garlic (Destroys red blood cells), Chocolate, Spinach, Nuts.
- **Special Entity:** "Premium Timothy Hay".
  - **Reward:** Dramatically increases the Rabbit's movement speed to dodge the bullet hell.

## The "Death Game" Life System
- **Dog & Cat Levels (Salvation Mechanic):** If hit, there is a probability the animal will "throw up" the bad food, surviving the hit but losing 1 point of health as a penalty (allows for some mistakes).
- **Rabbit Level (No Salvation):** 0 forgiveness. If *even one* toxic food touches the rabbit, it triggers an instant System Shutdown (Game Over). It is a strict "One-mistake instant death" mechanic.

# UI/UX & Aesthetics
- **Visuals:** Pure retro arcade aesthetic. Use a dark background with vibrant elements.
- **Animations:** CRT monitor scanline effects, retro explosion particles when foods are destroyed.
- **Feedback:** Screen shake on taking damage, satisfying visual cues for power-ups (Matatabi barrier, 3x attack).
- **Typography:** Pixel/Arcade-style fonts (e.g., loaded via Google Fonts like 'Press Start 2P') for scores, trivia, and UI elements.

# 🚨 Educational Sourcing (Anti-Copy-Paste Policy) 🚨
**CRITICAL RULE - READ CAREFULLY:** I am actively learning how to code through this project. I strictly forbid you from just vomiting out undocumented code.
1. **Mandatory Citations:** For EVERY major implementation block (e.g., Canvas API rendering, `requestAnimationFrame` game loop, collision detection mathematics, State Management, Web Audio API), you MUST include a comment block at the top containing the **official documentation URL (e.g., MDN Web Docs)** and a summarizing quote explaining what the API does.
2. **No Blind Copy-Pasting:** Do not use generic, unexplained code snippets. Everything must be bespoke and purposefully written.
3. **Line-by-Line Comments:** You MUST provide extremely detailed, beginner-friendly comments for *almost every single line of logic*. Explain *why* the code is written that way, what state it mutates, and how it connects to the game logic. Treat this code as a comprehensive textbook for a beginner.
