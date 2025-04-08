from llama_cpp import Llama
from typing import Generator, Dict, Union, List

class TextProcessor:
    def __init__(self):
        """
        Initializes the TextProcessor object and calls the method to initialize the Mixtral model.
        """
        self.llm = None
        self.initialize_mixtral()
    
    def initialize_mixtral(self) -> None:
        """
        Initializes the Mixtral language model if it is not already initialized.
        """
        if self.llm is None:
            self.llm = Llama(
                model_path="models/mixtral-8x7b-v0.1.Q5_K_M.gguf",  # Download the model file/load the model file from location
                n_ctx=2048,             # The max sequence length to use - note that longer sequence lengths require much more resources (quadratic relationship)
                n_threads=0,            # The number of CPU threads to use
                n_gpu_layers=-1,        # The number of layers to offload to GPU, if GPU acceleration is available
                )
    
    def generate_output(self, question: str) -> Generator[Dict[str, Union[str, List[Dict[str, Union[str, None]]]]], None, None]:
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
            question,           # Prompt
            max_tokens=400,     # Generate up to X tokens
            stop=["$STOP$"],    # Stop token
            echo=False,         # Whether to echo the used prompt
            stream=True,        # whether to stream output or not (this has been causing some issues with the website)
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


if __name__ == "__main__":                                          #THIS CODE DOES NOT RUN IF MIXTRAL IS CALLED FROM THE WEBSITE
    processor = TextProcessor()                                     #initialize textprocessor
    print("Mixtral initialized")
    while True:
        input_text = input("Enter question (or 'exit' to quit): ")
        if input_text.lower() == "exit":                            #exit the loop when typing "exit"
            break
        else:
            RAG = "i don't like pie i like apples"                  #give a hardcoded RAG input
            prompt = processor.construct_prompt(input_text, RAG)    #creates a prompt using the user input and the hardcoded RAG
            output_text = processor.generate_output(prompt)         #call the generator to process the prompt
            text = ""
            for response in output_text:
                print(response["choices"])                          #for each response in the output, print the choices dictionary inside each response 
                for choice in response["choices"]:
                    text += choice["text"]                          #combine the output text into a singular string
                    print(text)                                     
