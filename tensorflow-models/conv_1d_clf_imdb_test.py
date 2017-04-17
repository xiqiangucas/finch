from keras.datasets import imdb
from keras.preprocessing import sequence
from conv_1d_clf import Conv1DClassifier
from utils import to_one_hot
import tensorflow as tf


max_features = 5000
maxlen = 400  # cut texts after this number of words (among top max_features most common words)
batch_size = 32
embedding_dims = 50


if __name__ == '__main__':
    print('Loading data...')
    (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)
    print(len(X_train), 'train sequences')
    print(len(X_test), 'test sequences')

    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
    print('x_train shape:', X_train.shape)
    print('x_test shape:', X_test.shape)
    y_train = to_one_hot(y_train)
    y_test = to_one_hot(y_test)

    sess = tf.Session()
    clf = Conv1DClassifier(seq_len=maxlen, vocab_size=max_features, embedding_dims=embedding_dims, n_out=2,
                           sess=sess)
    log = clf.fit(X_train, y_train, n_epoch=10, batch_size=batch_size, en_exp_decay=True, en_shuffle=True,
                  val_data=(X_test,y_test))
    pred = clf.predict(X_test)
    tf.reset_default_graph()

    final_acc = np.equal(np.argmax(pred,1), np.argmax(y_test,1)).astype(float).mean()
    print("final testing accuracy: %.4f" % final_acc)
