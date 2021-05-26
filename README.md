# Auto-tagging-Books-Using-BERT

There are millions of books published on the market. Literary agents can receive lots of pitches every year and usually needs time to read through the all the pitches, which may cause delay of publication. Thus, in this project, I built a machine learning model using book's synopsis and titles to automatically place genre tags for books. This will not only help to save lots of labor to manually tag books but also can also agents to select books and focus on the pitches they are interested in.

GoodReads is one of the most extensive repository of books. So for this project, I scraped data from GoodReads and used title and synopsis as feature, genres as labels to train the model. Here is what the website look like:
![GoodReads Website](https://github.com/cl3080/Auto-tagging-Books-Using-BERT/blob/main/Images/WebsiteImage.png)

Overall workflow:
1. Collect data from GoodReads. Here I scraped > 10K books and mainly focused on getting book synopsis, titles and genres. 
3. Basic data cleaning and exploratory data analysis.
4. Leveraged pre-trained embedding vectors from BERT language model.
5. Built a classification model using logistic regression, achiving >85% accuracy and >0.8 F-scores across 20 genres.

