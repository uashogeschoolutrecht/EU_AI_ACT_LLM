import unittest
from unittest.mock import patch, MagicMock
from mixtral import TextProcessor
 
class TestTextProcessor(unittest.TestCase):
    @patch('mixtral.Llama')
    def test_initialize_mixtral(self, MockLlama):
        processor = TextProcessor()
        MockLlama.assert_called_once_with(
            model_path="models/mixtral-8x7b-v0.1.Q5_K_M.gguf",
            n_ctx=2048,
            n_threads=0,
            n_gpu_layers=-1,
        )
        self.assertIsNotNone(processor.llm)
   
    @patch('mixtral.Llama')
    def test_generate_output(self, MockLlama):
        mock_llm_instance = MockLlama.return_value
        mock_llm_instance.return_value = [
            {
                'id': 'cmpl-b011cf31-6d66-4328-8a64-76b987b5970d',
                'object': 'text_completion',
                'created': 1718777621,
                'model': 'models/mixtral-8x7b-v0.1.Q5_K_M.gguf',
                'choices': [{'text': 'plan', 'index': 0, 'logprobs': None, 'finish_reason': None}]
            }
        ]
 
        processor = TextProcessor()
        question = "What is your plan?"
        output = processor.generate_output(question)
       
        responses = list(output)  # Convert generator to list to assert
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0]['choices'][0]['text'], 'plan')
 
    def test_construct_prompt(self):
        processor = TextProcessor()
        input_text = "What is the capital of France?"
        RAG = "Paris is the capital of France."
       
        prompt = processor.construct_prompt(input_text, RAG)
        expected_prompt = (
            "Answer the question using the context below and try to keep the explanation brief.\n"
            "End your explanation with $STOP$.\n"
            "Context: Paris is the capital of France.\n"
            "Question: What is the capital of France?\n"
            "Answer: "
        )
        self.assertEqual(prompt.strip(), expected_prompt.strip())
       
        prompt_without_RAG = processor.construct_prompt(input_text)
        expected_prompt_without_RAG = (
            "Answer the question to the best of your ability and try to keep the explanation brief.\n"
            "End your explanation with $STOP$.\n"
            "Question: What is the capital of France?\n"
            "Answer: "
        )
        self.assertEqual(prompt_without_RAG.strip(), expected_prompt_without_RAG.strip())
 
if __name__ == '__main__':
    unittest.main()
