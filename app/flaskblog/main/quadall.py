import sqlite3
import requests
import matplotlib.pyplot as plt
import re

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Define the regular expression pattern to match
pattern = r""  # You can adjust this pattern as needed

# Execute a SQL query to fetch data
cursor.execute("SELECT id, content FROM post  LIMIT 100")
rows = cursor.fetchall()

# Close the connection
conn.close()

# Loop through the fetched data
emotion_data_sets = []

for row in rows:
    post_id, post_content = row

    # Check if the content matches the pattern
    if re.search(pattern, post_content):
        # Call the API to analyze emotion
        api_url = 'http://127.0.0.1:5001/predict'
        data = {'text': post_content}  # Sending the post content as 'text'
        response = requests.post(api_url, json=data)
        emotion_data = response.json()

        # Structure the emotion data
        emotion_data_set = {
            "name": f"Post {post_id}",
            "data": emotion_data
        }
        emotion_data_sets.append(emotion_data_set)

# Print or further process the emotion data sets
for emotion_data_set in emotion_data_sets:
    print(emotion_data_set)


# Define quadrants
positive_intensity = ["joy", "surprise"]
negative_intensity = ["anger", "disgust", "fear", "hopelessness", "sadness"]
neutral_intensity = ["neutral"]

# Define colors for each emotion
emotion_colors = {
    "anger": "red",
    "disgust": "purple",
    "fear": "orange",
    "hopelessness": "brown",
    "joy": "green",
    "negative": "black",
    "neutral": "blue",
    "positive": "cyan",
    "sadness": "gray",
    "surprise": "pink"
}

# Create scatter plot for each data set
plt.figure(figsize=(8, 6))
for idx, data_set in enumerate(emotion_data_sets):
    for emotion, intensity in data_set["data"].items():
        label = None
        if emotion in positive_intensity:
            label = f"{emotion.capitalize()} (Positive)" if idx == 0 else None
            plt.scatter(intensity, 1, color=emotion_colors[emotion], label=label)
        elif emotion in negative_intensity:
            label = f"{emotion.capitalize()} (Negative)" if idx == 0 else None
            plt.scatter(intensity, -1, color=emotion_colors[emotion], label=label)
        elif emotion in neutral_intensity:
            label = f"{emotion.capitalize()} (Neutral)" if idx == 0 else None
            plt.scatter(intensity, 0, color=emotion_colors[emotion], label=label)

# Add labels
plt.xlabel("Intensity")
plt.ylabel("Sentiment")
plt.title("Emotion Quadrant Chart")
plt.axhline(0, color="gray", linestyle="--")
plt.axvline(0, color="gray", linestyle="--")
plt.legend()

# Show the plot
plt.show()