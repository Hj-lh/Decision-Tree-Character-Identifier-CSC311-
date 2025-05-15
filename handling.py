import pandas as pd
import math

class Node:
    def __init__(self, question=None, names=None):
        self.question = question
        self.left = None
        self.right = None
        self.names = names 



def info_gain(df, indices, attribute, value):
    N = len(indices)
    if N == 0:
        return 0
    
    #split
    yes_indices = [i for i in indices if df.loc[i, attribute] == value]
    no_indices = [i for i in indices if df.loc[i, attribute] != value]




    n_yes = len(yes_indices)
    n_no  = len(no_indices)


    # calculate pre-split etnropy log2(length) for parent
    before_split = math.log2(N)

    # calculate entropy for children
    e_yes = math.log2(n_yes) if n_yes > 0 else 0
    e_no = math.log2(n_no) if n_no > 0 else 0

    #avg 
    weight_e = (n_yes/N)*e_yes + (n_no/N)*e_no

    gain = before_split - weight_e 
    return gain



def find_best_question(df, indices):
    attributes = ['Gender', 'Alive', 'Age Group', 'Famous For', 'Nationality', 'Religion', 'Royalty']
    best_gain = 0
    best_question = None

    for attr in attributes:
        values = []
        for i in indices:
            v = df.loc[i, attr]
            if v not in values:
                values.append(v)
        
        for val in values:
            gain = info_gain(df, indices, attr, val)
            if gain > best_gain:
                best_gain = gain
                best_question = (attr, val)

    return best_question


def build_tree(df, indices, depth=0, max_depth=20):
    if depth >= max_depth or len(indices) <= 1:
        leaf_names = [df.loc[i, 'Name'] for i in indices]
        return Node(names=leaf_names)
    
    best_question = find_best_question(df, indices)
    if best_question is None:
        leaf_names = [df.loc[i, 'Name'] for i in indices]
        return Node(names=leaf_names)
    
    attribute, value = best_question

    yes_inds = [i for i in indices if df.loc[i, attribute] == value]
    no_inds  = [i for i in indices if df.loc[i, attribute] != value]

    node = Node(question=best_question,names=[df.loc[i, 'Name'] for i in indices])
    node.left  = build_tree(df, yes_inds, depth + 1, max_depth)
    node.right = build_tree(df, no_inds,  depth + 1, max_depth)

    return node


def format_question(attr, val):
    if attr == 'Gender':
        return f"Is your character {val.lower()}?"
    if attr == 'Alive':
        return "Is this person still alive?" if val == 'Yes' else "Has this person passed away?"
    if attr == 'Age Group':
        return f"Is your character in the {val}?"
    if attr == 'Famous For':
        return f"Is this person known for {val.lower()}?"
    if attr == 'Nationality':
        return f"Is this person from {val}?"
    if attr == 'Religion':
        return f"Does this person follow {val}?"
    if attr == 'Royalty':
        return "Is this person a member of a royal family?" if val == 'Yes' else "Is this person not part of any royal house?"



def play_game(root, df):
    current = root
    count = 0

    print(f"Starting with {len(current.names)} possible characters.")


    while current.question is not None:
        attr, val = current.question
        q_form = format_question(attr, val)
        count += 1
        print(f"Possible characters: {len(current.names)}")

        ans = input(f"Q{count}: {q_form}").lower()
        while ans not in ('yes','y','no','n'):
            ans = input("Please answer 'yes' or 'no': ").lower()

        positive = ans in ('yes','y')

        current = current.left if positive else current.right
        print(f"After question {count}, {len(current.names)} possible remain.")

    if len(current.names) == 1:
        print(f"The character is {current.names[0]}. It took {count} questions.")
    else:
        print(f"Reached max depth; {len(current.names)} possibilities remain:")
        print(", ".join(current.names))

    optimal = math.ceil(math.log2(len(df)))
    worst   = len(df)

    print(f"Optimal best-case would be {optimal} questions.")
    print(f"The theoretical worst-case would be {worst} questions.")


    return count






def main():
    df = pd.read_csv('311CSC_Dataset.csv')
    indices = list(range(len(df)))
    root = build_tree(df, indices)
    play_game(root, df)



if __name__ == "__main__":
    main()



