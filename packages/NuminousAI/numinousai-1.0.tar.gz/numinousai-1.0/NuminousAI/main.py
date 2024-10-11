import re
import os
import json
import base64
import random
import requests

UserAgents = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9415.94",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Viewer/99.9.9009.89",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5; rv:123.0esr) Gecko/20100101 Firefox/123.0esr",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9979.100",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.3.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.126 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/121.2277.107 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/92.3.3357.27",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 EdgA/121.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.86 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.1.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/91.2.2121.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Unique/97.7.7286.70",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 OpenWave/94.4.4504.39",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.105 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Unique/97.7.7239.70",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Trailer/93.3.3516.28",
    "Mozilla/5.0 (Android 11; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.99 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.141 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.105 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 DuckDuckGo/7 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Agency/98.8.8175.80",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPX/2.2.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 Config/92.2.7601.2",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.150 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 Ddg/17.0",
    "Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.65 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) AvastSecureBrowser/5.3.1 Mobile/15E148 Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Config/92.2.2788.20",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.72 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Herring/95.1.1930.31",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Agency/98.8.8188.80",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.79 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.116 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.86 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.96 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/118.0.2088.68 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 AtContent/95.5.5392.49",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/119.0.2151.78 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 8.1.0; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 RDDocuments/8.4.8.940",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/120.0.2210.150 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 PTST/240201.144844",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 GLS/100.10.9850.99",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/116.0.1938.56 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/117.0.2045.48 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 8.1.0; C5 2019 Build/OPM2.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0.3 Mobile/15E148 Safari/604.1 RDDocuments/8.7.2.978",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0 Trailer/93.3.3695.30"
]

# Copyright (c) 2024 Sujal Rajpoot
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# THE ABOVE COPYRIGHT NOTICE AND THIS PERMISSION NOTICE SHALL BE INCLUDED IN ALL
# COPIES OR SUBSTANTIAL PORTIONS OF THE SOFTWARE.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Unauthorized use, duplication, or distribution of this code without explicit 
# permission from Sujal Rajpoot will result in legal action. All rights reserved.
#
# For permission to use this code, please contact the author at sujalrajpoot70@gmail.com.

class DeepInfra:
    """
    A Python interface for interacting with various DeepInfra LLM models.

    This class provides methods to perform a variety of tasks using models hosted by the 
    DeepInfra API. Supported tasks include text generation, text-to-image conversion, 
    automatic speech recognition, text-to-speech conversion, and zero-shot image classification.

    # Available Feature Classes
        TextGeneration: This class enables text generation using deep learning models. It can be used for text generation tasks. The output text is typically generated from the input prompt.
            - Use Case: Text generation, language translation, and content creation.
        
        AutomaticSpeechRecognition: This class enables automatic speech recognition using deep learning models. It can be used for speech-to-text or text-to-speech conversion. The output text is typically generated from the input audio.
            - Use Case: Speech-to-text and voice synthesis.

        TextToSpeech: This class enables text-to-speech conversion using deep learning models. It can be used for text-to-speech conversion. The output audio is typically generated from the input text.
            - Use Case: Text-to-speech and voice synthesis.

        ZeroShotImageClassification: This class enables zero-shot image classification using deep learning models. It can be used for image classification tasks. The output text is typically generated from the input image.
            - Use Case: Image classification, image captioning, and image search.

        # For Classes Documentation and their Available Models
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().TextGeneration() or AutomaticSpeechRecognition() or TextToSpeech() or ZeroShotImageClassification()
            >>> print(ai.TextGeneration().list_available_models())

        # For Using any class feature like TextGeneration
            - Example
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().TextGeneration()
            >>> query = "Hello, How are you?"
            >>> Model = "Meta-Llama-3.1-70B-Instruct"
            >>> print(ai.generate(message=query, model=Model))
            >>> print(ai.generate(message=query, model=Model, stream=True))
            
    For more information, you can visit https://deepinfra.com/models
    """
    class TextGeneration:
        """
        Text generation AI models can generate coherent and natural-sounding human language text, making them useful for a variety of applications from language translation to content creation.

        There are several types of text generation AI models, including rule-based, statistical, and neural models. Neural models, and in particular transformer-based models like GPT, have achieved state-of-the-art results in text generation tasks. These models use artificial neural networks to analyze large text corpora and learn the patterns and structures of language.

        While text generation AI models offer many exciting possibilities, they also present some challenges. For example, it's essential to ensure that the generated text is ethical, unbiased, and accurate, to avoid potential harm or negative consequences.

        # Example
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().TextGeneration()
            >>> query = "Hello, How are you?"
            >>> Model = "Meta-Llama-3.1-70B-Instruct"
            >>> print(ai.generate(message=query, model=Model))
            >>> print(ai.generate(message=query, model=Model, stream=True))

        For more information visit: https://deepinfra.com/models/text-generation
        """
        def list_available_models(self) -> str:
            """List all available models with their Documentations."""
            print("Available Models:\n")
            Available_Models = {
                "Meta-Llama-3.1-405B-Instruct":"Meta developed and released the Meta Llama 3.1 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B and 405B sizes.\nFor more information visit: https://deepinfra.com/meta-llama/Meta-Llama-3.1-405B-Instruct\n",

                "Meta-Llama-3.1-70B-Instruct":"Meta developed and released the Meta Llama 3.1 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B and 405B sizes.\nFor more information visit: https://deepinfra.com/meta-llama/Meta-Llama-3.1-70B-Instruct\n",

                "Meta-Llama-3.1-8B-Instruct":"Meta developed and released the Meta Llama 3.1 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B and 405B sizes.\nFor more information visit: https://deepinfra.com/meta-llama/Meta-Llama-3.1-8B-Instruct\n",
                
                "Meta-Llama-3-8B-Instruct":"Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8 and 70B sizes.\nFor more information visit: https://deepinfra.com/meta-llama/Meta-Llama-3-8B-Instruct\n",

                "Meta-Llama-3-70B-Instruct":"Model Details Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8 and 70B sizes.\nFor more information visit: https://deepinfra.com/meta-llama/Meta-Llama-3-70B-Instruct\n",

                "Llama-2-7b-chat-hf":"Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. This is the repository for the 7B fine-tuned model, optimized for dialogue use cases and converted for the Hugging Face Transformers format.\nFor more information visit: https://deepinfra.com/meta-llama/Llama-2-7b-chat-hf\n",

                "Llama-2-13b-chat-hf":"Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. This is the repository for the 7B fine-tuned model, optimized for dialogue use cases and converted for the Hugging Face Transformers format.\nFor more information visit: https://deepinfra.com/meta-llama/Llama-2-13b-chat-hf\n",

                "Llama-2-70b-chat-hf":"LLaMa 2 is a collections of LLMs trained by Meta. This is the 70B chat optimized version. This endpoint has per token pricing.\nFor more information visit: https://deepinfra.com/meta-llama/Llama-2-70b-chat-hf\n",

                "Mistral-7B-Instruct-v0.1":"The Mistral-7B-Instruct-v0.1 Large Language Model (LLM) is a instruct fine-tuned version of the Mistral-7B-v0.1 generative text model using a variety of publicly available conversation datasets.\nFor more information visit: https://deepinfra.com/mistralai/Mistral-7B-Instruct-v0.1\n",

                "Mistral-7B-Instruct-v0.2":"The Mistral-7B-Instruct-v0.2 Large Language Model (LLM) is a instruct fine-tuned version of the Mistral-7B-v0.2 generative text model using a variety of publicly available conversation datasets.\nFor more information visit: https://deepinfra.com/mistralai/Mistral-7B-Instruct-v0.2\n",

                "Mistral-7B-Instruct-v0.3":"Mistral-7B-Instruct-v0.3 is an instruction-tuned model, next iteration of of Mistral 7B that has larger vocabulary, newer tokenizer and supports function calling.\nFor more information visit: https://deepinfra.com/mistralai/Mistral-7B-Instruct-v0.3\n",

                "Mistral-Nemo-Instruct-2407":"12B model trained jointly by Mistral AI and NVIDIA, it significantly outperforms existing models smaller or similar in size.\nFor more information visit: https://deepinfra.com/mistralai/Mistral-Nemo-Instruct-2407\n",

                "Mixtral-8x7B-Instruct-v0.1":"Mixtral is mixture of expert large language model (LLM) from Mistral AI. This is state of the art machine learning model using a mixture 8 of experts (MoE) 7b models. During inference 2 expers are selected. This architecture allows large models to be fast and cheap at inference. The Mixtral-8x7B outperforms Llama 2 70B on most benchmarks.\nFor more information visit: https://deepinfra.com/mistralai/Mixtral-8x7B-Instruct-v0.1\n",

                "Mixtral-8x22B-Instruct-v0.1":"This is the instruction fine-tuned version of Mixtral-8x22B - the latest and largest mixture of experts large language model (LLM) from Mistral AI. This state of the art machine learning model uses a mixture 8 of experts (MoE) 22b models. During inference 2 experts are selected. This architecture allows large models to be fast and cheap at inference.\nFor more information visit: https://deepinfra.com/mistralai/Mixtral-8x22B-Instruct-v0.1\n",

                "Mixtral-8x22B-v0.1":"Mixtral-8x22B is the latest and largest mixture of expert large language model (LLM) from Mistral AI. This is state of the art machine learning model using a mixture 8 of experts (MoE) 22b models. During inference 2 expers are selected. This architecture allows large models to be fast and cheap at inference. This model is not instruction tuned.\nFor more information visit: https://deepinfra.com/mistralai/Mixtral-8x22B-v0.1\n",

                "Dolphin-2.6-mixtral-8x7b":"The Dolphin 2.6 Mixtral 8x7b model is a finetuned version of the Mixtral-8x7b model, trained on a variety of data including coding data, for 3 days on 4 A100 GPUs. It is uncensored and requires trust_remote_code. The model is very obedient and good at coding, but not DPO tuned. The dataset has been filtered for alignment and bias. The model is compliant with user requests and can be used for various purposes such as generating code or engaging in general chat.\nFor more information visit: https://deepinfra.com/cognitivecomputations/dolphin-2.6-mixtral-8x7b\n",

                "Reflection-Llama-3.1-70B":"Reflection Llama-3.1 70B is trained with a new technique called Reflection-Tuning that teaches a LLM to detect mistakes in its reasoning and correct course. The model was trained on synthetic data.\nFor more information visit: https://deepinfra.com/mattshumer/Reflection-Llama-3.1-70B\n",

                "MiniCPM-Llama3-V-2_5":"MiniCPM-Llama3-V 2.5 is the latest model in the MiniCPM-V series. The model is built on SigLip-400M and Llama3-8B-Instruct with a total of 8B parameters. It exhibits a significant performance improvement over MiniCPM-V 2.0.\nFor more information visit: https://deepinfra.com/openbmb/MiniCPM-Llama3-V-2_5\n",

                "Gemma-1.1-7b-it":"Gemma is an open-source model designed by Google. This is Gemma 1.1 7B (IT), an update over the original instruction-tuned Gemma release. Gemma 1.1 was trained using a novel RLHF method, leading to substantial gains on quality, coding capabilities, factuality, instruction following and multi-turn conversation quality.\nFor more information visit: https://deepinfra.com/google/gemma-1.1-7b-it\n",

                "Gemma-2-9b-it":"Gemma is a family of lightweight, state-of-the-art open models from Google. The 9B Gemma 2 model delivers class-leading performance, outperforming Llama 3 8B and other open models in its size category.\nFor more information visit: https://deepinfra.com/google/gemma-2-9b-it\n",

                "Gemma-2-27b-it":"Gemma is a family of lightweight, state-of-the-art open models from Google. Gemma-2-27B delivers the best performance for its size class, and even offers competitive alternatives to models more than twice its size.\nFor more information visit: https://deepinfra.com/google/gemma-2-27b-it\n",

                "L3-70B-Euryale-v2.1":"Euryale 70B v2.1 is a model focused on creative roleplay from Sao10k\nFor more information visit: https://deepinfra.com/Sao10K/L3-70B-Euryale-v2.1\n",

                "Qwen2-72B-Instruct":"The 72 billion parameter Qwen2 excels in language understanding, multilingual capabilities, coding, mathematics, and reasoning.\nFor more information visit: https://deepinfra.com/Qwen/Qwen2-72B-Instruct\n",

                "WizardLM-2-8x22B":"WizardLM-2 8x22B is Microsoft AI's most advanced Wizard model. It demonstrates highly competitive performance compared to those leading proprietary models.\nFor more information visit: https://deepinfra.com/microsoft/WizardLM-2-8x22B\n",

                "WizardLM-2-7B":"WizardLM-2 7B is the smaller variant of Microsoft AI's latest Wizard model. It is the fastest and achieves comparable performance with existing 10x larger open-source leading models\nFor more information visit: https://deepinfra.com/microsoft/WizardLM-2-7B\n",

                "lzlv_70b_fp16_hf":"A Mythomax/MLewd_13B-style merge of selected 70B models A multi-model merge of several LLaMA2 70B finetunes for roleplaying and creative work. The goal was to create a model that combines creativity with intelligence for an enhanced experience.\nFor more information visit: https://deepinfra.com/lizpreciatior/lzlv_70b_fp16_hf\n",

                "Yi-34B-Chat":"The Yi series models are the next generation of open-source large language models trained from scratch by 01.AI.\nFor more information visit: https://deepinfra.com/01-ai/Yi-34B-Chat\n",

                "Chronos-hermes-13b-v2":"This offers the imaginative writing style of chronos while still retaining coherency and being capable. Outputs are long and utilize exceptional prose. Supports a maxium context length of 4096. The model follows the Alpaca prompt format.\nFor more information visit: https://deepinfra.com/Austism/chronos-hermes-13b-v2\n",

                "MythoMax-L2-13b":"The idea behind this merge is that each layer is composed of several tensors, which are in turn responsible for specific functions. Using MythoLogic-L2's robust understanding as its input and Huginn's extensive writing capability as its output seems to have resulted in a model that exceeds at both, confirming my theory. (More details to be released at a later time). This type of merge is incapable of being illustrated, as each of its 363 tensors had an unique ratio applied to it. As with my prior merges, gradients were part of these ratios to further finetune its behaviour.\nFor more information visit: https://deepinfra.com/Gryphe/MythoMax-L2-13b\n",

                "MythoMax-L2-13b-turbo":"Faster version of Gryphe/MythoMax-L2-13b running on multiple H100 cards in fp8 precision. Up to 160 tps.\nFor more information visit: https://deepinfra.com/Gryphe/MythoMax-L2-13b-turbo\n",

                "Zephyr-orpo-141b-A35b-v0.1":"Zephyr 141B-A35B is an instruction-tuned (assistant) version of Mixtral-8x22B. It was fine-tuned on a mix of publicly available, synthetic datasets. It achieves strong performance on chat benchmarks.\nFor more information visit: https://deepinfra.com/HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1\n",

                "Phind-CodeLlama-34B-v2":"Phind-CodeLlama-34B-v2 is an open-source language model that has been fine-tuned on 1.5B tokens of high-quality programming-related data and achieved a pass@1 rate of 73.8% on HumanEval. It is multi-lingual and proficient in Python, C/C++, TypeScript, Java, and more. It has been trained on a proprietary dataset of instruction-answer pairs instead of code completion examples. The model is instruction-tuned on the Alpaca/Vicuna format to be steerable and easy-to-use. It accepts the Alpaca/Vicuna instruction format and can generate one completion for each prompt.\nFor more information visit: https://deepinfra.com/Phind/Phind-CodeLlama-34B-v2\n",

                "CodeLlama-34b-Instruct-hf":"Code Llama is a state-of-the-art LLM capable of generating code, and natural language about code, from both code and natural language prompts. This particular instance is the 34b instruct variant\nFor more information visit: https://deepinfra.com/codellama/CodeLlama-34b-Instruct-hf\n",

                "CodeLlama-70b-Instruct-hf":"CodeLlama-70b is the largest and latest code generation from the Code Llama collection.\nFor more information visit: https://deepinfra.com/codellama/CodeLlama-70b-Instruct-hf\n",

                "Qwen2-7B-Instruct":"The 7 billion parameter Qwen2 excels in language understanding, multilingual capabilities, coding, mathematics, and reasoning.\nFor more information visit: https://deepinfra.com/Qwen/Qwen2-7B-Instruct\n",

                "Starcoder2-15b":"StarCoder2-15B model is a 15B parameter model trained on 600+ programming languages. It specializes in code completion.\nFor more information visit: https://deepinfra.com/bigcode/starcoder2-15b\n",

                "Starcoder2-15b-instruct-v0.1":"We introduce StarCoder2-15B-Instruct-v0.1, the very first entirely self-aligned code Large Language Model (LLM) trained with a fully permissive and transparent pipeline. Our open-source pipeline uses StarCoder2-15B to generate thousands of instruction-response pairs, which are then used to fine-tune StarCoder-15B itself without any human annotations or distilled data from huge and proprietary LLMs.\nFor more information visit: https://deepinfra.com/bigcode/starcoder2-15b-instruct-v0.1\n",

                "Dolphin-2.9.1-llama-3-70b":"Dolphin 2.9.1, a fine-tuned Llama-3-70b model. The new model, trained on filtered data, is more compliant but uncensored. It demonstrates improvements in instruction, conversation, coding, and function calling abilities.\nFor more information visit: https://deepinfra.com/cognitivecomputations/dolphin-2.9.1-llama-3-70b\n",

                "Dbrx-instruct":"DBRX is an open source LLM created by Databricks. It uses mixture-of-experts (MoE) architecture with 132B total parameters of which 36B parameters are active on any input. It outperforms existing open source LLMs like Llama 2 70B and Mixtral-8x7B on standard industry benchmarks for language understanding, programming, math, and logic.\nFor more information visit: https://deepinfra.com/databricks/dbrx-instruct\n",

                "Airoboros-70b":"Latest version of the Airoboros model fine-tunned version of llama-2-70b using the Airoboros dataset. This model is currently running jondurbin/airoboros-l2-70b-2.2.1\nFor more information visit: https://deepinfra.com/deepinfra/airoboros-70b\n",

                "Codegemma-7b-it":"CodeGemma is a collection of lightweight open code models built on top of Gemma. CodeGemma models are text-to-text and text-to-code decoder-only models and are available as a 7 billion pretrained variant that specializes in code completion and code generation tasks, a 7 billion parameter instruction-tuned variant for code chat and instruction following and a 2 billion parameter pretrained variant for fast code completion.\nFor more information visit: https://deepinfra.com/google/codegemma-7b-it\n",

                "Phi-3-medium-4k-instruct":"The Phi-3-Medium-4K-Instruct is a powerful and lightweight language model with 14 billion parameters, trained on high-quality data to excel in instruction following and safety measures. It demonstrates exceptional performance across benchmarks, including common sense, language understanding, and logical reasoning, outperforming models of similar size.\nFor more information visit: https://deepinfra.com/microsoft/Phi-3-medium-4k-instruct\n",

                "Nemotron-4-340B-Instruct":"Nemotron-4-340B-Instruct is a chat model intended for use for the English language, designed for Synthetic Data Generation\nFor more information visit: https://deepinfra.com/nvidia/Nemotron-4-340B-Instruct\n",

                "Openchat-3.6-8b":"Openchat 3.6 is a LLama-3-8b fine tune that outperforms it on multiple benchmarks.\nFor more information visit: https://deepinfra.com/openchat/openchat-3.6-8b\n",

                "Openchat_3.5":"OpenChat is a library of open-source language models that have been fine-tuned with C-RLFT, a strategy inspired by offline reinforcement learning. These models can learn from mixed-quality data without preference labels and have achieved exceptional performance comparable to ChatGPT. The developers of OpenChat are dedicated to creating a high-performance, commercially viable, open-source large language model and are continuously making progress towards this goal.\nFor more information visit: https://deepinfra.com/openchat/openchat_3.5\n"
            }
            for model_name, model_documentation in Available_Models.items():
                print(f"{model_name} : {model_documentation}")
            return "You Can Use any Model by giving its name in generate function like: generate(message='Hello, How are you?', model='Meta-Llama-3.1-70B-Instruct')"
        
        # Define the method to generate text
        def generate(self, message: str, model:str = "Meta-Llama-3-70B-Instruct", system_prompt: str = "Be Helpful and Friendly.", max_tokens: int = 512, temperature: float = 0.7, stream: bool = False, chunk_size: int = 1) -> str:
            """
            Generates a text completion from the specified model based on the input message and system prompt.

            This method sends a request to the model, using the `message` as input and generating a response guided by a system prompt. The method supports both regular and streamed responses. If streaming is enabled, the response will be displayed in real-time, chunk by chunk, while also being collected as a full string.

            # Args
                message (str): The user input message to send to the model.
                system_prompt (str): A system-level instruction to guide the behavior of the model. Default is 'Be Helpful and Friendly.'.
                max_tokens (int): The maximum number of tokens to generate. Default is 512.
                temperature (float): A value controlling the randomness of the output (between 0 and 1). Default is 0.7.
                stream (bool): If True, the response will be printed in real-time as it streams. Default is False.
                chunk_size (int): The size of each chunk to be retrieved from the stream. Default is 1.

            # Returns
                str: The generated text completion from the model.
                If streaming is enabled, the response is printed live and also returned as a full concatenated string.

            # Raises
                ValueError: If temperature is not between 0 and 1 or if max_tokens is outside the acceptable range.
                Exception: If any error occurs during the HTTP request or response parsing.

            # Example
                >>> if __name__=="__main__":
                >>> ai = TextGeneration()
                >>> query = "Hello, How are you?"
                >>> Model = "Meta-Llama-3.1-70B-Instruct"
                >>> print(ai.generate(message=query, model=Model))
                >>> print(ai.generate(message=query, model=Model, stream=True))

            # Comments
                - The method first checks if the temperature and max_tokens are within valid ranges. 
                - The payload is structured to contain the model name, user message, and temperature parameters.
                - The method uses streaming if enabled, printing each received chunk immediately.
                - The response is concatenated and returned as a single string after the completion.
            """
            url = "https://api.deepinfra.com/v1/openai/chat/completions"
            Models = {
                "Meta-Llama-3.1-405B-Instruct":"meta-llama/Meta-Llama-3.1-405B-Instruct",
                "Meta-Llama-3.1-70B-Instruct":"meta-llama/Meta-Llama-3.1-70B-Instruct",
                "Meta-Llama-3.1-8B-Instruct":"meta-llama/Meta-Llama-3.1-8B-Instruct",
                "Reflection-Llama-3.1-70B":"mattshumer/Reflection-Llama-3.1-70B",
                "Mistral-Nemo-Instruct-2407":"mistralai/Mistral-Nemo-Instruct-2407",
                "MiniCPM-Llama3-V-2_5":"openbmb/MiniCPM-Llama3-V-2_5",
                "Gemma-2-27b-it":"google/gemma-2-27b-it",
                "Gemma-2-9b-it":"google/gemma-2-9b-it",
                "L3-70B-Euryale-v2.1":"Sao10K/L3-70B-Euryale-v2.1",
                "Meta-Llama-3-70B-Instruct":"meta-llama/Meta-Llama-3-70B-Instruct",
                "Qwen2-72B-Instruct":"Qwen/Qwen2-72B-Instruct",
                "Mistral-7B-Instruct-v0.3":"mistralai/Mistral-7B-Instruct-v0.3",
                "Meta-Llama-3-8B-Instruct":"meta-llama/Meta-Llama-3-8B-Instruct",
                "Mixtral-8x22B-Instruct-v0.1":"mistralai/Mixtral-8x22B-Instruct-v0.1",
                "WizardLM-2-8x22B":"microsoft/WizardLM-2-8x22B",
                "WizardLM-2-7B":"microsoft/WizardLM-2-7B",
                "Mixtral-8x7B-Instruct-v0.1":"mistralai/Mixtral-8x7B-Instruct-v0.1",
                "lzlv_70b_fp16_hf":"lizpreciatior/lzlv_70b_fp16_hf",
                "Yi-34B-Chat":"01-ai/Yi-34B-Chat",
                "Chronos-hermes-13b-v2":"Austism/chronos-hermes-13b-v2",
                "MythoMax-L2-13b":"Gryphe/MythoMax-L2-13b",
                "MythoMax-L2-13b-turbo":"Gryphe/MythoMax-L2-13b-turbo",
                "Zephyr-orpo-141b-A35b-v0.1":"HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1",
                "Phind-CodeLlama-34B-v2":"Phind/Phind-CodeLlama-34B-v2",
                "Qwen2-7B-Instruct":"Qwen/Qwen2-7B-Instruct",
                "Starcoder2-15b":"bigcode/starcoder2-15b",
                "Starcoder2-15b-instruct-v0.1":"bigcode/starcoder2-15b-instruct-v0.1",
                "CodeLlama-34b-Instruct-hf":"codellama/CodeLlama-34b-Instruct-hf",
                "CodeLlama-70b-Instruct-hf":"codellama/CodeLlama-70b-Instruct-hf",
                "Dolphin-2.6-mixtral-8x7b":"cognitivecomputations/dolphin-2.6-mixtral-8x7b",
                "Dolphin-2.9.1-llama-3-70b":"cognitivecomputations/dolphin-2.9.1-llama-3-70b",
                "Dbrx-instruct":"databricks/dbrx-instruct",
                "Airoboros-70b":"deepinfra/airoboros-70b",
                "Codegemma-7b-it":"google/codegemma-7b-it",
                "Gemma-1.1-7b-it":"google/gemma-1.1-7b-it",
                "Llama-2-13b-chat-hf":"meta-llama/Llama-2-13b-chat-hf",
                "Llama-2-70b-chat-hf":"meta-llama/Llama-2-70b-chat-hf",
                "Llama-2-7b-chat-hf":"meta-llama/Llama-2-7b-chat-hf",
                "Phi-3-medium-4k-instruct":"microsoft/Phi-3-medium-4k-instruct",
                "Mistral-7B-Instruct-v0.1":"mistralai/Mistral-7B-Instruct-v0.1",
                "Mistral-7B-Instruct-v0.2":"mistralai/Mistral-7B-Instruct-v0.2",
                "Mixtral-8x22B-v0.1":"mistralai/Mixtral-8x22B-v0.1",
                "Nemotron-4-340B-Instruct":"nvidia/Nemotron-4-340B-Instruct",
                "Openchat-3.6-8b":"openchat/openchat-3.6-8b",
                "Openchat_3.5":"openchat/openchat_3.5"
            }
            # Validate model to ensure it is in the Models dict
            if model not in Models:
                available_models = ',\n'.join(Models.keys())
                return f"Model key '{model}' is not valid. Please select a valid model.\nAvailable models are: {available_models}"

            model_value = Models[model]
            # Validate temperature to ensure it is between 0 and 1
            if not (0 <= temperature <= 1):
                return f"Your Temperature Value is {temperature}. Please Choose Temperature Value Between 0 to 1 eg. 0.7, 1"

            # Validate max_tokens to ensure it's in the valid range (1 to 1,000,000)
            if not (1 <= max_tokens <= 1000000):
                return "maximum length of the newly generated text must be between 1 and 1,000,000."

            # Prepare the headers for the API request
            headers = {"Accept": "text/event-stream","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.9,hi;q=0.8","Connection": "keep-alive","Content-Type": "application/json","Dnt": "1","Host": "api.deepinfra.com","Origin": "https://deepinfra.com","Referer": "https://deepinfra.com/","Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": f"{random.choice(UserAgents)}","X-Deepinfra-Source": "web-page"}

            # Prepare the payload for the API request
            payload = {
                "model": model_value,
                "messages": [
                    {"role": "system", "content": system_prompt},  # system prompt to guide the model's behavior
                    {"role": "user", "content": message}  # user message to the model
                ],
                "temperature": temperature,  # controls the randomness of the response
                "max_tokens": max_tokens,  # maximum number of tokens to generate
                "stop": [],  # an empty list means the model won't stop until it reaches max_tokens or context length
                "stream": True  # enables streaming of the response
            }
            try:
                # Make the POST request to the API endpoint with streaming enabled
                response = requests.post(url, headers=headers, json=payload, stream=True, timeout=None)

                streaming_text = ""  # Initialize the text container for the final response

                # Stream and process the response in real-time
                for value in response.iter_lines(decode_unicode=True, chunk_size=chunk_size):
                    modified_value = re.sub("data: ", "", value)  # Remove the "data: " prefix from the stream

                    if modified_value and "[DONE]" not in modified_value:
                        # Parse the received chunk of data
                        json_modified_value = json.loads(modified_value)
                        try:
                            # Check if content exists in the response chunk and append it to the final text
                            if json_modified_value["choices"][0]["delta"]["content"] is not None:
                                if stream:
                                    print(json_modified_value["choices"][0]["delta"]["content"], end="")  # Stream the content
                                streaming_text += json_modified_value["choices"][0]["delta"]["content"]  # Append content
                        except:
                            continue  # Ignore any parsing errors and continue to the next chunk

                # Return the fully concatenated response text
                return streaming_text
            
            except Exception as e:
                # Catch and return any exceptions that occur during the request or processing
                return e

    class TextToImage:
        """
        Text-to-image AI models are a powerful technology that can generate images based on textual descriptions, making them an essential tool for content creation, assistive technology, entertainment, and education.

        The text description is first processed by a natural language processing (NLP) model, which extracts relevant features and keywords. This information is then passed to a generative model, which uses trained parameters to generate an image that matches the textual description. This innovative technology has the potential to transform visual content creation, making it more accessible and user-friendly.

        For marketing and advertising professionals, text-to-image AI models can help create images that are tailored to specific campaigns or target audiences. Visually impaired individuals can use these models to better understand and interact with their environment, making them a valuable assistive technology. The entertainment industry can use text-to-image models to generate images for video games, virtual reality, and other immersive experiences. Finally, educators can use text-to-image models to create interactive diagrams, charts, and other resources to help students better understand complex concepts.

        # Example
            >>> if __name__=="__main__":
            >>> ai = TextToImage()
            >>> Model = "FLUX-1-dev"
            >>> print(ai.generate(prompt="generate an image of a dog sitting on a table with its puppies", model=Model, num_images=4, image_size="512x512", bearer_token="Bearer jwt:eyxxxY", prints=True))
        
        For more information visit: https://deepinfra.com/models/text-to-image
        """
        def list_available_models(self) -> str:
            """List all available models with their Documentations."""
            print("Available Models:\n")
        
            Available_Models = {
                "FLUX-1-dev":"FLUX.1-dev is a state-of-the-art 12 billion parameter rectified flow transformer developed by Black Forest Labs. This model excels in text-to-image generation, providing highly accurate and detailed outputs. It is particularly well-regarded for its ability to follow complex prompts and generate anatomically accurate images, especially with challenging details like hands and faces.\nFor more information visit: https://deepinfra.com/black-forest-labs/FLUX-1-dev",
                
                "FLUX-1-schnell":"FLUX.1 [schnell] is a 12 billion parameter rectified flow transformer capable of generating images from text descriptions. This model offers cutting-edge output quality and competitive prompt following, matching the performance of closed source alternatives. Trained using latent adversarial diffusion distillation, FLUX.1 [schnell] can generate high-quality images in only 1 to 4 steps.\nFor more information visit: https://deepinfra.com/black-forest-labs/FLUX-1-schnell",
                
                "Stable-diffusion-v1-4":"Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given any text input.\nFor more information visit: https://deepinfra.com/CompVis/stable-diffusion-v1-4",

                "Deliberate":"The Deliberate Model allows for the creation of anything desired, with the potential for better results as the user's knowledge and detail in the prompt increase. The model is ideal for meticulous anatomy artists, creative prompt writers, art designers, and those seeking explicit content.\nFor more information visit: https://deepinfra.com/XpucT/Deliberate",

                "Openjourney":"Text to image model based on Stable Diffusion.\nFor more information visit: https://deepinfra.com/prompthero/openjourney",

                "Stable-diffusion-v1-5":"Most widely used version of Stable Diffusion. Trained on 512x512 images, it can generate realistic images given text description\nFor more information visit: https://deepinfra.com/runwayml/stable-diffusion-v1-5",
                
                "Sdxl":"SDXL consists of an ensemble of experts pipeline for latent diffusion: In a first step, the base model is used to generate (noisy) latents, which are then further processed with a refinement model (available here: https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/) specialized for the final denoising steps. Note that the base model can be used as a standalone module.\nFor more information visit: https://deepinfra.com/stability-ai/sdxl",
                
                "Sdxl-turbo":"The SDXL Turbo model, developed by Stability AI, is an optimized, fast text-to-image generative model. It is a distilled version of SDXL 1.0, leveraging Adversarial Diffusion Distillation (ADD) to generate high-quality images in less steps.\nFor more information visit: https://deepinfra.com/stabilityai/sdxl-turbo",
                
                "Stable-diffusion-2-1":"Stable Diffusion is a latent text-to-image diffusion model. Generate realistic images given text description\nFor more information visit: https://deepinfra.com/stabilityai/stable-diffusion-2-1"
                
            }

            for model_name, model_documentation in Available_Models.items():
                print(f"{model_name} : {model_documentation}\n")
            return 'You Can Use any Model by giving its name in generate function like: generate(prompt="generate an image of a dog sitting on a table with its puppies", model="FLUX-1-dev", bearer_token="Bearer jwt:eyxxxY")'
        
        def generate(
            self,
            prompt:str, 
            bearer_token:str, 
            model:str, 
            negative_prompt:str = None, 
            num_images:int = 4, 
            guidance_scale: float = 7.5, 
            strength:float = None, 
            image_size:str = "512x512", 
            upload_image_path:str = None, 
            mask_image:str = None, 
            refine:str = None, 
            High_Noise_Frac:float = None, 
            apply_watermark:str = None, 
            image_filename_prefix:str = "output_image", 
            prints:bool = True
            ) -> str:
            """
            Generates images using the selected AI model with optional parameters for fine-tuning the output.

            # Args
                - prompt (str): The text prompt to guide image generation.
                - bearer_token (str): The API bearer token for authorization.
                - model (str): The model to use for generation (e.g., 'FLUX-1-dev', 'Stable-diffusion-v1-4').
                - negative_prompt (str, optional): Text to influence the model to avoid certain concepts.
                - num_images (int, optional): The number of images to generate. Default is 4, can be between 1 and 4.
                - guidance_scale (float, optional): How much the model should focus on the prompt (higher means - more focused). Default is 7.5.
                - strength (float, optional): How much to follow an uploaded image. Ranges from 0 to 1 (1 means ignore the image).
                - image_size (str, optional): Desired image size, must be one of predefined values (default is '512x512').
                - upload_image_path (str, optional): Path to an image to guide the generation process.
                - mask_image (str, optional): Path to an image mask for inpainting tasks.
                - refine (str, optional): Refiner option, can be 'no_refiner', 'expert_ensemble_refiner', or 'base_image_refiner'.
                - High_Noise_Frac (float, optional): Noise fraction for 'expert_ensemble_refiner'. Range: 0 to 1.
                - apply_watermark (str, optional): Whether to apply watermark ('yes' or 'no').
                - image_filename_prefix (str, optional): Prefix for the output image filenames. Default is 'output_image'.
                - prints (bool, optional): Whether to print internal information and debug logs. Default is True.

            # Returns
                - str: A success message indicating image file saving, or an error message if something went wrong.

            # Example
                ```python
                result = generate(
                    prompt="A futuristic city skyline", 
                    bearer_token="Bearer my_token", 
                    model="FLUX-1-dev", 
                    num_images=2, 
                    image_size="512x512"
                    )
                print(result)
                ```
                
            # Notes
            - If the model does not support certain parameters, the function will return an error specifying the unsupported parameters.
            - Ensure the `bearer_token` is valid and includes the "Bearer" prefix.
            - Images are saved as .jpg files in the current working directory with names like "output_image-1.jpg", "output_image-2.jpg", etc.
            """
            # Define supported parameters for each model  
            model_parameters = {
                "FLUX-1-dev": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token"],
                "FLUX-1-schnell": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token"],
                "Stable-diffusion-v1-4": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                                        "negative_prompt", "upload_image_path", "strength"],
                "Deliberate": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                            "negative_prompt", "upload_image_path", "strength"],
                "Openjourney": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                                "negative_prompt", "upload_image_path", "strength"],
                "Stable-diffusion-v1-5": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                                        "negative_prompt", "upload_image_path", "strength"],
                "Sdxl": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                        "negative_prompt", "upload_image_path", "strength", "mask_image", "refine", 
                        "High_Noise_Frac", "apply_watermark"],
                "Sdxl-turbo": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token"],
                "Stable-diffusion-2-1": ["prompt", "num_images", "guidance_scale", "height", "width", "bearer_token", 
                                        "negative_prompt", "upload_image_path", "strength"],
            }

            Available_Models = {
                "FLUX-1-dev":"black-forest-labs/FLUX-1-dev",
                "FLUX-1-schnell":"black-forest-labs/FLUX-1-schnell",
                "Stable-diffusion-v1-4":"CompVis/stable-diffusion-v1-4",
                "Deliberate":"XpucT/Deliberate",
                "Openjourney":"prompthero/openjourney",
                "Stable-diffusion-v1-5":"runwayml/Stable-diffusion-v1-5",
                "Sdxl":"stability-ai/sdxl",
                "Sdxl-turbo":"stabilityai/sdxl-turbo",
                "Stable-diffusion-2-1":"stabilityai/stable-diffusion-2-1"
            }

            # Predefined image sizes with width and height in pixels
            image_sizes = {
                "128x128": {"width": 128, "height": 128},
                "256x256": {"width": 256, "height": 256},
                "384x384": {"width": 384, "height": 384},
                "448x448": {"width": 448, "height": 448},
                "512x512": {"width": 512, "height": 512},
                "576x576": {"width": 576, "height": 576},
                "640x640": {"width": 640, "height": 640},
                "704x704": {"width": 704, "height": 704},
                "768x768": {"width": 768, "height": 768},
                "832x832": {"width": 832, "height": 832},
                "896x896": {"width": 896, "height": 896},
                "960x960": {"width": 960, "height": 960},
                "1024x1024": {"width": 1024, "height": 1024}
            }
            
            # Validate if the chosen model is supported
            if model not in Available_Models.keys():
                available_models = ', '.join(Available_Models.keys())
                return f"Model Name '{model}' is not valid. Please select a valid model.\nAvailable models are: {available_models}"
            model_value = Available_Models[model]
            
            # Validate the image size; return error if invalid
            if image_size not in image_sizes:
                available_sizes = ', '.join(image_sizes.keys())
                return f"Image size '{image_size}' is not valid. Please select a valid size from: {available_sizes}"

            # Extract width and height for the selected image size
            width = image_sizes[image_size]['width']
            height = image_sizes[image_size]['height']

            # Supported parameters for the current model
            supported_params = model_parameters[model]

            # Build the payload dynamically based on supported parameters
            payload = {}
            params = {
                "prompt": prompt,
                "num_images": num_images,
                "guidance_scale": guidance_scale,
                "width": width,
                "height": height,
                "bearer_token": bearer_token,
                "negative_prompt": negative_prompt,
                "upload_image_path": upload_image_path,
                "strength": strength,
                "mask_image": mask_image,
                "refine": refine,
                "High_Noise_Frac": High_Noise_Frac,
                "apply_watermark": apply_watermark,
            }

            # Add supported parameters to payload
            for param, value in params.items():
                if param in supported_params:
                    payload[param] = value
                    if value is None:return f"{param} is required parameter and it should not be None."
                elif value is not None:
                    return f"Model {model} does not support parameter '{param}'."

            # Validate constraints on num_images
            if num_images not in [1,2,3,4]:
                return "num_images is the number of images to generate (Default: 1, 1 ≤ num_images ≤ 4)"
            
            # Validate guidance_scale
            if not (1 <= guidance_scale <= 20):
                return "guidance_scale is the scale of classifier-free guidance, higher means follow prompt more closely (Default: 7.5, 1 ≤ guidance_scale ≤ 20)"
            
            # Validate strength (if provided)
            if strength is not None and not 0 <= strength <= 1:
                return "strength is how much to follow the input image. 1 means ignore the image, 0 means follow the image exactly (Default: 0.8, 0 ≤ strength ≤ 1)"
            
            # Validate image path existence (if provided)
            if upload_image_path is not None and not os.path.exists(upload_image_path):
                return "upload_image_path must be a valid file path."
            
            # Validate mask image existence (if provided)
            if mask_image is not None and not os.path.exists(mask_image):
                return "mask_image must be a valid file path."
            
            # Validate refine (if provided)
            if refine is not None and refine not in ["no_refiner", "expert_ensemble_refiner", "base_image_refiner"]:
                return "refine must be either 'no_refiner', 'expert_ensemble_refiner', or 'base_image_refiner'."
            
            # Validate High_Noise_Frac (if provided)
            if High_Noise_Frac is not None and not 0 <= High_Noise_Frac <= 1:
                return "High_Noise_Frac is for expert_ensemble_refiner, the fraction of noise to use (Default: 0.8, 0 ≤ high_noise_frac ≤ 1)"
            
            # Validate apply_watermark (if provided)
            if apply_watermark is not None and str(apply_watermark).lower() not in ["yes", "no"]:
                return "apply_watermark must be either 'yes' or 'no'."
            
            # Make the API request to DeepInfra
            url = f"https://api.deepinfra.com/v1/inference/{model_value}"

            # Prepare the headers for the API request
            headers = {"Accept": "text/event-stream","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.9,hi;q=0.8","Authorization": f"Bearer {bearer_token.replace('Bearer ', '')}","Connection": "keep-alive","Content-Type": "application/json","Dnt": "1","Host": "api.deepinfra.com","Origin": "https://deepinfra.com","Referer": "https://deepinfra.com/","Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": f"{random.choice(UserAgents)}","X-Deepinfra-Source": "web-page"}
            try:
                # Convert payload to JSON
                response = requests.request("POST", url, headers=headers, data=json.dumps(payload), timeout=None)

                # Parse the API response as JSON
                json_response = json.loads(response.content)

                if response.status_code == 200:
                    # Process each image in the response and save it to the file system
                    for idx, image_data in enumerate(json_response.get('images', [])):
                        try:
                            # Extract and decode base64-encoded image data
                            base64_image_data = image_data.split(",")[1]
                            image_data = base64.b64decode(base64_image_data)
                            
                            # Define the filename for the saved image
                            image_filename = f"{image_filename_prefix}-{idx+1}.jpg"
                            
                            # Save the image as a .jpg file
                            with open(image_filename, "wb") as f:
                                f.write(image_data)
                            
                            # Optionally print a success message for each saved image
                            if prints:
                                print(f"Image saved successfully as {image_filename}\n")
                        except Exception as e:
                            print(f"Failed to save image {idx+1}: {e}")

                    # Return success message
                    return "All images saved successfully.\n"
                else:
                    # Return the error details from the API response
                    return f'Error: {json_response["detail"]["error"]}'
            except Exception as E:return E

    class AutomaticSpeechRecognition:
        """
        Automatic Speech Recognition (ASR) AI models are a critical component of many modern applications, including virtual assistants, dictation software, and transcription services. These models use machine learning techniques to transcribe spoken language into written text, enabling computers to understand and respond to spoken commands.

        There are many different types of ASR models, each with its own strengths and weaknesses. Traditional models include hidden Markov models (HMMs) and Gaussian mixture models (GMMs), while more recent models use deep learning techniques such as recurrent neural networks (RNNs), long short-term memory networks (LSTMs), convolutional neural networks (CNNs), and transformers.

        While ASR models have made significant progress in recent years, they still face challenges in noisy environments, with multiple speakers, and with accented or non-standard speech. Nevertheless, they are becoming increasingly accurate and versatile, enabling new and exciting applications in areas such as healthcare, education, and entertainment.
        
        # Example
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().AutomaticSpeechRecognition()
            >>> audio_file_path = "path/to/your/audio/file.mp3"
            >>> Model = "Whisper-large-v3"
            >>> print(ai.generate(audio_file_path=audio_file_path, model=Model))
            >>> print(ai.generate(audio_file_path=audio_file_path, model=Model, stream=True))
            
        For more information visit: https://deepinfra.com/models/automatic-speech-recognition
        """
        def list_available_models(self) -> str:
            """
            List all available models with their Documentations.
            
            >>> Example
                >>> ai = DeepInfra().AutomaticSpeechRecognition()
                >>> print(ai.list_available_models())

            This will print a list of all the available models and their descriptions.
            """
            print("Available Models:\n")
            Available_Models = {

                "Whisper-tiny":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. It was trained on 680k hours of labelled data and demonstrates a strong ability to generalize to many datasets and domains without fine-tuning. Whisper is a Transformer-based encoder-decoder model trained on English-only or multilingual data. The English-only models were trained on speech recognition, while the multilingual models were trained on both speech recognition and machine translation.\nFor more information visit: https://deepinfra.com/openai/whisper-tiny\n",

                "Whisper-tiny.en":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation, trained on 680k hours of labeled data without fine-tuning. It's a Transformer based encoder-decoder model, trained on English-only or multilingual data, predicting transcriptions in the same or different language as the audio. Whisper checkpoints come in five configurations of varying model sizes.\nFor more information visit: https://deepinfra.com/openai/whisper-tiny.en\n",

                "Whisper-base":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. It was trained on 680k hours of labelled data and demonstrates a strong ability to generalize to many datasets and domains without fine-tuning. The model is based on a Transformer encoder-decoder architecture. Whisper models are available for various languages including English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, and many more.\nFor more information visit: https://deepinfra.com/openai/whisper-base\n",

                "Whisper-base.en":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. It was trained on 680k hours of labelled data and demonstrated a strong ability to generalise to many datasets and domains without fine-tuning. Whisper checks pens are available in five configurations of varying model sizes, including a smallest configuration trained on English-only data and a largest configuration trained on multilingual data. This one is English-only.\nFor more information visit: https://deepinfra.com/openai/whisper-base.en\n",

                "Whisper-small":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. It was trained on 680k hours of labelled data and demonstrates a strong ability to generalize to many datasets and domains without the need for fine-tuning. The model is based on a Transformer architecture and uses a large-scale weak supervision technique.\nFor more information visit: https://deepinfra.com/openai/whisper-small\n",

                "Whisper-small.en":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation, trained on 680k hours of labelled data without the need for fine-tuning. It is a Transformer based encoder-decoder model, trained on either English-only or multilingual data, and is available in five configurations of varying model sizes. The models were trained on the tasks of speech recognition and speech translation, predicting transcriptions in the same or different languages as the audio.\nFor more information visit: https://deepinfra.com/openai/whisper-small.en\n",

                "Whisper-medium":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. It was trained on 680k hours of labeled data and demonstrates strong abilities to generalize to various datasets and domains without fine-tuning. The model is based on a Transformer encoder-decoder architecture.\nFor more information visit: https://deepinfra.com/openai/whisper-medium\n",

                "Whisper-medium.en":"Whisper is a pre-trained model for automatic speech recognition (ASR) and speech translation. Trained on 680k hours of labelled data, Whisper models demonstrate a strong ability to generalise to many datasets and domains without fine-tuning. The primary intended users of these models are AI researchers studying robustness, generalisation, and capabilities of the current model.\nFor more information visit: https://deepinfra.com/openai/whisper-medium.en\n",

                "Whisper-large":"Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification.\nFor more information visit: https://deepinfra.com/openai/whisper-large\n",
                
                "Whisper-large-v3":"Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification.\nFor more information visit: https://deepinfra.com/openai/whisper-large-v3\n",

                "Whisper-timestamped-medium":"Whisper is a set of multi-lingual, robust speech recognition models trained by OpenAI that achieve state-of-the-art results in many languages. Whisper models were trained to predict approximate timestamps on speech segments (most of the time with 1-second accuracy), but they cannot originally predict word timestamps. This version has implementation to predict word timestamps and provide a more accurate estimation of speech segments when transcribing with Whisper models.\nFor more information visit: https://deepinfra.com/openai/whisper-timestamped-medium\n",

                "Whisper-timestamped-medium.en":"Whisper is a set of multi-lingual, robust speech recognition models trained by OpenAI that achieve state-of-the-art results in many languages. Whisper models were trained to predict approximate timestamps on speech segments (most of the time with 1-second accuracy), but they cannot originally predict word timestamps. This variant contains implementation to predict word timestamps and provide a more accurate estimation of speech segments when transcribing with Whisper models.\nFor more information visit: https://deepinfra.com/openai/whisper-timestamped-medium.en\n",

                "Distil-large-v3":"Distil-Whisper was proposed in the paper Robust Knowledge Distillation via Large-Scale Pseudo Labelling. This is the third and final installment of the Distil-Whisper English series. It the knowledge distilled version of OpenAI's Whisper large-v3, the latest and most performant Whisper model to date. Compared to previous Distil-Whisper models, the distillation procedure for distil-large-v3 has been adapted to give superior long-form transcription accuracy with OpenAI's sequential long-form algorithm.\nFor more information visit: https://deepinfra.com/distil-whisper/distil-large-v3\n",

            }
            for model_name, model_documentation in Available_Models.items():
                print(f"{model_name} : {model_documentation}")
            return 'You Can Use any Model by giving its name in generate function like: generate(audio_file_path="./Test_Data/English.mp3", task="transcribe", model="Whisper-large-v3")'
        
        def generate(
            self,
            audio_file_path: str = "path/to/your/audio/file.mp3",
            task:str = "transcribe",
            model:str = "Whisper-large-v3",
            stream:bool = False
            ) -> str:
            """
            Generates a text transcript from the given audio file using the specified model.

            Args
                audio_file_path (str): The path to the audio file to transcribe. Defaults to None.
                task (str): The task to perform. Can be either "transcribe" or "translate". Defaults to "transcribe".
                model (str): The name of the model to use from the Available_Models dictionary. Defaults to "Whisper-large-v3".
                stream (bool): If True, the response will be printed in real-time as it streams. Defaults to False.

            Returns
                str: The generated text transcript from the given audio file.

            # Example
                >>> if __name__=="__main__":
                >>> ai = DeepInfra().AutomaticSpeechRecognition()
                >>> query = "path/to/your/audio/file.mp3"
                >>> Model = "Whisper-large-v3"
                >>> print(ai.generate(audio_file_path=query, model=Model))
                >>> print(ai.generate(audio_file_path=query, model=Model, stream=True))
            """
            Models = {
                "Whisper-large-v3":"openai/whisper-large-v3",

                "Distil-large-v3":"distil-whisper/distil-large-v3",

                "Whisper-base":"openai/whisper-base",

                "Whisper-base.en":"openai/whisper-base.en",

                "Whisper-large":"openai/whisper-large",

                "Whisper-medium":"openai/whisper-medium",

                "Whisper-medium.en":"openai/whisper-medium.en",

                "Whisper-small":"openai/whisper-small",

                "Whisper-small.en":"openai/whisper-small.en",

                "Whisper-timestamped-medium":"openai/whisper-timestamped-medium",

                "Whisper-timestamped-medium.en":"openai/whisper-timestamped-medium.en",

                "Whisper-tiny":"openai/whisper-tiny",

                "Whisper-tiny.en":"openai/whisper-tiny.en",

            }
            if audio_file_path is None:return "Please Provide a Valid audio file path"
            try:
                with open(audio_file_path, "rb") as audio_file:
                    audio_data = audio_file.read()
                base64_data = base64.b64encode(audio_data).decode('utf-8')
            except Exception as e:return e

            # Validate model to ensure it is in the Models dict
            if model not in Models:
                available_models = ',\n'.join(Models.keys())
                return f"Model key '{model}' is not valid. Please select a valid model.\nAvailable models are: {available_models}"

            model_value = Models[model]
            
            # Validate the task to ensure it is either "transcribe" or "translate"
            if str(task).lower() not in ["transcribe", "translate"]:
                return "Please Choose a Valid Task Either Transcribe or Translate"

            url = f"https://api.deepinfra.com/v1/inference/{model_value}"
            payload = json.dumps({
            "audio": f"data:audio/mpeg;base64,{base64_data}",
            "task": task
            })

            # Prepare the headers for the API request
            headers = {"Accept": "text/event-stream","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.9,hi;q=0.8","Connection": "keep-alive","Content-Type": "application/json","Dnt": "1","Host": "api.deepinfra.com","Origin": "https://deepinfra.com","Referer": "https://deepinfra.com/","Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": f"{random.choice(UserAgents)}","X-Deepinfra-Source": "web-page"}

            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=None)
                if response.status_code==200:
                    response_data = json.loads(response.content)
                    if stream:
                        for value in response_data["segments"]:
                            print(value["text"], end="") # Stream the text
                    return str(response_data["text"]).strip()
                else:return response.content
            except Exception as e:return e

    class TextToSpeech:
        """
        Converts input text into speech using DeepInfra API's Text-to-Speech service.
        Text-to-Speech (TTS) technology converts written text into spoken words using advanced speech synthesis. TTS systems are used in applications like virtual assistants, accessibility tools for visually impaired users, and language learning software, enabling seamless human-computer interaction.

        # Example
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().TextToSpeech()
            >>> Text = "Hello, How are you?"
            >>> Voice = "Aura"
            >>> print(ai.generate(text=Text,voice=Voice,output_filename="output_file.mp3")

        For more information visit: https://deepinfra.com/deepinfra/tts
        """
        def list_available_models(self) -> str:
            """List all available voice models with their Documentations."""
            print("Available Voices:\n")
        
            Available_Voices = {
                "Quartz":"Quartz is a popular voice model developed by DeepInfra. Quartz can be used in various applications, such as virtual assistants, accessibility tools for visually impaired users, and language learning software, enabling seamless human-computer interaction.\n",
                "Aura":"Aura is a popular voice model developed by DeepInfra. Aura is a soothing and articulate female voice. It brings a calm and composed presence, ideal for meditation apps, relaxation content, or any scenario where a peaceful and reassuring voice is needed. Aura provides a smooth listening experience for users.\n",
                "Luna":"Luna is a popular voice model developed by DeepInfra. Luna is a warm, clear, and expressive female voice designed to sound friendly and engaging. This voice is ideal for applications that require a gentle and approachable tone, making it perfect for conversational interfaces, educational tools, and customer service.\n"
            }

            for voice_name, voice_documentation in Available_Voices.items():
                print(f"{voice_name} : {voice_documentation}")
            return 'You Can Use any Voice by giving its name and text in generate function like: generate(text="Text-to-Speech technology converts written text into spoken words using advanced speech synthesis by the DeepInfra API.",voice="Aura",output_filename="output_file.mp3")'
        
        def generate(
            self,
            text:str = "Text-to-Speech technology converts written text into spoken words using advanced speech synthesis by the DeepInfra API.",
            voice:str = "Aura",
            output_filename:str = "output_file.mp3"
            ) -> str:
            """
            Converts input text into speech using DeepInfra API's Text-to-Speech service.

            # Args:
                text (str): The input text to be converted into speech. Defaults to a sample text about Text-to-Speech technology.
                voice (str): The name of the preset voice to be used for the speech. 
                            Valid options are: "Quartz", "Aura", and "Luna". Defaults to "Aura".
                output_filename (str): The name of the output MP3 file where the synthesized speech will be saved. Defaults to "output_file.mp3".

            # Returns:
                str: A success message indicating the name of the saved audio file or an error message if an invalid voice is selected or an API error occurs.

            # Raises:
                None, but in case of an invalid voice key, the function returns a message listing available voices.

            # API:
                The function sends a POST request to the DeepInfra API endpoint:
                URL: "https://api.deepinfra.com/v1/inference/deepinfra/tts"
                
            # Steps:
                1. Validates the voice key provided by the user. If the key is invalid, it returns a message listing available voices.
                2. Sends a POST request to the DeepInfra Text-to-Speech API with the input text, selected voice, and preset speech speed.
                3. The API responds with Base64-encoded audio data.
                4. Decodes the Base64 audio data and writes it to the specified MP3 file.
                5. Returns a success message once the audio file is saved.

            # Note:
                For more information, you can visit https://deepinfra.com/models
            """
            url = "https://api.deepinfra.com/v1/inference/deepinfra/tts"
            Voices = {"Quartz":"quartz", "Aura":"aura", "Luna":"luna"}
            if voice not in Voices:
                available_voices = ', '.join(Voices.keys())
                return f"Voice key '{voice}' is not valid. Please select a valid Voice.\nAvailable Voices are: {available_voices}"
            voice_value = Voices[voice]
            payload = json.dumps({"text": text,"preset_voice": voice_value,"speed": 1})
            
            # Prepare the headers for the API request
            headers = {"Accept": "text/event-stream","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.9,hi;q=0.8","Connection": "keep-alive","Content-Type": "application/json","Dnt": "1","Host": "api.deepinfra.com","Origin": "https://deepinfra.com","Referer": "https://deepinfra.com/","Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": f"{random.choice(UserAgents)}","X-Deepinfra-Source": "web-page"}

            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=None)
                if response.status_code == 200:
                    response_data = json.loads(response.content)
                    audio_data = response_data["audio"].split(",")[1]
                    audio_binary = base64.b64decode(audio_data)
                    with open(output_filename, "wb") as audio_file:
                        audio_file.write(audio_binary)
                    return f"Audio File Saved Successfully as {output_filename}"
                else:return response.content
            except Exception as E:return E

    class ZeroShotImageClassification:
        """
        Zero-shot image classification is a powerful technique in machine learning that allows you to classify images into categories that a model has never seen before during training. This is especially useful for image classification tasks where obtaining labeled training data for every possible category is difficult or expensive. This is often the case in a variety of industries, such as healthcare, manufacturing, and e-commerce.

        To build a zero-shot image classification model, you can use a technique called transfer learning, where a pre-trained model is fine-tuned on a smaller dataset with specific categories. The pre-trained model is typically trained on a large dataset of images with generic labels, such as ImageNet, which contains over a million images labeled with 1000 categories.

        During the fine-tuning process, the model learns to recognize visual features that are common across different categories, such as shapes, textures, and colors. To make zero-shot predictions, the model uses a set of attributes or features that are associated with each category.

        However, it's important to note that zero-shot models can sometimes struggle with fine-grained distinctions between similar categories, and may require additional training data to improve their accuracy. In these cases, you may want to consider using semi-supervised or unsupervised learning techniques to augment your zero-shot model with additional labeled or unlabeled data.
        
        # Example
            >>> if __name__=="__main__":
            >>> ai = DeepInfra().ZeroShotImageClassification()
            >>> Model = "Clip-vit-base-patch32"
            >>> print(ai.generate(image_path="dog.jpg", model=Model, bearer_token="Bearer jwt:eyxxxY"))

        For more information visit: https://deepinfra.com/models/zero-shot-image-classification
        """
        def list_available_models(self) -> str:
            """List all available models with their Documentations."""
            print("Available Models:\n")
            Available_Models = {
                "Clip-vit-base-patch32":"The CLIP model was developed by OpenAI to investigate the robustness of computer vision models. It uses a Vision Transformer architecture and was trained on a large dataset of image-caption pairs. The model shows promise in various computer vision tasks but also has limitations, including difficulties with fine-grained classification and potential biases in certain applications.\nFor more information visit: https://deepinfra.com/openai/clip-vit-base-patch32\n",
                "Clip-vit-large-patch14-336":"A zero-shot-image-classification model released by OpenAI. The clip-vit-large-patch14-336 model was trained from scratch on an unknown dataset and achieves unspecified results on the evaluation set. The model's intended uses and limitations, as well as its training and evaluation data, are not provided. The training procedure used an unknown optimizer and precision, and the framework versions included Transformers 4.21.3, TensorFlow 2.8.2, and Tokenizers 0.12.1.\nFor more information visit: https://deepinfra.com/openai/clip-vit-large-patch14-336\n"
            }
            for model_name, model_documentation in Available_Models.items():
                print(f"{model_name} : {model_documentation}")
            return 'You Can Use any Model by giving its name in generate function like: generate(image_path="dog.jpg", model=Model, bearer_token="Bearer jwt:eyxxxY")'
        
        def generate(
            self,
            image_path: str = "your_image_path",
            model:str = "Clip-vit-base-patch32",
            bearer_token: str = "your_bearer_token", 
            candidate_labels: list = ["cat", "dog"]
            ) -> dict:
            
            """
            Generates zero-shot-image-classification results using the specified model.

            Args:
                image_path (str): The path to the image file to classify. Defaults to "your_image_path".
                model (str): The name of the model to use from the Available_Models dictionary. Defaults to "Clip-vit-base-patch32".
                bearer_token (str): The DeepInfra API bearer token for authentication. Defaults to "your_bearer_token".
                candidate_labels (list): A list of strings containing the candidate labels for classification. Defaults to ["cat", "dog"].
                
            Returns:
                dict: A dict containing the classification results. If the request fails, contains the error detail as a string.
            """
            Models = {
                "Clip-vit-base-patch32":"openai/clip-vit-base-patch32",
                "Clip-vit-large-patch14-336":"openai/clip-vit-large-patch14-336"
            }
            try:
                # Validate model to ensure it is in the Models dict
                if model not in Models:
                    available_models = ',\n'.join(Models.keys())
                    return f"Model key '{model}' is not valid. Please select a valid model.\nAvailable models are: {available_models}"

                model_value = Models[model]

                # URL for the DeepInfra API endpoint for the CLIP ViT-B/32 model
                url = f"https://api.deepinfra.com/v1/inference/{model_value}"

                # Open the image file in binary mode and encode it to base64 format
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    base64_string = f"data:image/jpeg;base64,{encoded_string}"

                # Prepare the payload with the base64 image and the candidate labels
                payload = json.dumps({"image": base64_string, "candidate_labels": candidate_labels})
                
                # Prepare the headers for the API request
                headers = {"Accept": "text/event-stream","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "en-US,en;q=0.9,hi;q=0.8","Authorization": f"Bearer {bearer_token.replace('Bearer ', '')}","Connection": "keep-alive","Content-Type": "application/json","Dnt": "1","Host": "api.deepinfra.com","Origin": "https://deepinfra.com","Referer": "https://deepinfra.com/","Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","Sec-Ch-Ua-Mobile": "?0","Sec-Ch-Ua-Platform": "\"Windows\"","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": f"{random.choice(UserAgents)}","X-Deepinfra-Source": "web-page"}
                    
                # Make the POST request to the API with the prepared payload and headers
                response = requests.request("POST", url, headers=headers, data=payload, timeout=None)

                # Parse the response data from JSON
                response_data = json.loads(response.content)

                # If the response status is 200 (success), return the classification results
                if response.status_code == 200:
                    return {"results": f'{response_data["results"]}'}
                else:
                    # If the request fails, return the error detail from the response
                    return {'error': f'{response_data["detail"]}'}
            
            except Exception as E:
                # Return the exception message in case of any errors
                return {'error': f'{E}'}

if __name__=="__main__":...