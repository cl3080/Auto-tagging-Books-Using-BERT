# Auto-tagging-Books-Using-BERT

There are millions of books published on the market. Literary agents can receive lots of pitches every year and usually needs time to read through the all the pitches, which may cause delay of publication. Thus, in this project I built a machine learning model simply using book's synopsis and titles to automatically place tags for books. This will not only help to save lots of labor to manually tag books but also can allow agents to quickly select books and focus on the pitches they are interested in.

GoodReads is one of the most extensive repository of books. So for this project, I scraped data from GoodReads and used title and synopsis as feature, genres as labels to train the model. Here is what the website look like:
![GoodReads Website](https://github.com/cl3080/Auto-tagging-Books-Using-BERT/blob/main/Images/WebsiteImage.png) 

**Overall workflow:**
1. Collect data from GoodReads. Here I scraped > 30K books and mainly focused on getting book synopsis, titles and genres. 
2. Basic data cleaning and exploratory data analysis.
3. Leveraged pre-trained embedding vectors from BERT language model.
4. Built a classification model using fined tuned model, achiving >85% accuracy and >0.8 F-scores across 20 genres.

![Pipleline](https://github.com/cl3080/Auto-tagging-Books-Using-BERT/blob/main/Images/Pipeline.png)

References:
1. https://colab.research.google.com/github/jalammar/jalammar.github.io/blob/master/notebooks/bert/A_Visual_Notebook_to_Using_BERT_for_the_First_Time.ipynb#scrollTo=fvFvBLJV0Dkv   
2. https://huggingface.co/transformers/model_doc/distilbert.html  
3. https://towardsdatascience.com/bert-explained-state-of-the-art-language-model-for-nlp-f8b21a9b6270
