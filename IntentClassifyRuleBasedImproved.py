import sys, re
from NLURuleBased import NLURuleBased
import ipdb
from sklearn.metrics import f1_score

def get_data_from_annotated_file(data_file, annotated_data_file):
    labels = []
    instances = []
    gold_annotations = []

    with open(data_file) as df:
        data_lines = df.readlines()[1:]

    with open(annotated_data_file) as adf:
        annotated_data_lines = adf.readlines()[1:] 

    for i in range(len(data_lines)):
        data_line = data_lines[i]
        annotated_data_line = annotated_data_lines[i]

        #ipdb.set_trace()
        _, _, instance = (' '.join(data_line.split())).split(" ", 2)
        instance = instance.rstrip()

        label = annotated_data_line.split()[0]
        #ipdb.set_trace()
        gold_annotation = annotated_data_line.split("\t", 1)[1]

        labels.append(label)
        instances.append(instance)
        gold_annotations.append(gold_annotation)

    return labels, instances, gold_annotations

def get_data(data_file):
    labels = []
    instances = []

    with open(data_file) as df:
        data_lines = df.readlines()[1:]

    for line in data_lines:
        label, instance = line.split('\t')
        instance = instance.rstrip()

        labels.append(label)
        instances.append(instance)

    return labels, instances


def annotate_data0():
    data0file = "shared-filtered"
    with open(data0file) as d0f:
        d0lines = d0f.readlines()
    for line in d0lines:
        annotation = NLU.parse(line)
        print(annotation)
        NLU.printSemanticFrame()
        NLU.clear_slots()

def annotate_data(NLU, data_file, gold_file):
    annotations = []
    pred_labels = []

    #data_file_5_1 = "DATA5/part1.tsv"
    #data_file_5_1_annotated = "DATA5/part1_annotated.tsv"
    #data_file_5_2 = "DATA5/part2.tsv"
    #data_file_5_2_annotated = "DATA5/part2_annotated.tsv"
    #data_file_6_1 = "DATA6/part1.tsv"
    #data_file_6_1_annotated = "DATA6/part1_annotated.tsv"
    #data_file_6_2 = "DATA6/part2.tsv"
    #data_file_6_2_annotated = "DATA6/part2_annotated.tsv"

    #data_5_1_labels, data_5_1_instances = get_data_from_annotated_file(data_file_5_1, data_file_5_1_annotated)
    #data_5_2_labels, data_5_2_instances = get_data_from_annotated_file(data_file_5_2, data_file_5_1_annotated)
    #data_6_1_labels, data_6_1_instances = get_data_from_annotated_file(data_file_6_1, data_file_5_1_annotated)
    #data_6_2_labels, data_6_2_instances = get_data_from_annotated_file(data_file_6_2, data_file_5_1_annotated)


    #true_labels = data_5_1_labels + data_5_2_labels + data_6_1_labels + data_6_2_labels
    #instances = data_5_1_instances + data_5_2_instances + data_6_1_instances + data_6_2_instances

    #true_labels = data_5_1_labels + data_5_2_labels
    #instances = data_5_1_instances + data_5_2_instances

    #true_labels = data_6_1_labels + data_6_2_labels
    #instances = data_6_1_instances + data_6_2_instances

    #true_labels, instances = get_data(data_file)
    true_labels, instances, gold_annotations = get_data_from_annotated_file(data_file, gold_file)

    pred_labels = []
    annotations = []
    for instance in instances:
        annotation = NLU.parse(instance)
        annotations.append(annotation)
        pred_label = NLU.SemanticFrame.Intent.name
        pred_labels.append(pred_label)

    return annotations, pred_labels, true_labels, instances, gold_annotations

def accuracy(pred_labels, true_labels):
    correct =  sum(pred_labels[i] == true_labels[i] for i in range(len(pred_labels)))
    total = len(pred_labels)

    return float(correct) / float(total)

def f1_for_slot(slots, gold_slots, instances):
    #ipdb.set_trace()

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    N = len(slots)
    for i in range(N):
        slot_set = set(slots[i])
        gold_slot_set = set(gold_slots[i])

        for s in slots[i]:
            if s in gold_slot_set:
                TP += 1
            else:
                FP += 1

        for s in gold_slots[i]:
            if s not in slots:
                FN += 1



def main():
    NLU = NLURuleBased()
    data_file = sys.argv[1]
    gold_file = sys.argv[2]

    annotations, pred_labels, true_labels, instances, gold_annotations = annotate_data(NLU, data_file, gold_file)

    # Intent
    acc = accuracy(pred_labels, true_labels)
    f1 = f1_score(pred_labels, true_labels, average="micro")

    # Slot
    slots = [sorted(list(set(re.findall(r"<\/(.*?)>", a)))) for a in annotations]
    gold_slots = [sorted(list(set(re.findall(r"<\/(.*?)>", g)))) for g in gold_annotations]
    #ipdb.set_trace()

    slot_acc = accuracy(slots, gold_slots)
    #slot_f1 = f1_for_slot(slots, gold_slots, instances)

    #ipdb.set_trace()
    for i in range(len(true_labels)):
        print("instance: {}\tpred label: {}\ttrue label {}".format(i, pred_labels[i], true_labels[i]))
        print("annotation: {}\n".format(annotations[i]))
        print("gold_annotation {}\n".format(gold_annotations[i]))

    print("intent accuracy on data: ", acc)
    print("intent f1 score on data: ", f1)
    print("slot accuracy on data: ", slot_acc)
    #ipdb.set_trace()

    print("Rule based NLU - enter query:")

    while(True):
        inputStr = input("> ")
        if (inputStr == "Quit"):
            break
        annotation = NLU.parse(inputStr)
        #ipdb.set_trace()
        print("Predicted Intent: ", NLU.SemanticFrame.Intent.name)
        print("Predicted Slot annotation: ", annotation)
        NLU.clear_slots()

if __name__ == '__main__':
    main()