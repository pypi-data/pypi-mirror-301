import pandas as pd
import numpy as np
import nltk
from nltk.util import ngrams

nltk_stemmer = nltk.stem.PorterStemmer()
nltk_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

vec_luhn_sw_pronouns = ['i','you','he','she','it','we','they','them','us','him','her','his','hers','its','theirs','our','your']
vec_luhn_sw_prep = ['a','abaft','aboard','about','above','absent','across','afore','after','against','along','alongside','amid','amidst',
                    'among','amongst','an','anenst','apropos','apud','around','as','aside','astride','at','athwart','atop','barring','before',
                    'behind','below','beneath','beside','besides','between','beyond','but','by','circa','concerning','despite','down','during',
                    'except','excluding','failing','following','for','forenenst','from','given','in','including','inside','into','lest','like','mid',
                    'midst','minus','modulo','near','next','notwithstanding','of','off','on','onto','opposite','out','outside','over','pace','past',
                    'per','plus','pro','qua','regarding','round','sans','save','since','than','the','through','throughout','till','times','to',
                    'toward','towards','under','underneath','unlike','until','unto','up','upon','versus','via','vice','with','within','without',
                    'worth']
vec_luhn_sw_articles = ['a','an','the']
vec_luhn_sw_other = ['a','an','of','in','and','this','are','by','can','from','as','they','for','that','the','is','at','be','on','to','e','g','it']
vec_luhn_sw = vec_luhn_sw_pronouns
vec_luhn_sw.extend(vec_luhn_sw_prep)
vec_luhn_sw.extend(vec_luhn_sw_articles)
vec_luhn_sw.extend(vec_luhn_sw_other)
vec_luhn_sw = [x.lower() for x in vec_luhn_sw]
vec_luhn_sw = list(set(vec_luhn_sw))

def tokenize(val_text,
             val_n_gram:int=-1,
             is_sw_remove:bool=False,
             vec_sw_add:list=['e','g','it'],
             func_stem=None):
    """
    Tokenizes the input text into sentences and words, with optional stopword removal and stemming.

    Args:
        val_text (str): The input text to be tokenized.
        val_n_gram (int): The length of a contiguous sequence of n words. Defaults to -1, which are 1-grams.
        is_sw_remove (bool, optional): Flag indicating whether to remove stopwords from the tokenized words. 
                                       Defaults to False.
        vec_sw_add (list, optional): Additional stopwords to remove, in case `is_sw_remove` is True. 
                                     Defaults to ['e', 'g', 'it'].
        func_stem (callable, optional): A function to apply stemming to the words. This function accepts a list 
                                        of words and return a transformed list of stemmed words. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: A DataFrame with tokenized sentences. The DataFrame has two columns:
                - 'sentence': The tokenized sentences.
                - 'id_sent': The sentence index.
            - pd.DataFrame: A DataFrame with tokenized words. The DataFrame has two columns:
                - 'word': The tokenized words (lowercased and stopwords removed, if applicable).
                - 'id_sent': The sentence index corresponding to each word.

    Example:
        val_text = "This is a sentence. Here's another one."
        df_sentences, df_words = tokenize(val_text,is_sw_remove=True,vec_sw_add=['here'],func_stem=None)
    
    The function will tokenize the input text into sentences and words, remove the stopwords (including 'here'), and 
    apply stemming if `func_stem` is provided.
    """
    if(is_sw_remove):
        nltk_stopwords = nltk.corpus.stopwords.words('english')
        nltk_stopwords.extend(vec_sw_add)
    else:
        nltk_stopwords = []
    nltk_tokens_sent = nltk.sent_tokenize(val_text)
    df_sentences = pd.DataFrame({'sentence':nltk_tokens_sent})
    df_sentences['id_sent'] = df_sentences.index
    df_words = []
    for i,val_sent in enumerate(nltk_tokens_sent):
        nltk_tokens_word = [j.lower() for j in nltk_tokenizer.tokenize(val_sent) if j not in nltk_stopwords]
        if(val_n_gram>1):
            vec_n_grams = ngrams(nltk_tokens_word,n=val_n_gram)
            nltk_tokens_word = [' '.join(x) for x in vec_n_grams]
        df_words_tmp = pd.DataFrame({'word':nltk_tokens_word})
        df_words_tmp['id_sent'] = i
        df_words.append(df_words_tmp)
    df_words = pd.concat(df_words,ignore_index=True,sort=False)
    if(func_stem is not None):
        df_words.sort_values(by='word',inplace=True)
        vec_tmp_words = df_words['word'].copy()
        df_words['word_orig'] = vec_tmp_words
        df_words['word'] = func_stem(vec_words=df_words['word'].copy())
        df_words.sort_index(inplace=True)
    return(df_sentences,df_words)

def tokenize_stem_nltk(vec_words:list):
    """
    Applies NLTK's Porter stemming algorithm to a list of words.

    Args:
        vec_words (list): A list of words (strings) to be stemmed.

    Returns:
        list: A list of stemmed words, where each word in the input list is transformed by the NLTK Porter stemmer.

    Example:
        vec_words = ['running', 'jumps', 'easily']
        stemmed_words = tokenize_stem_nltk(vec_words)
    
    The function will return: ['run', 'jump', 'eas']
    """
    return([nltk_stemmer.stem(x) for x in vec_words])

def tokenize_stem_luhn_compare(str_a:str,
                               str_b:str,
                               val_min_len:int=6):
    """
    Compares two strings using a character-by-character comparison, counting the number of differing characters.
    If either string's length is less than `val_min_len`, the function returns infinity.

    Args:
        str_a (str): The first string to be compared.
        str_b (str): The second string to be compared.
        val_min_len (int, optional): The minimum length of the strings required for comparison. Defaults to 6.

    Returns:
        int or float: The number of character differences between the two strings. If either string is shorter than 
                      `val_min_len`, returns infinity (np.inf).

    Example:
        str_a = "running"
        str_b = "jumping"
        val_cnt = tokenize_stem_luhn_compare(str_a, str_b, val_min_len=6)
    
    The function will compare 'running' and 'jumping', counting the differing characters.
    If either string is shorter than 6 characters, it will return np.inf.
    """
    str_zipped = zip(str_a,str_b)
    val_cnt = 0
    if(len(str_a)>val_min_len and len(str_b)>val_min_len):
        for i,tupl_letters in enumerate(str_zipped):
            if(tupl_letters[0]!=tupl_letters[1]):
                val_cnt += 1
        val_cnt += abs(len(str_a)-len(str_b))
    else:
        val_cnt = np.inf
    return(val_cnt)

def tokenize_stem_luhn(vec_words:list,val_cutoff:int=6):
    """
    Applies the Luhn stemming algorithm to a list of words by comparing consecutive words and grouping them based on 
    character similarity. If two consecutive words differ by fewer characters than the specified cutoff, the previous word is retained.

    Args:
        vec_words (list): A list of words (strings) to be processed using the Luhn comparison method.  This list should be sorted in
                          alphabetical order.
        val_cutoff (int, optional): The maximum allowable character difference between consecutive words for them to 
                                    be considered similar. If the difference is less than or equal to this value, 
                                    the previous word is retained. Defaults to 6.

    Returns:
        list: A list of words representing resolved/deduplicated words.

    Example:
        vec_words = ['running', 'run', 'jumps', 'jumping', 'easily']
        processed_words = tokenize_stem_luhn(vec_words, val_cutoff=3)
    
    In this example, 'run' will replace 'running' based on the character similarity, while other words will remain unchanged.
    """
    vec_words_rtn = []
    pre_str_word = None
    for i,cur_str_word in enumerate(vec_words):
        if(i==0):
            pre_str_word = cur_str_word
            vec_words_rtn.append(cur_str_word)
        else:
            if(tokenize_stem_luhn_compare(str_a=cur_str_word,str_b=pre_str_word)<=val_cutoff):
                vec_words_rtn.append(pre_str_word)
            else:
                vec_words_rtn.append(cur_str_word)
            pre_str_word = cur_str_word
    return(vec_words_rtn)

def word_freq_cutoffs(df:pd.DataFrame,
                      val_lower:float=0.30,
                      val_upper:float=0.88,
                      is_print:bool=False):
    """
    Calculates the significance score cutoffs for words based on specified quantiles of the significance distribution.

    Args:
        df (pd.DataFrame): A DataFrame containing a 'significance' column, which represents the significance score of each word.
        val_lower (float, optional): The lower quantile to calculate the cutoff for significance scores. Defaults to 0.15.
        val_upper (float, optional): The upper quantile to calculate the cutoff for significance scores. Defaults to 0.85.
        is_print (bool, optional): If True, prints the calculated lower and upper significance cutoffs. Defaults to False.

    Returns:
        tuple: A tuple containing two values:
            - float: The lower significance cutoff based on the `val_lower` quantile.
            - float: The upper significance cutoff based on the `val_upper` quantile.

    Example:
        df = pd.DataFrame({'significance': [0.1, 0.5, 0.9, 0.3, 0.7]})
        word_freq_cutoffs(df, val_lower=0.2, val_upper=0.8)
        
        Output:
        (0.3, 0.7)
        
    Notes:
        - If the lower quantile value equals the minimum significance score, a small value (1e-5) is added to avoid returning the minimum.
        - Similarly, if the upper quantile value equals the maximum significance score, a small value (1e-5) is subtracted to avoid returning the maximum.
    """
    #C
    val_sig_lower = df['significance'].quantile(q=val_lower)
    if(val_sig_lower==df['significance'].min()):
        val_sig_lower = df['significance'].quantile(q=val_lower)+1e-5
    #D
    val_sig_upper = df['significance'].quantile(q=val_upper)
    if(val_sig_upper==df['significance'].max()):
        val_sig_upper = df['significance'].quantile(q=val_upper)-1e-5
    if(is_print):
        print(f'''Quantile Significance Lower = {'{:.0f}'.format(val_sig_lower)}\nQuantile Significance Upper = {'{:.0f}'.format(val_sig_upper)}''')
    return(val_sig_lower,val_sig_upper)

def calc_signifcance_words(df:pd.DataFrame,
                           is_use_luhn_tf:bool=True,
                           is_sw_zero:bool=False,
                           vec_sw_add:list=['e','g','it'],
                           vec_sw_luhn:list=[]):
    """
    Calculates the significance of words in a DataFrame based on word frequency, 
    with options to remove stopwords and apply different term frequency methods.

    Args:
        df (pd.DataFrame): A DataFrame containing at least a 'word' column, where each row represents a word.
        is_use_luhn_tf (bool, optional): If True, uses the Luhn method (raw word frequency) for calculating word significance. 
                                         If False, uses the term frequency (TF) method, which divides word count by the total number of words. Defaults to True.
        is_sw_zero (bool, optional): If True, assigns a significance score of zero to stopwords found in the text. 
                                     Defaults to False.
        vec_sw_add (list, optional): A list of additional stopwords to be considered if `is_sw_zero` is True. Defaults to ['e', 'g', 'it'].
        vec_sw_luhn (list, optional): A list of words to exclude from the DataFrame before significance calculation (Luhn's stopwords). 
                                      Defaults to None, but could be list of preopositions, pronouns, and articles by passing built-in vec_luhn_sw.

    Returns:
        pd.DataFrame: A DataFrame where each word is enriched with its corresponding significance score, calculated either using Luhn's raw frequency 
                      or TF method.

    Example:
        df = pd.DataFrame({'word': ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']})
        calc_signifcance_words(df, is_use_luhn_tf=True, is_sw_zero=False)
        
        Output:
        | word   | count | significance |
        |--------|-------|--------------|
        | apple  | 3     | 3            |
        | banana | 2     | 2            |
        | cherry | 1     | 1            |
    """
    df_word_cnts = pd.DataFrame(df['word'].value_counts()).reset_index()
    if(vec_sw_luhn):
        for i in vec_sw_luhn:
            df.drop(index=df.index[df['word']==i],inplace=True)
    if(is_sw_zero):
        nltk_stopwords = nltk.corpus.stopwords.words('english')
        nltk_stopwords.extend(vec_sw_add)
        for i,row in df.iterrows():
            if(row['word'] in nltk_stopwords):
                df_word_cnts.at[i,'count'] = 0
    if(is_use_luhn_tf):
        df_word_cnts['significance'] = df_word_cnts['count']
    else:
        #tf = (number of repetitions of word in a document) / (# of words in a document)
        df_word_cnts['significance'] = df_word_cnts['count']/df.shape[0]
    df_rev = pd.merge(left=df,right=df_word_cnts,on='word',how='left')
    return(df_rev)

def calc_word_score(val_sig:float,
                    val_lower:float,
                    val_upper:float):
    """
    Calculates the score of a word based on its significance value, constrained within a specified range.

    Args:
        val_sig (float): The significance value of the word.
        val_lower (float): The lower bound of the acceptable range.
        val_upper (float): The upper bound of the acceptable range.

    Returns:
        float: The score of the word. If `val_sig` is within the range [val_lower, val_upper], 
               it returns `val_sig`. Otherwise, it returns 0.

    Example:
        calc_word_score(8, 2, 10)
        
        Output:
        8

        calc_word_score(1, 2, 10)
        
        Output:
        0
    """
    val_score = 0
    if(val_sig>=val_lower and val_sig<=val_upper):
        val_score = val_sig
    return(val_score)

def calc_sentence_score(df:pd.DataFrame,
                        val_num_apart:int=5,
                        is_vector_return:bool=False,
                        func_summary=None):
    vec_scores = []
    vec_n_length = []
    val_idx_max = df.index.max()
    vec_indices = df.index.to_list()
    for i,z in enumerate(vec_indices):
        val_idx_last_sig_word = -1
        df_subset = df.loc[vec_indices[i:i+val_num_apart]].copy()
        if(df_subset.iloc[0]['score']>0):
            val_max_i = df_subset.loc[df_subset['score']>0].index.max()
            val_idx_last_sig_word = vec_indices.index(val_max_i)
            is_srching = True
            num_iter = 0
            while(is_srching):
                num_iter += 1
                df_subset_srch = df.loc[vec_indices[i:val_idx_last_sig_word+val_num_apart]].copy()
                val_max_i_rev = df_subset_srch.loc[df_subset_srch['score']>0].index.max()
                val_idx_last_sig_word_rev = vec_indices.index(val_max_i_rev)
                if(val_idx_last_sig_word==val_idx_last_sig_word_rev):
                    is_srching = False
                    df_range = df.loc[vec_indices[i:val_idx_last_sig_word+1]].copy()
                    #vec_scores.append(df_range['score'].sum())
                    #vec_n_length.append(df_range.loc[df_range['score']>0].shape[0])
                    vec_scores.append(np.sum([df_range['score']>0]))
                    vec_n_length.append(val_idx_last_sig_word+1-i)
                else:
                    val_max_i = val_max_i_rev
                    val_idx_last_sig_word = val_idx_last_sig_word_rev
        else:
            vec_scores.append(0.)
            vec_n_length.append(1.)
    if(is_vector_return):
        rtn_val = [vec_scores,vec_n_length]
    else:
        if(func_summary is None):
            val_idx_max = np.argmax(vec_scores)
            rtn_val = (vec_scores[val_idx_max]**2)/vec_n_length[val_idx_max]
        else:
            rtn_val = func_summary(vec_scores)
    return(rtn_val)

def calc_sentence_score_all(df:pd.DataFrame,
                            val_num_apart:int=5,
                            is_vector_return:bool=False,
                            func_summary=None):
    """
    Calculates scores for each unique sentence in the DataFrame using a custom scoring function.

    Args:
        df (pd.DataFrame): A DataFrame containing sentence data with at least the following columns:
                           'id_sent' (unique identifier for each sentence).
        val_num_apart (int, optional): A parameter to control the scoring process, typically defining 
                                       how many adjacent sentences are considered during scoring. Defaults to 5.
        is_vector_return (bool, optional): If True, returns a list of scores for each sentence. 
                                           If False, returns a DataFrame of sentence IDs and their scores. 
                                           Defaults to False.
        func_summary (callable, optional): A custom function used to calculate the score for each sentence. 
                                           If None, a default scoring function is used. Default is None.

    Returns:
        list or pd.DataFrame: 
            - If `is_vector_return` is True, returns a list of scores for each unique sentence.
            - If `is_vector_return` is False, returns a DataFrame with columns:
                - 'id_sent': the unique sentence identifier.
                - 'score': the corresponding score for each sentence, sorted by score in descending order.
    """
    vec_scores_sent_ids = df['id_sent'].unique()
    vec_scores_sent_ids.sort()
    vec_scores_sent = []
    for i in vec_scores_sent_ids:
        vec_scores_sent.append(calc_sentence_score(df=df.loc[df['id_sent']==i].copy(),
                                                        val_num_apart=val_num_apart,
                                                        is_vector_return=is_vector_return,
                                                        func_summary=func_summary))
    if(is_vector_return):
        rtn_val = vec_scores_sent
    else:
        df_sentences_scored = pd.DataFrame([vec_scores_sent_ids,vec_scores_sent]).T
        df_sentences_scored.columns = ['id_sent','score']
        df_sentences_scored.sort_values(by=['score'],ascending=False,inplace=True)
        rtn_val = df_sentences_scored.copy()
    return(rtn_val)

def summarize(df_sentences:pd.DataFrame,
              df_scores:pd.DataFrame,
              val_num_sentences:int=5):
    """
    Summarizes the top sentences based on their corresponding scores.

    Args:
        df_sentences (pd.DataFrame): A DataFrame containing sentence data with at least two columns:
                                     'id_sent' (unique identifier for sentences) and 'sentence' (the text).
        df_scores (pd.DataFrame): A DataFrame containing scores for each sentence with at least two columns:
                                  'id_sent' (matching 'id_sent' from df_sentences) and 'score' (the numerical score).
        val_num_sentences (int, optional): The number of top sentences to include in the summary. Defaults to 5.

    Returns:
        tuple: A tuple containing two elements:
            - list: A list of the top sentence scores.
            - list: A list of the corresponding top sentences (strings).

    Example:
        df_sentences = pd.DataFrame({'id_sent': [1, 2, 3], 'sentence': ['This is sentence 1', 'This is sentence 2', 'This is sentence 3']})
        df_scores = pd.DataFrame({'id_sent': [1, 2, 3], 'score': [0.85, 0.92, 0.75]})
        summarize(df_sentences, df_scores, val_num_sentences=2)
        
        Output:
        ([0.92, 0.85], ['This is sentence 2', 'This is sentence 1'])
    """
    vec_summary_text = []
    vec_summary_scores = []
    df = pd.merge(left=df_sentences,right=df_scores,on='id_sent',how='left')
    df.sort_values(by=['score'],ascending=False,inplace=True)
    for i,row in df.head(val_num_sentences).iterrows():
        vec_summary_scores.append(row['score'])
        vec_summary_text.append(row['sentence'])
    return(vec_summary_scores[:val_num_sentences],vec_summary_text[:val_num_sentences])

def print_summary(vec_scores:list,
                  vec_sentences:list,
                  is_print:bool=True):
    """
    Combines sentences with their corresponding scores, optionally prints them, and returns the combined result.

    Args:
        vec_scores (list): A list of numerical scores corresponding to each sentence.
        vec_sentences (list): A list of sentences to be combined with their respective scores.
        is_print (bool, optional): A flag that indicates whether to print the combined result. 
                                   Defaults to True.

    Returns:
        list: A list of combined sentences and their corresponding scores in the format:
              "<sentence> [<score>]".
              
    Example:
        vec_scores = [0.85, 0.92]
        vec_sentences = ["This is a sentence.", "Another sentence."]
        print_summary(vec_scores, vec_sentences)
        
        Output:
        This is a sentence. [0.8500] Another sentence. [0.9200]
    """
    vec_combined = []
    for i in zip(vec_scores,vec_sentences):
        vec_combined.append('{} '.format(i[1].strip().replace('\n',' '))+"\33[31m"+'[{:.4f}]'.format(i[0])+"\33[0m")
    if(is_print):
        print(' '.join(vec_combined))
    return(vec_combined)

def run_auto_summarization(val_text:str,
                           val_lower_flt:float=0.30,
                           val_lower_int:int=None,
                           val_upper_flt:float=0.88,
                           val_upper_int:int=None,
                           val_spacing:int=5,
                           val_num_sentences:int=4,
                           val_n_gram:int=-1,
                           is_sw_remove:bool=False,
                           is_sw_zero:bool=False,
                           is_use_luhn_tf=True,
                           vec_sw_luhn:list=[],
                           vec_sw_add:list=[],
                           func_stem_selected=None,
                           func_summary_selected=None,
                           is_print:bool=False):
    df_sents,df_words = tokenize(val_text=val_text,
                                 val_n_gram=val_n_gram,
                                 is_sw_remove=is_sw_remove,
                                 vec_sw_add=vec_sw_add,
                                 func_stem=func_stem_selected)
    df_words_scored = calc_signifcance_words(df=df_words,
                                             is_use_luhn_tf=is_use_luhn_tf,
                                             is_sw_zero=is_sw_zero,
                                             vec_sw_luhn=vec_sw_luhn,
                                             vec_sw_add=vec_sw_add)
    if((val_lower_int is None or val_upper_int is None) and val_lower_flt<val_upper_flt):
        val_sig_lower,val_sig_upper = word_freq_cutoffs(df=df_words_scored,
                                                        val_lower=val_lower_flt,
                                                        val_upper=val_upper_flt,
                                                        is_print=is_print)
    elif(val_lower_int is None or val_upper_int is None):
        if(is_print):
            print(f'''WARNING: Lower Cutoff={val_lower_flt} >> Upper Cutoff={val_upper_flt}, which cannot happen; reseting to defaults...''')
        val_sig_lower,val_sig_upper = word_freq_cutoffs(df=df_words_scored,
                                                        val_lower=val_lower_flt,
                                                        val_upper=val_upper_flt,
                                                        is_print=is_print)
    elif(val_lower_int<val_upper_int):
        val_sig_lower = val_lower_int
        val_sig_upper = val_upper_int
    else:
        if(is_print):
            print(f'''WARNING: Lower Cutoff={val_lower_int} >> Upper Cutoff={val_upper_int}, which cannot happen; reseting to defaults...''')
        val_sig_lower,val_sig_upper = word_freq_cutoffs(df=df_words_scored,
                                                        val_lower=val_lower_flt,
                                                        val_upper=val_upper_flt,
                                                        is_print=is_print)
    if(df_words_scored['significance'].max()>=val_sig_upper and df_words_scored['significance'].min()<=val_sig_lower):
        df_words_scored['score'] = [calc_word_score(val_sig=x,
                                                    val_lower=val_sig_lower,
                                                    val_upper=val_sig_upper) for x in df_words_scored['significance']]
        df_sentences_scored = calc_sentence_score_all(df=df_words_scored,
                                                      val_num_apart=val_spacing,
                                                      func_summary=func_summary_selected)
        vec_scores,vec_top_sents = summarize(df_sentences=df_sents,
                                             df_scores=df_sentences_scored,
                                             val_num_sentences=val_num_sentences)
        if(is_print):
            str_rtn = print_summary(vec_scores=vec_scores,
                                    vec_sentences=vec_top_sents,
                                    is_print=is_print)
    else:
        df_sentences_scored = pd.DataFrame()
        vec_scores = []
        vec_top_sents = []
        if(is_print):
            print(f'''WARNING: The selected lower limit results in C={val_sig_lower}, max={df_words_scored['significance'].min()}''')
            print(f'''WARNING: The selected upper limit results in D={val_sig_upper}, max={df_words_scored['significance'].max()}''')
    return(df_words_scored,df_sentences_scored,vec_scores,vec_top_sents)

#This ensures the NLTK stopwords are updated when the library is imported...
nltk.download('stopwords',quiet=True)