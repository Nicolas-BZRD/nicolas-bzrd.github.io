document.addEventListener('DOMContentLoaded', function() {
    const timelineData = [
        {
            date: '2025',
            title: 'Should We Still Pretrain Encoders with Masked Language Modeling?',
            authors: 'H Gisserot-Boukhlef, N Boizard, M Faysse, DM Alves, E Malherbe, ...',
            type: 'main_author large_scale_training efficient_training',
            description: 'Learning high-quality text representations is fundamental to a wide range of NLP tasks. While encoder pretraining has traditionally relied on Masked Language Modeling (MLM), recent evidence suggests that decoder models pretrained with Causal Language Modeling (CLM) can be effectively repurposed as encoders, often surpassing traditional encoders on text representation benchmarks. However, it remains unclear whether these gains reflect an inherent advantage of the CLM objective or arise from confounding factors such as model and data scale. In this paper, we address this question through a series of large-scale, carefully controlled pretraining ablations, training a total of 38 models ranging from 210 million to 1 billion parameters, and conducting over 15,000 fine-tuning and evaluation runs. We find that while training with MLM generally yields better performance across text representation tasks, CLM-trained models are more data-efficient and demonstrate improved fine-tuning stability. Building on these findings, we experimentally show that a biphasic training strategy that sequentially applies CLM and then MLM, achieves optimal performance under a fixed computational training budget. Moreover, we demonstrate that this strategy becomes more appealing when initializing from readily available pretrained CLM models, reducing the computational burden needed to train best-in-class encoder models.',
            conference: 'arXiv preprint',
            logoUrl: 'img/mlmvsclm.webp',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/pdf/2507.00994', icon: 'fas fa-file-pdf' },
                { type: 'HuggingFace', url: 'https://huggingface.co/MLMvsCLM', icon: 'fas fa-robot' },
                { type: 'GitHub', url: 'https://github.com/Nicolas-BZRD/EuroBERT', icon: 'fab fab fa-github' },
            ]
        },
        {
            date: '2025',
            title: 'EuroLLM-9B: Technical Report',
            authors: 'PH Martins, J Alves, P Fernandes, NM Guerreiro, R Rei, A Farajian, ...',
            type: 'paper large_scale_training',
            description: 'The quality of open-weight LLMs has seen significant improvement, yet they remain predominantly focused on English. In this paper, we introduce the EuroLLM project, aimed at developing a suite of open-weight multilingual LLMs capable of understanding and generating text in all official European Union languages, as well as several additional relevant languages. We outline the progress made to date, detailing our data collection and filtering process, the development of scaling laws, the creation of our multilingual tokenizer, and the data mix and modeling configurations. Additionally, we release our initial models: EuroLLM-1.7B and EuroLLM-1.7B-Instruct and report their performance on multilingual general benchmarks and machine translation.',
            conference: 'arXiv preprint',
            logoUrl: 'img/eurollm.png',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/pdf/2506.04079', icon: 'fas fa-file-pdf' },
                { type: 'HuggingFace', url: 'https://huggingface.co/collections/utter-project/eurollm-66b2bd5402f755e41c5d9c6d', icon: 'fas fa-robot' },
            ]
        },
        {
            date: '2025',
            title: 'EuroBERT: Scaling Multilingual Encoders for European Languages',
            authors: 'N Boizard, H Gisserot-Boukhlef, DM Alves, A Martins, A Hammal, C Corro, ...',
            type: 'paper main_author large_scale_training',
            description: 'General-purpose multilingual vector representations, used in retrieval, regression and classification, are traditionally obtained from bidirectional encoder models. Despite their wide applicability, encoders have been recently overshadowed by advances in generative decoder-only models. However, many innovations driving this progress are not inherently tied to decoders. In this paper, we revisit the development of multilingual encoders through the lens of these advances, and introduce EuroBERT, a family of multilingual encoders covering European and widely spoken global languages. Our models outperform existing alternatives across a diverse range of tasks, spanning multilingual capabilities, mathematics, and coding, and natively supporting sequences of up to 8,192 tokens. We also examine the design decisions behind EuroBERT, offering insights into our dataset composition and training pipeline. We publicly release the EuroBERT models, including intermediate training checkpoints, together with our training framework.',
            conference: 'COLM 2025',
            logoUrl: 'img/eurobert.png',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/pdf/2503.05500', icon: 'fas fa-file-pdf' },
                { type: 'HuggingFace', url: 'https://huggingface.co/EuroBERT', icon: 'fas fa-robot' },
                { type: 'GitHub', url: 'https://github.com/Nicolas-BZRD/EuroBERT', icon: 'fab fa-github' },
            ]
        },
        {
            date: '2024',
            title: 'Towards cross-tokenizer distillation: the universal logit distillation loss for LLMs',
            authors: 'N Boizard, KE Haddad, C Hudelot, P Colombo',
            type: 'paper main_author efficient_training',
            description: 'This research explores a universal logit distillation loss for Large Language Models, focusing on cross-tokenizer distillation techniques to improve model efficiency and performance across different tokenization schemes.',
            conference: 'TMLR 2025',
            logoUrl: 'img/uld.png',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/abs/2402.12030', icon: 'fas fa-file-pdf' },
                { type: 'HuggingFace', url: 'https://huggingface.co/collections/Nicolas-BZRD/uld-loss-universal-llms-distillation-65cfa07f1e4ed7404502a9eb', icon: 'fas fa-robot' },
                { type: 'GitHub', url: 'https://github.com/Nicolas-BZRD/llm-recipes', icon: 'fab fa-github' },
            ]
        },
        {
            date: '2024',
            title: 'Croissantllm: A truly bilingual french-english language model',
            authors: 'M Faysse, P Fernandes, N Guerreiro, A Loison, D Alves, C Corro, ...',
            type: 'paper large_scale_training',
            description: 'We introduce CroissantLLM, a 1.3B language model pretrained on a set of 3T English and French tokens, to bring to the research and industrial community a high-performance, fully open-sourced bilingual model that runs swiftly on consumer-grade local hardware. To that end, we pioneer the approach of training an intrinsically bilingual model with a 1:1 English-to-French pretraining data ratio, a custom tokenizer, and bilingual finetuning datasets. We release the training dataset, notably containing a French split with manually curated, high-quality, and varied data sources. To assess performance outside of English, we craft a novel benchmark, FrenchBench, consisting of an array of classification and generation tasks, covering various orthogonal aspects of model performance in the French Language. Additionally, rooted in transparency and to foster further Large Language Model research, we release codebases, and dozens of checkpoints across various model sizes, training data distributions, and training steps, as well as fine-tuned Chat models, and strong translation models. We evaluate our model through the FMTI framework, and validate 81 % of the transparency criteria, far beyond the scores of even most open initiatives. This work enriches the NLP landscape, breaking away from previous English-centric work in order to strengthen our understanding of multilinguality in language models.',
            conference: 'TMLR 2025',
            logoUrl: 'img/croissant.webp',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/abs/2402.00786', icon: 'fas fa-file-pdf' },
                { type: 'HuggingFace', url: 'https://huggingface.co/croissantllm', icon: 'fas fa-robot' },
            ]
        },
        {
            date: '2023',
            title: 'Deep learning-based stereo camera multi-video synchronization',
            authors: 'N Boizard, K El Haddad, T Ravet, F Cresson, T Dutoit',
            type: 'paper main_author',
            description: 'Stereo vision is essential for many applications. Currently, the synchronization of the streams coming from two cameras is done using mostly hardware. A software-based synchronization method would reduce the cost, weight and size of the entire system and allow for more flexibility when building such systems. With this goal in mind, we present here a comparison of different deep learning-based systems and prove that some are efficient and generalizable enough for such a task. This study paves the way to a production ready software-based video synchronization system.',
            conference: 'ICASSP 2023',
            logoUrl: 'img/video.png',
            links: [
                { type: 'arXiv', url: 'https://arxiv.org/abs/2303.12916', icon: 'fas fa-file-pdf' }
            ]
        }
    ];

    const timelineContainer = document.getElementById('timeline-container');

    function renderTimeline(filter = 'all') {
        if (!timelineContainer) return;

        timelineContainer.innerHTML = '';
        const filteredData = filter === 'all'
            ? timelineData
            : timelineData.filter(item => {
                const itemTypes = item.type.split(' ');
                return itemTypes.includes(filter);
            });

        if (filteredData.length === 0) {
            timelineContainer.innerHTML = '<p class="text-gray-500 text-center ml-[-24px]">No items to display for this category.</p>';
            return;
        }

        filteredData.forEach(item => {
            const linksHTML = item.links.map(link => `
                <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center bg-gray-100 hover:bg-blue-100 text-gray-800 hover:text-blue-700 text-sm font-medium py-2 px-4 rounded-lg transition-colors">
                    <i class="fa-fw ${link.icon}" style="font-size: 1em; min-width: 1.2em; text-align: center; margin-right: 0.5rem;"></i>
                    ${link.type}
                </a>
            `).join('');

            const logoSrc = (item.logoUrl && item.logoUrl.startsWith('img/')) ? item.logoUrl : `https://via.placeholder.com/96x96?text=${encodeURIComponent(item.title.substring(0, 5))}`;

            const logoHTML = `
                <div class="w-24 h-24 mb-4 md:mb-0 md:mr-6 flex-shrink-0">
                    <img src="${logoSrc}" alt="${item.conference ? item.conference : item.title} Logo" class="w-full h-full object-cover rounded-lg shadow-md">
                </div>
            `;

            const conferenceHTML = item.conference ? `
                <p class="text-blue-600 font-semibold mb-2">${item.conference}</p>
            ` : '';

            const authorsHTML = item.authors ? `
                <p class="text-sm text-gray-600 mb-4">${item.authors}</p>
            ` : '';

            const timelineItem = `
                <div class="mb-12 relative">
                    <div class="timeline-dot absolute left-0 top-1.5 w-4 h-4 bg-blue-500 rounded-full border-4 border-white"></div>
                    <div class="ml-10">
                        <p class="text-sm text-gray-500 mb-2 font-medium">${item.date}</p>
                        <div class="timeline-card bg-white p-6 rounded-lg shadow-lg border border-gray-200">
                            <div class="flex flex-col md:flex-row items-start mb-4">
                                ${logoHTML}
                                <div class="flex-grow">
                                    <h3 class="text-xl font-bold text-gray-900 mb-2">${item.title}</h3>
                                    ${authorsHTML}
                                    ${conferenceHTML}
                                </div>
                            </div>
                            <p class="text-gray-700 mb-6">${item.description}</p>
                            <div class="flex flex-wrap gap-3 mt-4">
                                ${linksHTML}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            timelineContainer.innerHTML += timelineItem;
        });
    }

    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.dataset.filter;
            renderTimeline(filter);

            filterButtons.forEach(btn => {
                btn.classList.remove('bg-blue-600', 'text-white');
                btn.classList.add('bg-gray-200', 'text-gray-700');
            });
            button.classList.add('bg-blue-600', 'text-white');
            button.classList.remove('bg-gray-200', 'text-gray-700');
        });
    });

    renderTimeline();
});