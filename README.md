# Hermes
Hermes is a random Discord bot I've been working on that implements many different APIs to create the funniest shitpost bot. 

## TokenLoader
TokenLoader is a utility module for loading `.token` files.

### `tokenloader.load(filename)`
Loads a token that is stored in a `.token` file.

## Commands

### /finishthis | `sentence` | `maxwords (optional)`
Uses the *Bloom* LLM to finish your sentence. `maxwords` specifies the maximum amount of words to generate.

### /askai | `question`
Ask Facebook's BlenderBot LLM a question. It will remember your conversation.

### /randomgif
Sends a random GIF found on Giphy.

### /randommeme
Sends a random meme scraped from Reddit.

### /randominsult | `persontoinsult (optional)`
Finds a random insult and insults the mentioned person.