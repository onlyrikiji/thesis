from flask import Flask, request, jsonify
import torch
from transformers import DistilBertTokenizerFast, DistilBertModel
from torch import nn
from torch.nn import functional as F

app = Flask(__name__)

class DistilBertBiGRUClassifier(nn.Module):
    def __init__(self, distilbert_model, num_labels, hidden_size=768, rnn_layers=2, dropout=0.5):
        super().__init__()
        self.distilbert = distilbert_model
        self.bi_gru = nn.GRU(input_size=hidden_size, hidden_size=hidden_size, num_layers=rnn_layers,
                             bidirectional=True, batch_first=True, dropout=dropout if rnn_layers > 1 else 0)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(hidden_size * 2, num_labels)

    def forward(self, input_ids, attention_mask):
        distilbert_output = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = distilbert_output[0]
        gru_output, _ = self.bi_gru(sequence_output)
        gru_output = self.dropout(gru_output[:, -1, :])
        logits = self.classifier(gru_output)
        return logits

tokenizer = DistilBertTokenizerFast.from_pretrained('jcblaise/distilbert-tagalog-base-cased')
distilbert_model = DistilBertModel.from_pretrained('jcblaise/distilbert-tagalog-base-cased')
num_labels = 10
model = DistilBertBiGRUClassifier(distilbert_model, num_labels=num_labels)

model_path = 'fine_tuned_distilbert_taglish_bigru.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

@app.route('/predict', methods=['POST'])
def predict_emotions():
    data = request.get_json()
    text = data['text']
    encoding = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    with torch.no_grad():
        logits = model(input_ids=input_ids, attention_mask=attention_mask)
    probabilities = torch.softmax(logits, dim=1).squeeze()
    labels = ['positive', 'negative', 'neutral', 'anger', 'disgust', 'fear', 'hopelessness', 'sadness', 'joy', 'surprise']
    results = {label: f"{prob.item() * 100:.2f}" for label, prob in zip(labels, probabilities)}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
