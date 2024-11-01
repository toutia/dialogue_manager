from transformers import DistilBertTokenizer, DistilBertModel

# Load the DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# Save the model and tokenizer
model.save_pretrained('./models/distilbert')
tokenizer.save_pretrained('./models/distilbert')
