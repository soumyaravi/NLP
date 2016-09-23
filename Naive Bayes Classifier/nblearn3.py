import os
import sys

stop_words = ['a','about','above','across','after','again','against','all','almost','alone','along','already','also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are','area','areas','around','as','ask','asked','asking','asks','at','away','b','back','backed','backing','backs','be','became','because','become','becomes','been','before','began','behind','being','beings','best','better','between','big','both','but','by','c','came','can','cannot','case','cases','certain','certainly','clear','clearly','come','could','d','did','differ','different','differently','do','does','done','down','downed','downing','downs','during','e','each','early','either','end','ended','ending','ends','enough','even','evenly','ever','every','everybody','everyone','everything','everywhere','f','face','faces','fact','facts','far','felt','few','find','finds','first','for','four','from','full','fully','further','furthered','furthering','furthers','g','gave','general','generally','get','gets','give','given','gives','go','going','good','goods','got','great','greater','greatest','group','grouped','grouping','groups','h','had','has','have','having','he','her','here','herself','high','higher','highest','him','himself','his','how','however','i','if','important','in','interest','interested','interesting','interests','into','is','it','its','itself','j','just','k','keep','keeps','kind','knew','know','known','knows','l','large','largely','last','later','latest','least','less','let','lets','like','likely','long','longer','longest','m','made','make','making','man','many','may','me','member','members','men','might','more','most','mostly','mr','mrs','much','must','my','myself','n','necessary','need','needed','needing','needs','never','new','newer','newest','next','no','nobody','non','noone','not','nothing','now','nowhere','number','numbers','o','of','off','often','old','older','oldest','on','once','one','only','open','opened','opening','opens','or','order','ordered','ordering','orders','other','others','our','out','over','p','part','parted','parting','parts','per','perhaps','place','places','point','pointed','pointing','points','possible','present','presented','presenting','presents','problem','problems','put','puts','q','quite','r','rather','really','right','room','rooms','s','said','same','saw','say','says','second','seconds','see','seem','seemed','seeming','seems','sees','several','shall','she','should','show','showed','showing','shows','side','sides','since','small','smaller','smallest','so','some','somebody','someone','something','somewhere','state','states','still','such','sure','t','take','taken','than','that','the','their','them','then','there','therefore','these','they','thing','things','think','thinks','this','those','though','thought','thoughts','three','through','thus','to','today','together','too','took','toward','turn','turned','turning','turns','two','u','under','until','up','upon','us','use','used','uses','v','very','w','want','wanted','wanting','wants','was','way','ways','we','well','wells','went','were','what','when','where','whether','which','while','who','whole','whose','why','will','with','within','without','work','worked','working','works','would','x','y','year','years','yet','you','young','younger','youngest','your','yours','z']

spam = {}
ham = {}
prob_spam = {}
prob_ham = {}
distinct = {}

# read the files and split it into tokens
# call the required functions from the main function
def main(args):
    spam_files = 0
    ham_files = 0

    for subdir, dirs, files in os.walk(args[0]):
        for file in files:
            if (file.endswith('.txt')):
                words = []
                with open(os.path.join(subdir, file), "r", encoding="latin1") as infile:
                    words = infile.read().split()
                infile.close()
                if file.__contains__('ham'):
                    ham_files += 1
                    for data in words:
                        if data not in stop_words:
                            if data in ham:
                                ham[data] = ham.get(data) + 1
                            else:
                                ham[data] = 1
                            if data not in distinct:
                                distinct[data] = 1
                else:
                    spam_files += 1
                    for data in words:
                        if data not in stop_words:
                            if data in spam:
                                spam[data] = spam.get(data) + 1
                            else:
                                spam[data] = 1
                            if data not in distinct:
                                distinct[data] = 1

    return


# Calculate the probability of each word
def findProbability():
    spam_count = 0
    ham_count = 0

    #calculate total number of words in each class
    for data in spam:
        spam_count += spam.get(data)
    for data in ham:
        ham_count += ham.get(data)

    return {'spam':spam_count,'ham':ham_count}


def writeOutput(spam_count,ham_count):
    with open('nbmodel3.txt', 'w', encoding="latin1") as out:
        total =(len(spam) + len(ham))
        out.write("Spam,Total probability," + (str(spam_count)) + "\n")
        out.write("Ham,Total probability," + (str(ham_count)) + "\n")
        out.write("Unique,words," + str(len(distinct)) + "\n")
        out.write("Total,vocabulary," + str(total) + "\n")
        for data in spam:
            out.write("Spam," + data + "," + str(spam[data]) + "\n")
        for data in ham:
            out.write("Ham," + data + "," + str(ham[data]) + "\n")
    out.close()
    return


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print('Usage: python nblearn3.py <path>')
        sys.exit(1)
    main(sys.argv[1:])
    ans = findProbability()
    writeOutput(ans['spam'],ans['ham'])