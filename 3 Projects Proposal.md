# Team Project Proposal

**Team:** Glyz-Team  
**Members:** Furui Guan, Yichen Li, Yilun Yang, Aozuo Zheng

## Ranked Project Ideas

---

### 1) Attack of Monsters — 2048 Defense (preferred)
**Tagline:** The weblink will open up a portal for monsters to attack New Haven. Defend the world by playing three rounds of 2048 in a local co-op session (up to 3 players on one keyboard).  
**Major user journeys**
- **Casual player:** Open page → animation shows monster approaching → play 3 rounds of 2048 → defeat monster → name the run to appear on the leaderboard.  
- **Local coop:** Up to 3 players use one keyboard (WASD | arrow keys | BNH keys) to contribute damage across rounds.  
- **Return player:** Optionally create a short unique ID after first attempt to retrieve past attempts.
- **Admin:** Track Usage - Games Played, remove invalid attempt to maintain leaderboard, etc... 
**Core MVP features**
1. Surprise emergency page with animation for opening up a portal to monster world.  
2. 2048 gameplay with visual bullet effects for merges. 2048 triggers an ultimate attack. 
3. Local co-op support for up to 3 players on one keyboard (no online multiplayer).  
4. Post-run naming and persistent leaderboard; optional lightweight account via unique ID to view past attempts.  
**Backend note:** Simple backend to store leaderboard entries and optional user IDs (Postgres).

---

### 2) Campus “Tree-Hole” Forum
**Tagline:** Anonymous / semi-anonymous campus forum encouraging honest student posts about professors, courses, campus life, and events.  
**Major user journeys**
- **Poster:** Quick Post → choose anonymous or identity → select tags → post to board.  
- **Reader:** Browse trending posts, filter by tag/board, view a poster’s public history if available.  
- **Admin:** Moderate reports, remove inappropriate posts and manage tag rules.  
**Core MVP features**
1. Quick Post UI with anonymous toggle and rule-based tag suggestions.  
2. Three boards: Course & Prof Eval; Life (second-hand / lost & found); Trending feed.  
3. Tag filtering and saveable filters; server-side trending algorithm.  
4. Likes/comments and admin moderation.  
**Backend note:** Support user accounts, profile picture, and a user’s history of past posts (Postgres).

---

### 3) New Haven Crime & Safety Map 
**Tagline:** Interactive map showing 10 years of New Haven crime history by category, plus campus emergency pole locations and a community “how sketchy I feel” heatmap.  
**Major user journeys**
- **Visitor:** Open map → view clustered crime points + blue-light poles → filter by category/time → click a point to read a short summary + source link.  
- **Logged user:** Save phone & emergency contact → submit a “how sketchy I feel” report at current location → contribute to community heatmap.  
- **Admin:** moderate submissions and track user behavior   
**Core MVP features**
1. Map UI plotting preprocessed historical CSV as clustered points with a time slider.  
2. Four high-level categories: Gang / Traffic (non-dangerous) / Robbery & Assault / Homicide.  
3. Blue-light / emergency pole layer and mobile one-tap call (tel:911 or campus security).  
4. User "sketchy" reports aggregated into a moderated heatmap.  
**Backend note:** Support user accounts with phone & emergency contact; store sketchy reports and aggregate into heatmap (Postgres).

---

**Preferred project:** #1 Monitor Siege — 2048 Defense
