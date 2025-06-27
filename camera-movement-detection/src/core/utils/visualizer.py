import cv2

def annotate_frame(frame, text, position=(10, 30), font_scale=1, color=(0, 0, 255), thickness=2):
    """
    Annotates a frame with text at a specified position.

    This function adds text to the given frame using OpenCV's `putText` method, allowing customization
    of the text's position, font size, color, and thickness.

    Args:
        frame (numpy.ndarray): The frame (image) to annotate.
        text (str): The text to display on the frame.
        position (tuple): The (x, y) position where the text should be placed (default is (10, 30)).
        font_scale (float): The scale of the font (default is 1).
        color (tuple): The color of the text in BGR format (default is red `(0, 0, 255)`).
        thickness (int): The thickness of the text (default is 2).

    Returns:
        numpy.ndarray: The annotated frame with the added text.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    annotated = frame.copy()
    cv2.putText(annotated, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    return annotated
