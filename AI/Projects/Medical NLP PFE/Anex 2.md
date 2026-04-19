
### 1. Papiers de Recherche Académiques (Bibliographie)
Ces articles fondent la rigueur scientifique de votre architecture, justifiant le passage de l'IA générique à l'IA spécialisée.

*   **Transformers & Mécanisme d'Attention :**
    *   Vaswani, A., et al. (2017). *Attention Is All You Need.* [Lien (arXiv)](https://arxiv.org/abs/1706.03762)
    *   *Contexte :* Origine du mécanisme d'Attention QKV. Indispensable pour votre gestion du "Negation Trap".
*   **Modèles Médicaux Spécialisés (Embeddings) :**
    *   Lee, J., et al. (2020). *BioBERT: a pre-trained biomedical language representation model for biomedical text mining.* [Lien (Bioinformatics)](https://academic.oup.com/bioinformatics/article/36/4/1234/5566506)
    *   Alsentzer, E., et al. (2019). *Publicly Available Clinical BERT Embeddings.* [Lien (ACL)](https://aclanthology.org/W19-1909/)
    *   Liu, F., et al. (2021). *Self-Alignment Pretraining for Biomedical Entity Representations (SapBERT).* [Lien (ACL)](https://aclanthology.org/2021.naacl-main.334/)
    *   Gu, Y., et al. (2021). *Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing (PubMedBERT).* [Lien (ACM)](https://dl.acm.org/doi/10.1145/3458609.3458742)
*   **Ranking & Information Retrieval :**
    *   Burges, C., et al. (2005). *Learning to Rank using Gradient Descent (RankNet).* [Lien (ICML)](https://icml.cc/2005/index.html)
    *   *Contexte :* Base du Pairwise Learning-to-Rank (LTR) pour votre tournoi de classement.

---

### 2. Théories Mathématiques et Origines
*Ces concepts ont été implémentés pour garantir la précision scientifique face aux maladies rares.*

*   **Géométrie 768-D & Hypothèse de la Variété (Manifold Hypothesis) :** Projection des concepts médicaux dans un espace de haute dimension pour "déplier" la vérité biologique.
*   **Similarité Cosinus :** $\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$. Choisi pour son **invariance à la longueur**, permettant de comparer notes patient et définitions maladies.
*   **Le Piège du Seuil de 0.9 :** Problème de saturation des scores Cosinus nécessitant le recours à des graphes (Phase 2) pour discriminer des maladies quasi-identiques.
*   **Théorie des Graphes (NetworkX MultiDiGraph) :** Raisonnement en temps constant $O(1)$ avec des chemins dirigés pour assurer l'**IA Explicable (XAI)**.
*   **Similarité de Jaccard :** $J(A, B) = \frac{|A \cap B|}{|A \cup B|}$. Utilisée pour le "Biological Fact-Check" (vérification des IDs HPO) plutôt que la simple similarité textuelle.
*   **Features de Classement (Neural Ranker) :** Utilisation de la **différence vectorielle $(A - B)$** et du **produit de Hadamard $(A * B)$** au sein de votre MLP (PyTorch) pour isoler les symptômes discriminants.

---

### 3. Stack Technique et Implémentation

#### A. LLM & Nettoyage (Phase 1)
*   **LLMs :** Gemini / ChatGPT (Configurés avec **Température = 0** pour le déterminisme).
*   **Prompt Engineering :** *Few-Shot Prompting* et *Chain-of-Thought (CoT)*.
*   **Regex Safety Net :** `r'\{.*\}'` pour garantir une sortie JSON propre, indépendamment du comportement "bavard" de l'IA.

#### B. Modèles d'Embeddings (Hugging Face)
*   **BioBERT (Cased) :** [dmis-lab/biobert-v1.1](https://huggingface.co/dmis-lab/biobert-v1.1). *Cased* pour préserver la nomenclature IUPAC/génétique.
*   **ClinicalBERT :** [emilyalsentzer/Bio_ClinicalBERT](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT)
*   **SapBERT :** [cambridgeltl/SapBERT-from-PubMedBERT-fulltext](https://huggingface.co/cambridgeltl/SapBERT-from-PubMedBERT-fulltext)
*   **PubMedBERT :** [microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract](https://huggingface.co/microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract)
*   **Baseline (Contrôle) :** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

#### C. Ontologies (Normalisation Sémantique)
*   **HPO :** [hpo.jax.org](https://hpo.jax.org/)
*   **Orphanet :** [orpha.net](https://www.orpha.net/)
*   **MONDO :** [mondo.monarchinitiative.org](https://mondo.monarchinitiative.org/)
*   **Syntaxe :** [RDF Turtle (.ttl)](https://www.w3.org/TR/turtle/)

#### D. Validation Statistique
*   **Mann-Whitney U-Test :** Utilisé via `scipy.stats.mannwhitneyu` pour confirmer la supériorité statistique des modèles adaptés ($p < 0.05$).
*   **MRR (Mean Reciprocal Rank) :** Pour valider l'algorithme de ranking.
*   **Visualisation :** `Seaborn` (Violin plots, Heatmaps).