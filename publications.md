# Nicolas Boizard — Publications and Research Timeline

Member of Technical Staff @ Cohere. Canonical page: https://nicolas-bzrd.github.io/

Member of Technical Staff on the pretraining team at Cohere, scaling up model training, and PhD candidate at CentraleSupélec (Université Paris-Saclay), advised by Pierre Colombo and Céline Hudelot, defending in early 2027. PhD research on large-scale training of multilingual and multimodal LLMs, both decoders and encoders (EuroLLM, CroissantLLM, BidirLM-Omni, EuroBERT), and on distillation, such as the Universal Logit Distillation Loss for cross-tokenizer distillation.

---

## BidirLM: From Text to Omnimodal Bidirectional Encoders by Adapting and Composing Causal LLMs

- **Year:** 2026
- **Venue:** COLM 2026
- **Authors:** N Boizard, T Deschamps-Berger, H Gisserot-Boukhlef, C Hudelot, P Colombo
- **Topics:** Main author, Efficient training
- **arXiv:** https://arxiv.org/abs/2604.02045
- **HuggingFace:** https://huggingface.co/BidirLM

**Abstract.** Transforming causal generative language models into bidirectional encoders offers a powerful alternative to BERT-style architectures. However, current approaches remain limited: they lack consensus on optimal training objectives, suffer from catastrophic forgetting at scale, and fail to flexibly integrate the vast ecosystem of specialized generative models. In this work, through systematic ablations on the Gemma3 and Qwen3 families, we identify the key factors driving successful adaptation, highlighting the critical role of an often-omitted prior masking phase. To scale this process without original pre-training data, we introduce a dual strategy combining linear weight merging with a lightweight multi-domain data mixture that mitigates catastrophic forgetting. Finally, we augment our encoders by merging them with specialized causal models, seamlessly transferring modality- and domain-specific capabilities. This open-source recipe, designed for any causal decoder LLM, yields BidirLM, a family of five encoders that outperform alternatives on text, vision, and audio representation benchmarks.

## BERT-as-a-Judge: A Robust Alternative to Lexical Methods for Efficient Reference-Based LLM Evaluation

- **Year:** 2026
- **Venue:** COLM 2026
- **Authors:** H Gisserot-Boukhlef, N Boizard, E Malherbe, C Hudelot, P Colombo
- **Topics:** Efficient training
- **arXiv:** https://arxiv.org/abs/2604.09497
- **HuggingFace:** https://huggingface.co/collections/Nicolas-BZRD/bert-as-a-judge

**Abstract.** Accurate evaluation is central to the large language model (LLM) ecosystem, guiding model selection and downstream adoption across diverse use cases. In practice, however, evaluating generative outputs typically relies on rigid lexical methods to extract and assess answers, which can conflate a model's true problem-solving ability with its compliance with predefined formatting guidelines. While recent LLM-as-a-Judge approaches mitigate this issue by assessing semantic correctness rather than strict structural conformity, they also introduce substantial computational overhead, making evaluation costly. In this work, we first systematically investigate the limitations of lexical evaluation through a large-scale empirical study spanning 36 models and 15 downstream tasks, demonstrating that such methods correlate poorly with human judgments. To address this limitation, we introduce BERT-as-a-Judge, an encoder-driven approach for assessing answer correctness in reference-based generative settings, robust to variations in output phrasing, and requiring only lightweight training on synthetically annotated question-candidate-reference triplets. We show that it consistently outperforms the lexical baseline while matching the performance of much larger LLM judges, providing a compelling tradeoff between the two and enabling reliable, scalable evaluation. Finally, through extensive experimentation, we provide detailed insights into BERT-as-a-Judge's performance to offer practical guidance for practitioners, and release all project artifacts to foster downstream adoption.

## EuroLLM-22B: Technical Report

- **Year:** 2026
- **Venue:** Technical Report
- **Authors:** MM Ramos, DM Alves, H Gisserot-Boukhlef, J Alves, PH Martins, ...
- **Topics:** Large-scale training
- **arXiv:** https://arxiv.org/pdf/2602.05879
- **HuggingFace:** https://huggingface.co/collections/utter-project/eurollm

**Abstract.** This report presents EuroLLM-22B, a large language model trained from scratch to support the needs of European citizens by covering all 24 official European Union languages and 11 additional languages. EuroLLM addresses the issue of European languages being underrepresented and underserved in existing open large language models. We provide a comprehensive overview of EuroLLM-22B's development, including tokenizer design, architectural specifications, data filtering, and training procedures. Across a broad set of multilingual benchmarks, EuroLLM-22B demonstrates strong performance in reasoning, instruction following, and translation, achieving results competitive with models of comparable size. To support future research, we release our base and instruction-tuned models, our multilingual web pretraining data and updated EuroBlocks instruction datasets, as well as our pre-training and evaluation codebases.

## Scale or Reason? A Compute-Equivalent Analysis of Reasoning Distillation

- **Year:** 2025
- **Venue:** EMNLP 2026
- **Authors:** N Boizard, H Gisserot-Boukhlef, K El Haddad, C Hudelot, P Colombo
- **Topics:** Main author, Efficient training
- **arXiv:** https://arxiv.org/abs/2509.22193
- **HuggingFace:** https://huggingface.co/scale-or-reason

**Abstract.** Distilling reasoning traces from strong teacher models has become the standard recipe for building capable small language models. Yet reasoning traces are 5-20× longer than standard instruction fine-tuning (IFT) outputs, meaning every practitioner who chooses reasoning distillation implicitly forgoes training a larger IFT model on the same compute budget. Whether this trade-off is worthwhile remains unaddressed. We study it with a controlled experiment: a single teacher generates paired IFT and reasoning outputs for identical prompts by toggling only its reasoning mode, isolating supervision format as the sole variable. Training students at five scales (0.5B to 14B) and evaluating on 18 benchmarks, we find that at matched FLOPs, IFT lies on or near the Pareto frontier across the majority of configurations. Reasoning reaches the Pareto frontier only on open-ended tasks at 7B and above. Even there, a sequential curriculum mixing just 25-50% reasoning data with IFT captures most of the accuracy benefit at far lower compute cost.

## Should We Still Pretrain Encoders with Masked Language Modeling?

- **Year:** 2025
- **Venue:** ICLR 2026
- **Authors:** H Gisserot-Boukhlef, N Boizard, M Faysse, DM Alves, E Malherbe, ...
- **Topics:** Main author, Efficient training
- **arXiv:** https://arxiv.org/pdf/2507.00994
- **HuggingFace:** https://huggingface.co/MLMvsCLM
- **GitHub:** https://github.com/Nicolas-BZRD/EuroBERT

**Abstract.** Learning high-quality text representations is fundamental to a wide range of NLP tasks. While encoder pretraining has traditionally relied on Masked Language Modeling (MLM), recent evidence suggests that decoder models pretrained with Causal Language Modeling (CLM) can be effectively repurposed as encoders, often surpassing traditional encoders on text representation benchmarks. However, it remains unclear whether these gains reflect an inherent advantage of the CLM objective or arise from confounding factors such as model and data scale. In this paper, we address this question through a series of large-scale, carefully controlled pretraining ablations, training a total of 38 models ranging from 210 million to 1 billion parameters, and conducting over 15,000 fine-tuning and evaluation runs. We find that while training with MLM generally yields better performance across text representation tasks, CLM-trained models are more data-efficient and demonstrate improved fine-tuning stability. Building on these findings, we experimentally show that a biphasic training strategy that sequentially applies CLM and then MLM, achieves optimal performance under a fixed computational training budget. Moreover, we demonstrate that this strategy becomes more appealing when initializing from readily available pretrained CLM models, reducing the computational burden needed to train best-in-class encoder models.

## EuroLLM-9B: Technical Report

- **Year:** 2025
- **Venue:** Technical Report
- **Authors:** PH Martins, J Alves, P Fernandes, NM Guerreiro, R Rei, A Farajian, ...
- **Topics:** Large-scale training
- **arXiv:** https://arxiv.org/pdf/2506.04079
- **HuggingFace:** https://huggingface.co/collections/utter-project/eurollm

**Abstract.** The quality of open-weight LLMs has seen significant improvement, yet they remain predominantly focused on English. In this paper, we introduce the EuroLLM project, aimed at developing a suite of open-weight multilingual LLMs capable of understanding and generating text in all official European Union languages, as well as several additional relevant languages. We outline the progress made to date, detailing our data collection and filtering process, the development of scaling laws, the creation of our multilingual tokenizer, and the data mix and modeling configurations. Additionally, we release our initial models: EuroLLM-1.7B and EuroLLM-1.7B-Instruct and report their performance on multilingual general benchmarks and machine translation.

## EuroBERT: Scaling Multilingual Encoders for European Languages

- **Year:** 2025
- **Venue:** COLM 2025
- **Authors:** N Boizard, H Gisserot-Boukhlef, DM Alves, A Martins, A Hammal, C Corro, ...
- **Topics:** Main author, Large-scale training
- **arXiv:** https://arxiv.org/pdf/2503.05500
- **HuggingFace:** https://huggingface.co/EuroBERT
- **GitHub:** https://github.com/Nicolas-BZRD/EuroBERT

**Abstract.** General-purpose multilingual vector representations, used in retrieval, regression and classification, are traditionally obtained from bidirectional encoder models. Despite their wide applicability, encoders have been recently overshadowed by advances in generative decoder-only models. However, many innovations driving this progress are not inherently tied to decoders. In this paper, we revisit the development of multilingual encoders through the lens of these advances, and introduce EuroBERT, a family of multilingual encoders covering European and widely spoken global languages. Our models outperform existing alternatives across a diverse range of tasks, spanning multilingual capabilities, mathematics, and coding, and natively supporting sequences of up to 8,192 tokens. We also examine the design decisions behind EuroBERT, offering insights into our dataset composition and training pipeline. We publicly release the EuroBERT models, including intermediate training checkpoints, together with our training framework.

## Towards cross-tokenizer distillation: the universal logit distillation loss for LLMs

- **Year:** 2024
- **Venue:** TMLR 2025
- **Authors:** N Boizard, K El Haddad, C Hudelot, P Colombo
- **Topics:** Main author, Efficient training
- **arXiv:** https://arxiv.org/abs/2402.12030
- **HuggingFace:** https://huggingface.co/collections/Nicolas-BZRD/uld-loss-universal-llms-distillation-65cfa07f1e4ed7404502a9eb
- **GitHub:** https://github.com/Nicolas-BZRD/llm-recipes

**Abstract.** Deploying large language models (LLMs) with billions of parameters is often impractical in industrial settings due to constraints like cost, latency, and hardware limitations. Knowledge distillation (KD) provides a solution by compressing the knowledge from large, resource-intensive models into task-specific smaller ones. Various strategies exist, some relying on the text generated by the teacher model, optionally, leveraging its output logits to improve learning. However, these logit-based methods usually require the teacher and student models to share the same tokenizer, which limits their applicability across different model families. In this paper, we propose the Universal Logit Distillation (ULD) loss, which uses optimal transport theory to enable distillation across different architectures and tokenizers. Our results demonstrate that ULD loss effectively facilitates the distillation process, paving the way for a more widespread use of distillation.

## Croissantllm: A truly bilingual french-english language model

- **Year:** 2024
- **Venue:** TMLR 2025
- **Authors:** M Faysse, P Fernandes, N Guerreiro, A Loison, D Alves, C Corro, ...
- **Topics:** Large-scale training
- **arXiv:** https://arxiv.org/abs/2402.00786
- **HuggingFace:** https://huggingface.co/croissantllm

**Abstract.** We introduce CroissantLLM, a 1.3B language model pretrained on a set of 3T English and French tokens, to bring to the research and industrial community a high-performance, fully open-sourced bilingual model that runs swiftly on consumer-grade local hardware. To that end, we pioneer the approach of training an intrinsically bilingual model with a 1:1 English-to-French pretraining data ratio, a custom tokenizer, and bilingual finetuning datasets. We release the training dataset, notably containing a French split with manually curated, high-quality, and varied data sources. To assess performance outside of English, we craft a novel benchmark, FrenchBench, consisting of an array of classification and generation tasks, covering various orthogonal aspects of model performance in the French Language. Additionally, rooted in transparency and to foster further Large Language Model research, we release codebases, and dozens of checkpoints across various model sizes, training data distributions, and training steps, as well as fine-tuned Chat models, and strong translation models. We evaluate our model through the FMTI framework, and validate 81 % of the transparency criteria, far beyond the scores of even most open initiatives. This work enriches the NLP landscape, breaking away from previous English-centric work in order to strengthen our understanding of multilinguality in language models.

## Deep learning-based stereo camera multi-video synchronization

- **Year:** 2023
- **Venue:** ICASSP 2023
- **Authors:** N Boizard, K El Haddad, T Ravet, F Cresson, T Dutoit
- **Topics:** Main author
- **arXiv:** https://arxiv.org/abs/2303.12916

**Abstract.** Stereo vision is essential for many applications. Currently, the synchronization of the streams coming from two cameras is done using mostly hardware. A software-based synchronization method would reduce the cost, weight and size of the entire system and allow for more flexibility when building such systems. With this goal in mind, we present here a comparison of different deep learning-based systems and prove that some are efficient and generalizable enough for such a task. This study paves the way to a production ready software-based video synchronization system.

---

## News and Talks

- **2026** — BidirLM-Omni 2.5B ranks first on MTEB (open source), MIEB, and MAEB — at its size and up to 7B (https://huggingface.co/spaces/mteb/leaderboard)
- **2026** — Invited talks at Cohere and eBay on BidirLM
- **2026** — EuroBERT powers Jina-nano (1st on MTEB) — 1M+ downloads on Hugging Face (https://huggingface.co/jinaai/jina-embeddings-v5-text-nano)
- **2026** — Le Monde Informatique — EuroLLM-22B parie sur un modèle open source et multilingue. (https://www.lemondeinformatique.fr/actualites/lire-eurollm-22b-parie-sur-un-modele-open-source-et-multilingue-98963.html)
- **2026** — Usine Digitale — EuroLLM-22B, le modèle open source porté par un consortium d'acteurs européens. (https://www.usine-digitale.fr/intelligence-artificielle/ia-generative/eurollm-22b-le-modele-open-source-porte-par-un-consortium-dacteurs-europeens.JFLFB5EDDBBOTNGRUAXGHIOB7Q.html)
- **2025** — ULD Loss powers Hugging Face's on-policy distillation framework (https://huggingface.co/spaces/HuggingFaceH4/on-policy-distillation)
- **2025** — EuroBERT reached 300k+ downloads on Hugging Face (https://huggingface.co/EuroBERT)
- **2025** — Invited talk at NVIDIA on EuroBERT & MLM vs CLM
- **2025** — ULD Loss added to the Axolotl training library (https://github.com/axolotl-ai-cloud/axolotl)
- **2025** — Journal du Net — EuroLLM-9B, l'autre IA européenne de référence taillée pour les entreprises. (https://www.journaldunet.com/intelligence-artificielle/1539559-eurollm-9b-l-autre-ia-europeenne-de-reference-taillee-pour-les-entreprises/)
- **2025** — ActuIA — IA et NLP : EuroBert, l'encodeur multilingue au service des langues européennes. (https://www.actuia.com/actualite/ia-et-nlp-eurobert-lencodeur-multilingue-au-service-des-langues-europeennes/)
- **2025** — Heise — AI model BERT learns European: EuroBERT presented. (https://www.heise.de/en/news/AI-model-BERT-learns-European-EuroBERT-presented-10329005.html)
- **2025** — Invited talks at Cohere and Meta Paris on EuroBERT
- **2024** — Usine Nouvelle — CroissantLLM, l'IA générative dédiée à la langue française, utilisable [...] sur PC et smartphone. (https://www.usinenouvelle.com/editorial/croissantllm-l-ia-generative-dediee-la-langue-francaise-utilisable-en-open-source-sur-pc-et-smartphone.N2209739)
- **2024** — Usine Digitale — CroissantLLM, des chercheurs de CentraleSupélec lancent un modèle d'IA open source et bilingue. (https://www.usine-digitale.fr/article/croissantllm-des-chercheurs-de-centralesupelec-lancent-un-modele-d-ia-open-source-et-bilingue.N2209348)

## Profiles

- Google Scholar: https://scholar.google.com/citations?user=B-jY8EkAAAAJ&hl=en
- Hugging Face: https://huggingface.co/Nicolas-BZRD
- X (formerly Twitter): https://x.com/N1colAIs
- GitHub: https://github.com/Nicolas-BZRD
- LinkedIn: https://linkedin.com/in/nicolas-boizard
