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

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR],
    is_trainable=False
)


class DistillBertNluComponent(GraphComponent):
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

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get("text")
            inputs = self._prepare_inputs(text)
            response = self.triton_client.infer(
                model_name=self.model_name, inputs=inputs
            )

            # Parse the response to get intent and entities
            intent, confidence = self._parse_intent(response)
            entities = self._parse_entities(response, text)

            # Add intent and entities to the message
            message.set("intent", {"name": intent, "confidence": confidence})
            message.set("entities", entities)
        return messages

    def _prepare_inputs(self, text: Text):
        # Tokenize the text
        tokenized_text = self.tokenizer(text, return_tensors="np", padding=True, truncation=True)
        input_ids = np.array(tokenized_text["input_ids"], dtype=np.int32)
        attention_mask = np.array(tokenized_text["attention_mask"], dtype=np.int32)

        # Wrap inputs in Triton format
        input_ids_input = httpclient.InferInput("input_ids", input_ids.shape, "INT32")
        attention_mask_input = httpclient.InferInput("attention_mask", attention_mask.shape, "INT32")

        input_ids_input.set_data_from_numpy(input_ids)
        attention_mask_input.set_data_from_numpy(attention_mask)
        
        return [input_ids_input, attention_mask_input]

    def _parse_intent(self, response: httpclient.InferResult):
        # Parse Triton's response for intent logits
        intent_logits = response.as_numpy("intent_logits")
        probabilities = np.exp(intent_logits) / np.sum(np.exp(intent_logits), axis=1, keepdims=True)
        intent_idx = np.argmax(probabilities, axis=1)[0]
        confidence = probabilities[0][intent_idx]

        # Map intent index to name
        intent_map = self.config.get("intent_map", {})
        intent = intent_map.get(intent_idx, "unknown")

        return intent, confidence

    def _parse_entities(self, response: httpclient.InferResult, text: Text):
        # Parse Triton's response for entity predictions
        entity_logits = response.as_numpy("entity_logits")
        entity_ids = np.argmax(entity_logits, axis=2)[0]  # Get most likely entity class per token

        tokens = self.tokenizer.tokenize(text)
        entities = []
        current_entity = None
        current_entity_tokens = []

        # Map entity IDs to labels; assume we have a mapping for entity labels
        entity_map = self.config.get("entity_map", {})

        for idx, token in enumerate(tokens):
            entity_id = entity_ids[idx]
            entity_label = entity_map.get(entity_id, "O")

            if entity_label.startswith("B-"):  # Start of a new entity
                if current_entity:
                    entities.append(current_entity)
                current_entity = {"entity": entity_label[2:], "value": token, "start": idx, "end": idx}
            elif entity_label.startswith("I-") and current_entity:  # Continuation of an entity
                current_entity["value"] += " " + token
                current_entity["end"] = idx
            else:
                if current_entity:
                    entities.append(current_entity)
                    current_entity = None

        # Append any remaining entity
        if current_entity:
            entities.append(current_entity)

        return entities
