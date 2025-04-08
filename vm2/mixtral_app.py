"""
This script is designed for VM2 and implements a Flask web application that provides a chat service using a combination of language models and sparse embeddings for text processing.

The main functionalities include:
1. Handling chat requests: Receives a user message, finds the most similar sentence from a pre-loaded vector database, generates a response using the Mixtral language model, and returns the generated response.
2. Handling feedback: Receives user feedback along with a rating and logs the received information.
3. Text processing: Uses the Mixtral language model for generating responses and the Splade model for embedding texts and finding similar sentences based on cosine similarity.

The script configures logging, initializes the Flask application, and sets up the required routes for handling chat and feedback requests.

Main Components:
- TextProcessor class: Initializes the language models, handles text embeddings, and finds similar sentences.
- Flask routes: Defines the '/chat' and '/feedback' endpoints to handle respective requests.
- Entry point: Runs the Flask application on host '0.0.0.0' and port 5000 if the script is executed directly.
"""

from flask import Flask, request, jsonify
from llama_cpp import Llama
from typing import Generator, Dict, Union, List
from sparsembed import model
from transformers import AutoModelForMaskedLM, AutoTokenizer
import sparsembed
import pandas as pd
import numpy as np
import json
import logging
import torch

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
"""
Initializes the Flask application.

Creates an instance of the Flask class for the web application. The __name__ argument is passed
to the Flask instance to help determine the root path of the application. This allows Flask to
locate resources such as templates and static files.
"""

# Load Mixtral LLM
class TextProcessor:
    def __init__(self):
        """
        Initializes the TextProcessor object and calls the method to initialize the Mixtral model.
        """
        self.llm = None
        self.initialize_mixtral()
        self.model = self.initialize_splade_model()
        self.loaded_tensors, self.loaded_sentences = self.load_vector_data("vector_db.json")

    def initialize_mixtral(self):
        """
        Initializes the Mixtral language model if it is not already initialized.
        """
        if self.llm is None:
            self.llm = Llama(
                model_path="/data/vm2-mvp/models/mixtral-8x7b-v0.1.Q5_K_M.gguf",  # Correct model path
                n_ctx=2048,
                # The max sequence length to use - note that longer sequence lengths require much more resources (quadratic relationship)
                n_threads=8,  # The number of CPU threads to use
                n_gpu_layers=-1,  # The number of layers to offload to GPU, if GPU acceleration is available (TEST)
            )

    def generate_output(self, question: str) -> Generator[
        Dict[str, Union[str, List[Dict[str, Union[str, None]]]]], None, None]:
        """
        Generates output from the Mixtral model based on the input question.

        Args:
            question (str): The input question prompt.

        Returns:
            Generator[Dict[str, Union[str, List[Dict[str, Union[str, None]]]]], None, None]:
                A generator returning response dictionaries with the following structure:
                {
                    'id': str,
                    'object': str,
                    'created': int,
                    'model': str,
                    'choices': [
                        {
                            'text': str,
                            'index': int,
                            'logprobs': Optional[dict],
                            'finish_reason': Optional[str]
                        }
                    ]
                }
        """
        if self.llm is None:
            raise ValueError("Mixtral is not initialized. Please call initialize_mixtral() first.")

        output = self.llm(
            question,  # Prompt
            max_tokens=400,  # Generate up to X tokens
            stop=["$STOP$"],  # Stop token
            echo=False,  # Whether to echo the used prompt
            stream=True,  # whether to stream output or not (this has been causing some issues with the website)
            temperature=0.001,  # the "randomness/creativity" of the resonses
        )
        return output

    def construct_prompt(self, input_text: str, RAG: str = "") -> str:
        """
        Constructs a prompt for the Mixtral model based on the input text and optional context.

        Args:
            input_text (str): The input question text.
            RAG (str, optional): The context to be included in the prompt. Defaults to an empty string.

        Returns:
            str: The constructed prompt.
        """
        if RAG:
            prompt = f"Answer the question using the context below and try to keep the explanation brief.\n" \
                     f"End your explanation with $STOP$.\n" \
                     f"Context: {RAG.strip('.')}.\n" \
                     f"Question: {input_text.strip('?')}?\n" \
                     f"Answer: "
        else:
            prompt = f"Answer the question to the best of your ability and try to keep the explanation brief.\n" \
                     f"End your explanation with $STOP$.\n" \
                     f"Question: {input_text.strip('?')}?\n" \
                     f"Answer: "
        return prompt

    def initialize_splade_model(self):
        """
        Initializes the Splade model and tokenizer.

        Returns:
            sparsembed.model.Splade: The initialized Splade model.
        """
        model = AutoModelForMaskedLM.from_pretrained("naver/splade_v2_max")
        tokenizer = AutoTokenizer.from_pretrained("naver/splade_v2_max")
        return sparsembed.model.Splade(model=model, tokenizer=tokenizer)

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.float64:
        """
        Computes the cosine similarity between two vectors.

        Args:
            a (np.ndarray): First input vector.
            b (np.ndarray): Second input vector.

        Returns:
            np.float64: Cosine similarity between vector a and vector b.
        """
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot / (norm_a * norm_b)

    def embed(self, text: str) -> dict:
        """
        Encodes a given text into sparse embeddings using the Splade model.

        Args:
            text (str): The text to be encoded into embeddings.

        Returns:
            dict: A dictionary containing the sparse activations from the embeddings.
        """
        with torch.no_grad():
            embeddings = self.model.encode(
                texts=[text],  # Provide the input text as a list
                truncation="longest_first"  # Choose a valid truncation strategy if needed
            )
        return embeddings

    def get_splade_embeddings(self, text: str) -> torch.Tensor:
        """
        Encodes a given text into sparse embeddings using the Splade model.

        Args:
            text (str): The text to be encoded into embeddings.

        Returns:
            torch.Tensor: The sparse activations from the embeddings.
        """
        embeddings = self.embed(text)
        return embeddings["sparse_activations"]

    @staticmethod
    def load_vector_data(file_path: str) -> tuple:
        """
        Loads vector data from a JSON file and converts it back to tensors.

        Args:
            file_path (str): The path to the JSON file containing the vector data.

        Returns:
            tuple: A tuple containing two elements:
                - loaded_tensors (list of torch.Tensor): A list of tensors converted from the stored lists.
                - loaded_sentences (list of str): A list of sentences corresponding to the vectors.
        """
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)

        # Retrieve lists and sentences
        loaded_lists = loaded_data["arrays"]
        loaded_sentences = loaded_data["sentences"]

        # Convert lists back to tensors
        loaded_tensors = [torch.tensor(lst) for lst in loaded_lists]

        return loaded_tensors, loaded_sentences

    def find_most_similar_sentence(self, question: str, loaded_tensors: list, loaded_sentences: list) -> str:
        """
        Finds the most similar sentence to the given question from a list of pre-loaded sentences.

        Args:
            question (str): The question to compare against the loaded sentences.
            loaded_tensors (list of torch.Tensor): The list of tensors representing the embeddings of the loaded sentences.
            loaded_sentences (list of str): The list of pre-loaded sentences corresponding to the embeddings.

        Returns:
            str: The sentence from the loaded sentences that is most similar to the given question.
        """
        sparse_embedding_input = self.get_splade_embeddings(question)

        # Calculate cosine similarities
        similarities = [self.cosine_similarity(i, sparse_embedding_input.T)[0, 0] for i in loaded_tensors]

        # Find the index of the max similarity value
        max_value_index = similarities.index(max(similarities))

        # Return the most similar sentence
        return loaded_sentences[max_value_index]


processor = TextProcessor()


@app.route('/chat', methods=['POST'])
def chat():
    """
        Endpoint to handle chat requests.

        Receives a JSON payload with a 'message' field, processes it to find the most similar sentence from the vector database,
        generates a response using the Mixtral model, and returns the generated response.

        Returns:
            JSON response with the generated message.
        """
    data = request.get_json()
    message = data.get('message')
    logging.info(f"Received message: {message}")

    try:
        # Find the most similar sentence from the database
        similar_sentence = processor.find_most_similar_sentence(message, processor.loaded_tensors,
                                                                processor.loaded_sentences)
        logging.info(f"Found similar sentence: {similar_sentence}")

        # Use the similar sentence as context for the Mixtral model
        prompt = processor.construct_prompt(message, similar_sentence)
        print(prompt)
        output = processor.generate_output(prompt)
        logging.debug(f"Raw output: {output}")

        response_text = ""
        for response in output:
            print(response[
                      "choices"])  # for each response in the output, print the choices dictionary inside each response
            for choice in response["choices"]:
                response_text += choice["text"]  # combine the output text into a singular string

        logging.info(f"Sending response: {response_text}")
        return jsonify({"message": response_text})
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return jsonify({"message": "Error processing request"}), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    """
        Endpoint to handle feedback.

        Receives a JSON payload with 'feedback' and 'rating' fields, logs the received feedback and rating,
        and returns a confirmation message.

        Returns:
            str: Confirmation message.
        """
    data = request.get_json()
    feedback = data.get('feedback')
    rating = data.get('rating')
    logging.info(f"Received feedback: {feedback} with rating {rating}")
    return "Feedback received", 200


if __name__ == '__main__':
    """
        Entry point for running the Flask application.

        This block ensures that the Flask application runs only if the script is executed directly.
        It will not run if the script is imported as a module in another script.

        The Flask application will be started on host '0.0.0.0', making it accessible from any network interface,
        and will listen on port 5000 for incoming HTTP requests.

        app.run Parameters:
            host (str): The hostname to listen on. '0.0.0.0' makes the server accessible externally.
            port (int): The port of the web server. Defaults to 5000.
        """
    app.run(host='0.0.0.0', port=5000)
