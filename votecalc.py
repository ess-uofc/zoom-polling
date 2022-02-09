import csv
from operator import index

results = open('poll.csv', 'r')
membersData = open('bod-voting-members.csv', 'r')

type(results)
type(membersData)

csvreader = csv.reader(results)

rows = []

votes = 0

for row in csvreader:
    if (csvreader.line_num >= 7) & (len(row) > 1):
        rows.append(row)

results.close()

membersreader = csv.reader(membersData)

members = {}
voteType = {}

sharedVotes = []

def validVote(vote):
    if vote == "":
        return False
    if vote in sharedVotes:
        if sharedVoteStatus[vote] == False:
            sharedVoteStatus[vote] = True
            return True
        else:
            return False
    return True

for row in membersreader:
    email = row[1].lower()
    name = row[2]
    shared = row[3]
    members[email] = name
    if shared == "TRUE":
        voteType[email] = 2
        if name not in sharedVotes:
            sharedVotes.append(name)
    else:
        voteType[email] = 1

membersData.close()

sharedVoteStatus = {}

for shared in sharedVotes:
    sharedVoteStatus[shared] = False

voteOptions = {
    "for": 1,
    "against": 2,
    "abstain": 3
}

votesFor = 0
votesAgainst = 0
votesAbstain = 0

notedFor = []
notedAgainst = []
notedAbstain = []

for vote in rows:
    memberAssociation = ""
    try:
        memberAssociation = members[vote[2].lower()]
    except:
        print("Member not authorized " + vote[2])
    
    if validVote(memberAssociation):
        voteValue = voteOptions[vote[4].lower()]
        if voteValue == 1:
            votesFor += 1
            if vote[5] == "Yes":
                notedFor.append(memberAssociation)
        elif voteValue == 2:
            votesAgainst += 1
            if vote[5] == "Yes":
                notedAgainst.append(memberAssociation)
        elif voteValue == 3:
            votesAbstain += 1
            if vote[5] == "Yes":
                notedAbstain.append(memberAssociation)

result_strings = ["Motion Results:\n", "For: " + str(votesFor), "\nAgainst: " + str(votesAgainst), "\nAbstain: " + str(votesAbstain)]

is_noted = False

# if len(notedFor) > 1:
#     if not is_noted:
#         result_strings.append("\n")
#         result_strings.append("\nNoted Votes:\n")
#         is_noted = True
#     formatted_string = "\nFor: "
#     for n in notedFor:
#         formatted_string += n +", "
#     result_strings.append(formatted_string)

if len(notedAgainst) > 1:
    if not is_noted:
        result_strings.append("\n")
        result_strings.append("\nNoted Votes:\n")
        is_noted = True
    formatted_string = "\nAgainst: "
    for n in notedAgainst:
        formatted_string += n +", "
    result_strings.append(formatted_string)

if len(notedAbstain) > 1:
    if not is_noted:
        result_strings.append("\n")
        result_strings.append("\nNoted Votes:\n")
        is_noted = True
    formatted_string = "\nAbstain: "
    for n in notedAbstain:
        formatted_string += n +", "
    result_strings.append(formatted_string)

output_file = open("motionresults.txt", "w")
output_file.writelines(result_strings)
output_file.close()
print(result_strings)

# print(rows)