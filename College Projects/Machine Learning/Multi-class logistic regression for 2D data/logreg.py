import numpy as np
import matplotlib.pyplot as plt
import random
import data
from sklearn import metrics
    
def logreg_train(X,Y_):
  '''
    Argumenti
      X:  podatci, np.array NxD
      Y_: indeksi razreda, np.array Nx1

    Povratne vrijednosti
      w, b: parametri logističke regresije
  '''
  
  W = np.random.randn(len(X[0]), max(Y_)+1) #D x C
  b = np.random.randn(1, max(Y_)+1) #1 x C
  

  param_niter = 1000
  param_delta = 1
  
  # gradijentni spust (param_niter iteracija)
  for i in range(param_niter):
      
    # eksponencirane klasifikacijske mjere
    # pri računanju softmaksa obratite pažnju
    # na odjeljak 4.1 udžbenika
    # (Deep Learning, Goodfellow et al)!
    scores = np.dot(X,W) + b   # N x C
    expscores = np.exp(scores - np.max(scores)) # N x C
    # nazivnik sofmaksa
    sumexp = np.sum(expscores, axis = 1)   # N x 1
    sumexp = np.reshape(sumexp, (1,len(sumexp))).transpose()
    
    # logaritmirane vjerojatnosti razreda 
    probs = expscores/sumexp   # N x C
    logprobs = np.log(probs)  # N x C

    # gubitak
    loss = 0 # scalar
    for j in range (len(logprobs)):
        loss = loss - logprobs[j,Y_[j]]

    loss = loss/len(X)
         
    
    # dijagnostički ispis
    if i % 10 == 0:
      print("iteration {}: loss {}".format(i, loss))
      

    # derivacije komponenata gubitka po mjerama
    dL_ds = np.zeros((len(probs), max(Y_)+1)) #N x C
    for j in range (len(probs)):
        for k in range (max(Y_)+1):
            dL_ds[j,k] = probs[j,k] - (Y_[j]==k)
 
    # gradijenti parametara
    grad_W = np.dot(dL_ds.transpose(),X)/len(X)    # C x D (ili D x C)
    grad_b = np.sum(dL_ds.transpose(), axis = 1)/len(X)    # C x 1 (ili 1 x C)
    
    # poboljšani parametri
    W = W - param_delta * grad_W.transpose()
    b = b - param_delta * grad_b

  return W,b

def logreg_classify(X, W, b):
    '''
      Argumenti
          X:    podatci, np.array NxD
          W, b: parametri logističke regresije 

      Povratne vrijednosti
          probs: vjerojatnosti razreda c1-cN za svaki podatak
    '''

    scores = np.dot(X,W) + b   # N x C
    expscores = np.exp(scores - np.max(scores)) # N x C
    # nazivnik sofmaksa
    sumexp = np.sum(expscores, axis = 1)   # N x 1
    sumexp = np.reshape(sumexp, (1,len(sumexp))).transpose()
    
    # vjerojatnosti razreda 
    probs = expscores/sumexp   # N x C
    
    return probs

def eval_perf_multi(Y, Y_):
  cm = metrics.confusion_matrix(Y_, Y)              
  recall = np.around(np.diag(cm) / np.sum(cm, axis = 1), decimals = 2)
  precision = np.around(np.diag(cm) / np.sum(cm, axis = 0), decimals = 2)
  accuracy = np.around(np.trace(cm)/np.sum(cm), decimals = 2)
  return accuracy, recall, precision

def logreg_decfun(W,b):
  def classify(X):
    return np.argmax(logreg_classify(X, W, b), axis = 1)
  return classify
    
if __name__=="__main__":
    np.random.seed(100)
    # instantiate the dataset
    X,Y_ = data.sample_gauss_2d(3, 100)

    # train the logistic regression model
    W,b = logreg_train(X, Y_)

    # evaluate the model on the train set
    probs = np.round_(logreg_classify(X, W, b))

    # recover the predicted classes Y   
    Y = np.zeros(len(Y_))
    temp = 0
    for i in range (len(probs)):
      for j in range (len(probs[0])):
        if (probs[i,j] == 1):
          Y[temp] = int(j)
          temp += 1
                    

    # evaluate and print performance measures
    
    accuracy, recall, precision = eval_perf_multi(Y, Y_)
    print("RECALL:")
    print(recall)
    print()
    print("PRECISION:")
    print(precision)
    print()
    print("ACCURACY:")
    print(accuracy)

    # graph the decision surface
    decfun = logreg_decfun(W,b)
    bbox=(np.min(X, axis=0), np.max(X, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)
      
    # graph the data points
    data.graph_data(X, Y_, Y, special=[])

    # show the plot
    plt.show()
    
    
