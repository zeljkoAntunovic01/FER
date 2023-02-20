import numpy as np
import matplotlib.pyplot as plt
import random
import IPython
import data


def binlogreg_train(X,Y_):
  '''
    Argumenti
      X:  podatci, np.array NxD
      Y_: indeksi razreda, np.array Nx1

    Povratne vrijednosti
      w, b: parametri logističke regresije
  '''
  
  w = np.random.randn(len(X[0]), 1)
  b = 0
  param_niter = 100
  param_delta = 1
  
  # gradijentni spust (param_niter iteracija)
  for i in range(param_niter):
      
    # klasifikacijske mjere
    scores = np.dot(X, w) + b    # N x 1
    
    # vjerojatnosti razreda c_1
    probs = np.exp(scores)/(1+np.exp(scores))  # N x 1
    
    # gubitak
    loss_contribution_0 = np.sum(-np.log(1 - probs[Y_==0]))
    loss_contribution_1 = np.sum(-np.log(probs[Y_==1]))
    loss  = (loss_contribution_0 + loss_contribution_1)/len(X)    # scalar
    
    # dijagnostički ispis
    if i % 10 == 0:
        print("iteration {}: loss {}".format(i, loss))
        
    # derivacije gubitka po klasifikacijskim mjerama    
    dL_dscores = np.zeros((len(probs),1))  # N x 1
    for j in range (len(probs)):
        if (Y_[j] == 0):
            
            
            dL_dscores[j,0] = probs[j] - 0
        else:
            dL_dscores[j,0] = probs[j] - 1
            
    # gradijenti parametara
    grad_w = np.dot(dL_dscores.transpose(), X)/len(X)     # D x 1
    grad_b = np.sum(dL_dscores)/len(X)     # 1 x 1
    
    # poboljšani parametri
    w = w - param_delta * grad_w.transpose()
    b = b - param_delta * grad_b

  return w,b
    
 
  
def binlogreg_classify(X, w, b):
    '''
      Argumenti
          X:    podatci, np.array NxD
          w, b: parametri logističke regresije 

      Povratne vrijednosti
          probs: vjerojatnosti razreda c1
    '''

    # klasifikacijske mjere
    scores = np.dot(X, w) + b    # N x 1
    
    # vjerojatnosti razreda c_1
    probs = np.exp(scores)/(1+np.exp(scores))  # N x 1
    
    return probs

def binlogreg_decfun(w,b):
    def classify(X):
      return binlogreg_classify(X, w, b)
    return classify



if __name__=="__main__":
    np.random.seed(100)

    # instantiate the dataset
    X,Y_ = data.sample_gauss_2d(2, 100)

    # train the logistic regression model
    w,b = binlogreg_train(X, Y_)

    # evaluate the model on the train set
    probs = binlogreg_classify(X, w, b)

    # recover the predicted classes Y   
    Y = np.array(np.round_(probs.flatten()), dtype = int)


    # evaluate and print performance measures
    accuracy, recall, precision = data.eval_perf_binary(Y, Y_)
    AP = data.eval_AP(Y_[probs.flatten().argsort()])
    print (accuracy, recall, precision, AP)

    # graph the decision surface
    decfun = binlogreg_decfun(w,b)
    bbox=(np.min(X, axis=0), np.max(X, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)
      
    # graph the data points
    data.graph_data(X, Y_, Y, special=[])

    # show the plot
    plt.show()
  
