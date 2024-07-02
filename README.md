# Comics Generator

This program uses Generative AI to create an entire comic strip from a short scenario.

## How it works

1. **User Input**: 
    - Enter the number of characters (2 or 3) along with their descriptions.
    - Provide a scenario that involves the specified characters.
    - Select the desired comic style from various options (Superhero Style, Manga, Cartoon/Cartoony Style, European/Franco-Belgian Style, Noir/Pulp Style, Indie/Alternative Style, Western Style, Chibi Style, Realistic Style, Webtoon Style).

2. **Panel Generation**: 
    - A Large Language Model (LLM, OpenAI API) is used to split the scenario into 6 panels, each with its own description and associated text.

3. **Image Generation**: 
    - For each panel, an image is generated using Stable Diffusion (Stability API).
    - The panel text is added to the generated image.

4. **Final Strip Creation**: 
    - The 6 generated images with their texts are merged into a final comic strip.
    - The final comic strip can be viewed and downloaded directly from the application.
