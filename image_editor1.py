import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io

# Helper function to display the image
def display_image(img):
    st.image(img, use_column_width=True)

# Function to display the star rating system
def star_rating():
    if 'rating' not in st.session_state:
        st.session_state.rating = 0

    def set_rating(rating):
        st.session_state.rating = rating

    st.write("### Rate Us:")
    stars = ""
    for i in range(1, 6):
        if i <= st.session_state.rating:
            stars += "★"  # Filled star
        else:
            stars += "☆"  # Empty star
    st.write(stars)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        if col.button(f"{i + 1} ★"):
            set_rating(i + 1)

    st.write(f"Your rating: {st.session_state.rating} star(s)")

def main():
    st.title("AI-Based Image Editor")

    st.write("Welcome to our AI-based Image Editing Tool! Let’s transform your images with ease!")

    # Load Image
    uploaded_file = st.file_uploader("Load an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        original_image = Image.open(uploaded_file)
        edited_image = original_image.copy()
        display_image(edited_image)

        # Brightness control
        brightness = st.slider("Adjust Brightness", 0.1, 2.0, 1.0, 0.1)

        # Contrast control
        contrast = st.slider("Adjust Contrast", 0.1, 2.0, 1.0, 0.1)

        # Blur control
        blur = st.slider("Adjust Blur", 0, 10, 0, 1)

        # Apply filters button
        if st.button("Apply Filters"):
            # Apply brightness
            enhancer = ImageEnhance.Brightness(edited_image)
            edited_image = enhancer.enhance(brightness)

            # Apply contrast
            enhancer = ImageEnhance.Contrast(edited_image)
            edited_image = enhancer.enhance(contrast)

            # Apply blur
            edited_image = edited_image.filter(ImageFilter.GaussianBlur(blur))
            display_image(edited_image)

        # Remove background button
        if st.button("Remove Background"):
            img_byte_arr = io.BytesIO()
            edited_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            img_no_bg = remove(img_byte_arr)
            edited_image = Image.open(io.BytesIO(img_no_bg))
            display_image(edited_image)

        # Crop Image
        if st.button("Crop to Square"):
            width, height = edited_image.size
            new_dimension = min(width, height)
            left = (width - new_dimension) / 2
            top = (height - new_dimension) / 2
            right = (width + new_dimension) / 2
            bottom = (height + new_dimension) / 2
            edited_image = edited_image.crop((left, top, right, bottom))
            display_image(edited_image)

        # Reset Image
        if st.button("Reset"):
            edited_image = original_image.copy()
            display_image(edited_image)

        # Save Image
        if st.button("Save Image"):
            img_byte_arr = io.BytesIO()
            edited_image.save(img_byte_arr, format='PNG')
            st.download_button(
                label="Download Image",
                data=img_byte_arr.getvalue(),
                file_name="edited_image.png",
                mime="image/png"
            )

        # Feedback Section with Star Rating
        star_rating()

        # Comment box for feedback
        comment = st.text_area("Leave your feedback here...")

        # Submit feedback button
        if st.button("Submit Feedback"):
            st.success(f"Thank you for your feedback!\nRating: {st.session_state.rating} stars\nComment: {comment}")

if __name__ == "__main__":
    main()
