import pandas as pd
import requests
sampleComment = "She is a good teacher!"

#reading the dataset
data = pd.read_csv('Comments.csv')
print("number of data ", data.shape)
training = data[['comment','label']]
#convert comments and label dataFrame into list

list_commentsAndLabel = training.values.tolist()

def getSentiment(sampleComment):
    dictToSend = {'comment': sampleComment}
    res = requests.post('http://127.0.0.6:8000/getSentiment', json=dictToSend)
    
    dictFromServer = res.json()
    return str(dictFromServer)

def getAccuracy():
    countPos = sum(p[1] == "positive" for p in list_commentsAndLabel)
    countNeg = sum(p[1] == "negative" for p in list_commentsAndLabel)
    countNeu = sum(p[1] == "neutral" for p in list_commentsAndLabel)

    correctPosPred = 0
    correctNegPred = 0
    correctNeuPred = 0

    posPred = 0
    negPred = 0
    neuPred = 0

    correct = 0
    miss = 0
    for entry in list_commentsAndLabel:
        comment = entry[0]
        sentiment = getSentiment(comment).split(" ")[0]
        #get all predicted positive,negative,neutral (correct and wrong predictions)
        if(sentiment == "positive"):
            posPred += 1
        elif(sentiment == "negative"):
            negPred += 1
        else: 
            neuPred += 1

        if(sentiment == entry[1]):
            if(sentiment == "positive"):
                correctPosPred += 1
            elif(sentiment == "negative"):
                correctNegPred += 1
            else: 
                correctNeuPred += 1

            correct += 1
        else:
            print("WRONG - CORRECT: ", entry[1])
            print(comment)
            print('response from server:', getSentiment(comment))
            miss += 1
    #get precision, recall and f1-score
    posPrecision = round(correctPosPred/posPred * 100,1)
    negPrecision = round(correctNegPred/negPred * 100,1)
    neuPrecision = round(correctNeuPred/neuPred * 100,1)

    posRecall = round(correctPosPred/countPos * 100,1)
    negRecall = round(correctNegPred/countNeg * 100,1)
    neuRecall = round(correctNeuPred/countNeu * 100,1)

    posF1 = round(2 * (posPrecision * posRecall) / (posPrecision + posRecall),1)
    negF1 = round(2 * (negPrecision * negRecall) / (negPrecision + negRecall),1)
    neuF1 = round(2 * (neuPrecision * neuRecall) / (neuPrecision + neuRecall),1)

    avePrec =  round((posPrecision + negPrecision + neuPrecision)/3,1)
    aveRecall =  round((posRecall + negRecall + neuRecall)/3,1)
    aveF1 =  round((posF1 + negF1 + neuF1)/3,1)

    totalSupport = countPos + countNeu + countNeg
    accuracy = correct/len(data['comment'])
    #accuracy as whole
    print("--------------------- SUMMARY --------------------")
    print("accuracy: ", accuracy)
    print("miss", miss/len(data['comment']))
    print("correct: ", correct)
    print("miss", miss)
    print("recall")
    print("positive : ", correctPosPred, " correct prediction out of ", countPos)
    print("negative : ", correctNegPred, " correct prediction out of ", countNeg)
    print("neutral : ", correctNeuPred, " correct prediction out of ", countNeu)
    print("precision")
    print("positive : ", correctPosPred, " correct prediction out of ", posPred, " positive predictions.")
    print("negative : ", correctNegPred, " correct prediction out of ", negPred, " negative predictions.")
    print("neutral : ", correctNeuPred, " correct prediction out of ", neuPred, " neutral predictions.")
    print("---------------------------------------------------")
    print("         precision    recall    f1-score     support")
    print("positive   ", posPrecision, "    ", posRecall, "     ", posF1, "         ", countPos)
    print("negative   ", negPrecision, "    ", negRecall, "     ", negF1, "         ", countNeg)
    print("neutral    ", neuPrecision, "    ", neuRecall, "     ", neuF1, "         ", countNeu)
    print()
    print("accuracy                               ", accuracy)
    print("average    ", avePrec, "    ", aveRecall, "     ", aveF1, "         ", totalSupport)
getAccuracy()