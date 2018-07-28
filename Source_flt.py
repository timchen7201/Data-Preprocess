
limit = {
    'maxq' : 20,
    'minq' : 6,
    'maxa' : 20,
    'mina' : 3
}
import nltk
import itertools
import jieba
import argparse

def read_lines(filename):
    with open(filename) as f:
        return open(filename).read().split('\n')[:-1]
def S_Filter(q_token,a_token):
    tokenized_sentences=q_token+a_token
    freq_dist=nltk.FreqDist(itertools.chain(*tokenized_sentences))
    print("type:",type(freq_dist))
    
    vocab = freq_dist.most_common(209612)[-number:]
    least_words=[]
    print("length:",len(vocab))
    for i in range(len(vocab)):
        word=vocab[i][0][:]
        least_words.append(word)
    with open("file.txt","w") as f:
        for s in least_words:
            f.write(str(s)+'\n')
    print("length:",len(least_words))
#    print("least",least_words)
#    print(vocab)
#    least_words=list(freq_dist.keys())[-1000:]
#    least_words_times=list(freq_dist.values())[-1000:]
#    print("Least Words:{%s} times:{%s}\n"%(least_words,least_words_times))
    return 0
def S_Filter2(q_token,a_token):
    with open("file.txt", 'r') as f:
        delete_list = [line.rstrip('\n') for line in f]
    delete_idx=[]
    print(q_token[1])
    for i in range(len(delete_list)):
        for j in range(len(q_token)):
            if delete_list[i] in q_token[j] or delete_list[i] in a_token[j]:
                print("delete_word",delete_list[i])
                print("----------------")
                print("{0}:{1}\t{2}".format(j,q_token[j],a_token[j]))
                delete_idx.append(j)
    with open("idx_20000.txt","w") as f:
        for i in range(len(delete_idx)):
            f.write(str(delete_idx[i])+'\n')
    return delete_idx
def segment(lines):
    jieba.load_userdict('../dict/dict.txt.big.txt')
    token=[]
    for stn in lines:
        #        print('sentence:',stn)
        words=jieba.cut(stn,cut_all=False)
        token.append(list(words))
#    print("token[1]:",token[1])
    return token
def filter_lines(q_seq,a_seq,idx):
    filter_q=[]
    filter_a=[]
    print("len:",idx)
    for i in range(0,len(a_seq)):
        if i not in idx:
            qlen=len(q_seq[i])
            alen=len(a_seq[i])
            if qlen >= limit['minq'] and qlen < limit['maxq'] and alen >=limit['mina'] and alen < limit['maxa']:
                filter_q.append(q_seq[i])
                filter_a.append(a_seq[i])
    return filter_q ,filter_a
def get_arg():
    parser=argparse.ArgumentParser()
    parser.add_argument('covert_file_q', type=str, help='covert question file without.txt')
    parser.add_argument('covert_file_a', type=str, help='covert answer file without.txt')
    
    parser.add_argument('elim_word',type=int,help='The amount of eliminate words')
    arguments = parser.parse_args()
    return arguments

if __name__=='__main__':
    arg=get_arg()
    Q_CH_FILENAME=arg.covert_file_q+'.txt'
    A_CH_FILENAME=arg.covert_file_a+'.txt'
    global number
    number=arg.elim_word
    q_lines=read_lines(Q_CH_FILENAME)
    a_lines=read_lines(A_CH_FILENAME)
    
    q_tokenized=segment(q_lines)
    a_tokenized=segment(a_lines)
    S_Filter(q_tokenized,a_tokenized)
    idx=S_Filter2(q_tokenized,a_tokenized)
    q_lines,a_lines=filter_lines(q_lines,a_lines,idx)
    x='coverted'
    with open((arg.covert_file_q)+'_coverted.txt','w') as f:
        for i in range(len(q_lines)):
            f.write(str(q_lines[i])+'\n')

    with open((arg.covert_file_a)+'_coverted.txt','w') as f:
        for i in range(len(a_lines)):
            f.write(str(a_lines[i])+'\n')
