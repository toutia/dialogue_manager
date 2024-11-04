from typing import Dict, Text, Any, List
import tritonclient.http as httpclient
import numpy as np
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from transformers import DistilBertTokenizer
import requests
@DefaultV1Recipe.register("TritonLanguageModelFeaturizer", is_trainable=False)

class TritonLanguageModelFeaturizer(GraphComponent):
    def __init__(self, config: Dict[Text, Any], model_name: Text, triton_url: Text, tokenizer: DistilBertTokenizer):
        self.config = config
        self.model_name = model_name
        self.triton_client = httpclient.InferenceServerClient(url=triton_url)
        self.tokenizer = tokenizer

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        model_name = config.get("model_name", "distilbert")
        triton_url = config.get("triton_url", "localhost:8000")
        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        return cls(config=config, model_name=model_name, triton_url=triton_url, tokenizer=tokenizer)


        # Function to get embeddings from Triton server
    def get_embedding_from_triton(self,text, max_length=128):
        # Tokenize the text input for DistilBERT
        print(text)
        inputs = self.tokenizer(text, return_tensors='np', padding='max_length', truncation=True,max_length=max_length)

        # Create inference request inputs for Triton
        input_ids = httpclient.InferInput("input_ids", inputs['input_ids'].shape, "INT32")
        attention_mask = httpclient.InferInput("attention_mask", inputs['attention_mask'].shape, "INT32")

        # Set the input data
        input_ids.set_data_from_numpy(inputs['input_ids'].astype(np.int32))
        attention_mask.set_data_from_numpy(inputs['attention_mask'].astype(np.int32))

        # Make inference request
        results = self.client.infer(self.model_name, [input_ids, attention_mask])
        print(results)

        # Extract the embedding from the output (assuming it's the CLS token embedding)
        embeddings = results.as_numpy('output')
        return embeddings.squeeze()
    def process(self, message: Message, **kwargs: Any) -> None:
        """Extract embeddings from Triton and store in message."""
        text = message.get("text")
        embeddings = self.get_embedding_from_triton(text)
        message.set("text_features", embeddings)