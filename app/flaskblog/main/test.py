import matplotlib.pyplot as plt

# Emotion data
emotions = {
    "anger": 1.08,
    "disgust": 1.04,
    "fear": 0.84,
    "hopelessness": 1.73,
    "joy": 0.18,
    "negative": 83.21,
    "neutral": 0.19,
    "positive": 0.19,
    "sadness": 11.38,
    "surprise": 0.15,
}

# Define quadrants
positive_intensity = ["positive","joy", "surprise"]
negative_intensity = ["negative","anger", "disgust", "fear", "hopelessness", "sadness"]
neutral_intensity = ["neutral"]

# Define colors for each emotion
emotion_colors = {
    "anger": "cyan",
    "disgust": "purple",
    "fear": "orange",
    "hopelessness": "black",
    "joy": "yellow",
    "negative": "red",
    "neutral": "blue",
    "positive": "green",
    "sadness": "gray",
    "surprise": "pink"
}

# Create scatter plot
plt.figure(figsize=(8, 6))
for emotion, intensity in emotions.items():
    if emotion in positive_intensity:
        plt.scatter(intensity, 1, color=emotion_colors[emotion], label=emotion.capitalize() + " (Positive)")
    elif emotion in negative_intensity:
        plt.scatter(intensity, -1, color=emotion_colors[emotion], label=emotion.capitalize() + " (Negative)")
    elif emotion in neutral_intensity:
        plt.scatter(intensity, 0, color=emotion_colors[emotion], label=emotion.capitalize() + " (Neutral)")

# Add labels
plt.xlabel("Intensity")
plt.ylabel("Sentiment")
plt.title("Emotion Quadrant Chart")
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")
plt.legend()

# Show the plot
plt.show()
