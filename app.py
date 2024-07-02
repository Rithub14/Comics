import json
import streamlit as st
from io import BytesIO
# from PIL import Image

from generate_panels import generate_panels
from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

def main():
    st.title("Comic Strip Generator")
    st.subheader("Please enter the details on the left to create a comic strip.")
    st.sidebar.header("Enter Scenario and Style")
    
    # Input for number of characters
    num_characters = st.sidebar.selectbox("Number of Characters", [2, 3])
    
    # Inputs for character descriptions
    characters = []
    for i in range(num_characters):
        character_name = st.sidebar.text_input(f"Character {i+1} Name", f"Character {i+1}")
        character_description = st.sidebar.text_area(f"Character {i+1} Description", f"Description of Character {i+1}")
        characters.append(f"{character_name} is {character_description}")

    # Combine character descriptions into the scenario
    scenario = st.sidebar.text_area("Scenario", "Describe the scenario here.")
    full_scenario = "Characters: " + ". ".join(characters) + ". " + scenario

    Style = st.sidebar.selectbox("Style", ["Superhero Style", "Manga", "Cartoon/Cartoony Style", "European/Franco-Belgian Style", "Noir/Pulp Style", "Indie/Alternative Style", "Western Style", "Chibi Style", "Realistic Style", "Webtoon Style"])

    if st.sidebar.button("Generate Comic Strip"):
        generate_comic_strip(full_scenario, Style)

def generate_comic_strip(Scenario, Style):
    st.write(f"Generating panels with Style: '{Style}.'\n")

    panels = generate_panels(Scenario)

    with open('output/panels.json', 'w') as outfile:
        json.dump(panels, outfile)

    panel_images = []

    progress_bar = st.progress(0)
    total_panels = len(panels)

    for i, panel in enumerate(panels):
        panel_prompt = panel["description"] + ", cartoon box, " + Style
        try:
            panel_image = text_to_image(panel_prompt)
        except Exception as e:
            st.error(f"Error generating image for panel {panel['number']}: {e}")
            st.stop()

        panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
        panel_images.append(panel_image_with_text)

        progress = (i + 1) / total_panels
        progress_bar.progress(progress)

        panel_image_with_text.save(f"output/panel-{panel['number']}.png")

    final_strip = create_strip(panel_images)
    final_strip.save("output/strip.png")
    st.image("output/strip.png", caption="Final Comic Strip")

    buf = BytesIO()
    final_strip.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Comic Strip",
        data=byte_im,
        file_name="comic_strip.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
