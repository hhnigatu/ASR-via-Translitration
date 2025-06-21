# Exploring Transliteration-Based Zero-Shot Transfer for Amharic ASR
Hellina Hailu Nigatu and Hanan Aldarmaki. AfricaNLP 2025.

[paper]()
## Abstract
The performance of Automatic Speech Recognition (ASR) depends on the availability of transcribed speech datasets—often scarce or non-existent for many of the world’s languages. This study investigates alternative strategies to bridge the data gap using zero-shot cross-lingual transfer, leveraging transliteration as a method to utilize data from other languages. We experiment with transliteration from various source languages and demonstrate ASR performance in a low-resourced language, Amharic. We find that source data that align with the character distribution of the test data achieve the best performance, regardless of language family. We also experiment with fine-tuning with minimal transcribed data in the target language. Our findings demonstrate that transliteration, particularly when combined with a strategic choice of source languages, is a viable approach for improving ASR in zero-shot and low-resourced settings.

## Models
Links to models trained with transliterated data.

### Multilingual
Models trained with data combined from two languages. Each language has 10k utterances, sampled to match the Arabic dataset.

[Spanish-Arabic](https://huggingface.co/Hellina/es_ar) * [Spanish-Xhosa](https://huggingface.co/Hellina/es_xh)  * [French-Arabic]()   * [French-Xhosa]()   * [French-Spanish]()   * [Arabic-Xhosa]()

### Monolingual
Models trained with data from a single transfer language, with transliterated transcripts.

[Arabic]() * [Xhosa]() * [French](https://huggingface.co/Hellina/fr_only) * [Spanish]()

## Data
The compiled dataset with transliterated transcripts can be found [here](). Below, we present the sources of our training and test data. For ALFFA dataset, we provide the manually reconstructed test transcripts in the Data folder of this repository. 

## Training Data


* **Arabic**:  Kulkarni, A., Kulkarni, A., Shatnawi, S.A.M., Aldarmaki, H. (2023) ClArTTS: An Open-Source Classical Arabic Text-to-Speech Corpus. Proc. Interspeech 2023, 5511-5515, doi: 10.21437/Interspeech.2023-2224
* **Xhosa**:  Nic J. de Vries, Marelie H. Davel, Jaco Badenhorst, Willem D. Basson, Febe de Wet, Etienne Barnard, and Alta de Waal. (2014). A smartphone-based ASR data collection tool for under-resourced languages. Speech Communication.
* **Spanish**: Rosana Ardila, Megan Branson, Kelly Davis, Michael Kohler, Josh Meyer, Michael Henretty, Reuben Morais, Lindsay Saunders, Francis Tyers, and Gregor Weber. 2020. Common voice: A massively-multilingual speech corpus. In Proceedings of the Twelfth Language Resources and Evaluation Conference.
* **French**: Changhan Wang, Morgane Riviere, Ann Lee, Anne Wu, Chaitanya Talnikar, Daniel Haziza, Mary Williamson, Juan Pino, and Emmanuel Dupoux. 2021. VoxPopuli: A large-scale multilingual speech corpus for representation learning, semi-supervised learning and interpretation. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers).

## Test Data
* FLEURS: Conneau, A., Ma, M., Khanuja, S., Zhang, Y., Axelrod, V., Dalmia, S., ...Bapna, A. (2022). FLEURS: Few-shot Learning Evaluation of Universal Representations of Speech. ArXiv e-prints, 2205.12446. Retrieved from https://arxiv.org/abs/2205.12446v1
* ALFFA: Martha Yifiru Tachbelie, Solomon Teferra Abate, and Laurent Besacier. 2014. Using different acoustic, lexical and language modeling units for ASR of an under-resourced language – Amharic. Speech Communication.
* BABEL: M. Gales, K. Knill, A. Ragni, and S. Rath. 2014. Speech recognition and keyword spotting for low-resource languages: Babel project research at CUED. Workshop on Spoken Language Technologies for Underresourced Languages.
