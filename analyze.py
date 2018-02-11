'''

    A python script to scrape the data from the Computing Cares
    EECS 281 Survey and put it into a manageable form.

'''


import csv
import numpy as np
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
import heapq
import re
import string



response_enum = {
    'Strongly Agree': 5,
    'Agree': 4,
    'Neutral': 3,
    'Disagree': 2,
    'Strongly Disagree': 1
}



'''

    Identify the n most frequently used words in the comments
    section of the survey, without stopwords.

'''
def find_most_common_words(comments):

    # First, get the formatting correct.
    responses = [x.lower() for x in comments.keys()]

    # Add some custom stopwords.
    stop = stopwords.words('english')
    stop.extend(['i\'m', 'really', 'i\'ve', 'lot', 'heard', 'also', 'get'])

    # Now we can strip out all of the stopwords.
    stripped = [' '.join(filter(lambda x: x not in stop, r.split())) for r in responses]


    # Find the frequencies of the remaining words.
    frequencies = {}
    for msg in stripped:

        for word in msg.split():
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1


    print('Twenty most common words in the dataset (stripped of nltk.stopwords):')
    print(heapq.nlargest(20, frequencies, key=frequencies.get))    
    




'''

    Print a bunch of information about the data.

'''
def print_output(questions):

    question_id = 0
    for question in questions:
        
        # We don't need those
        if question['question'] == 'ID':
            continue

        print(str(question_id) + ': ' + question['question'])

        get_mean = False

        # Print the answers and their frequencies. Also
        # see if we should get the mean of the answers.
        for key in sorted(question['answers'].keys()):
            print('\t' + str(key) + ': ' + str(question['answers'][key]))
            if key != '':
                if key[0] == '1' and question['question'] != 'ID':
                    get_mean = True

        # lol
        if question_id == 7:
            get_mean = False

        # Use the responses enumeration for the 'Strongly Agree' etc. answers
        if question_id >= 8 and question_id < 19:
            nums = []

            for key, value in question['answers'].items():
                nums.extend([response_enum[key] for i in range(value)])

            print('\n\tMean: ' + str(np.mean(nums)))


        if get_mean:
            nums = []
            
            for key, value in question['answers'].items():
                if key != '' and  key[0].isdigit():
                    nums.extend(int(key[0]) for i in range(value))

            print('\n\tMean: ' + str(np.mean(nums)))


        question_id += 1
        print('\n\n')

    # Find the 20 most common words in the comments section.
    find_most_common_words(questions[48]['answers'])


'''

    Add an answer to the answers dictionary
    for a specific question.

'''
def add_to_answers(questions, question_index, answer):
    if answer not in questions[question_index]['answers']:
         questions[question_index]['answers'][answer] = 1
    else:
        questions[question_index]['answers'][answer] += 1


'''

    A function to help discover cross-column trends.

    Currently:
        How do men vs women respond to a question about equal
        opportunities for men vs women in industry?

    Ignore how shitty this looks I hate matplotlib haha

'''
def analyze(students):

    answers = {'Man': {}, 'Woman': {}}
    num_men = 0 
    num_women = 0

    question_one = 59
    question_two = 11

    for student in students:
        if student[question_one] in answers:
            if student[question_two] not in answers[question_one]:
                answers[student[question_one]][student[question_two]] = 1
            else:
                answers[student[question_one]][student[question_two]] += 1

            if student[question_one] == 'Man': num_men += 1
            elif student[question_one] == 'Woman': num_women += 1

    print(answers)

    men = [0] * 5
    women = [0] * 5
    for gender, responses in answers.items():
        g = []

        for response, freq in responses.items():
            g.extend([response_enum[response] for i in range(freq)])

        print(str(gender) + ' mean: ' + str(np.mean(g)))

        for response in responses.keys():
            if gender == 'Man':
                men[response_enum[response] - 1] = answers[gender][response] / num_men
            else:
                women[response_enum[response] - 1] = answers[gender][response] / num_women
            print(str(gender) + ' ' + str(response) + ': ' + str(answers[gender][response] / (num_men if gender == 'Man' else num_women)))
        
    print(men)
    print(women)

            
    x = [men, women]

    y_axis = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

    p1 = plt.bar([0.8, 1.8, 2.8, 3.8, 4.8], men, width = 0.2)
    p2 = plt.bar([1, 2, 3, 4, 5], women, tick_label=y_axis, width = 0.2)

    plt.legend((p1, p2), ('Men', 'Women'))
    plt.xlabel('Response')
    plt.ylabel('Proportion per Indicated Gender (Male, Female)')
    plt.title('Responses by Indicated Gender to Equal Opportunity for Women in Industry') 
    # plt.show()




'''

    Read a CSV file and take some stats.

'''
def main(filename):
    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        questions = []
        students = []
        
        # Grab the header (contains the questions)
        header = next(reader)

        # Create a dictionary for each question.
        for question in header:
            questions.append({ 'question': question, 'answers': { } })

        questions[0]['question'] = 'ID'

        # Iterate over each students response.
        for line in reader:
            question_index = 0

            # Save the bulk response for dealing
            # with more intricate stats later on.
            students.append(line)


            for answer in line:
                
                # For certain questions we want to break on commas again (bad CC formatting)
                if question_index == 2 or question_index == 55 or question_index == 50:
                    for sep in answer.split(','):
                        add_to_answers(questions, question_index, sep if sep[0] != ' ' else sep[1:])

                else:
                    add_to_answers(questions, question_index, answer)
                        
                question_index += 1


        # analyze(students)
        print_output(questions) 




if __name__ == '__main__':

    main('EECS281_stripped.csv')




'''
Index: 0 Question: ID
Index: 1 Question: Do you prefer to study/work on projects by yourself or with other students?
Index: 2 Question: Why did you choose to take this course?
Index: 3 Question: How comfortable do you feel entering this course?
Index: 4 Question: At this point, I think that most students in this course know...
Index: 5 Question: How confident are you in your ability to be successful in this course?
Index: 6 Question: What grade do you hope to obtain?
Index: 7 Question: How confident are you in obtaining that grade?
Index: 8 Question: How many hours per week do you expect to spend outside of class on work for this course?
Index: 9 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I believe Computer Science can make a positive impact n the world.]
Index: 10 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I believe Computer Science helps people.]
Index: 11 Question: How much do you agree or disagree with the following statements about Computer Science in general? [After graduation, there are equal opportunities for a career in Computer Science for male and females alike.]
Index: 12 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I believe that knowledge about Computer Science will be more important in the future than it is now.]
Index: 13 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I believe that having a career in Computer Science is as compatible as any other career with having a quality family life.]
Index: 14 Question: How much do you agree or disagree with the following statements about Computer Science in general? [My opinion of Computer Science is representative of those of my gender.]
Index: 15 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I find Computer Science intimidating.]
Index: 16 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I can see myself in a computing-related career in the future.]
Index: 17 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I can see myself as a Computer Scientist in the future.]
Index: 18 Question: How much do you agree or disagree with the following statements about Computer Science in general? [Someone who takes CS courses beyond this one will be a coder for the rest of their life.]
Index: 19 Question: How much do you agree or disagree with the following statements about Computer Science in general? [I believe that other students in Computer Science will be welcoming of me.]
Index: 20 Question: How many formal programming courses have you completed?
Index: 21 Question: Have you completed any informal programming study (online, book, etc) on your own?
Index: 22 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Faculty/teachers praised the quality of your academic work]
Index: 23 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [You were offered special academic resources or opportuinities]
Index: 24 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Faculty/teachers let you know your ideas are valuable]
Index: 25 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Faculty/teachers let you know that they are confident you will complete your college studies succesfully]
Index: 26 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Family or friends praised your academic achievements]
Index: 27 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Family or friends would praise and value your ideas]
Index: 28 Question: How frequently would you say you received the following types of encouragement since you began high school? Please give your general impression. [Family or friends let you know that they are confident you will complete your college studies succesfully]
Index: 29 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel a sense of choice and freedom in what I undertake]
Index: 30 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel capable at what I do]
Index: 31 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I really like the people I interact with]
Index: 32 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel confident that I can do things well]
Index: 33 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel that my decisions reflect what I really want]
Index: 34 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel included in the groups that I want to belong to]
Index: 35 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel competent to achieve my goals]
Index: 36 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I get along with people I come into contact with]
Index: 37 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel my choices express who I really am]
Index: 38 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel I am doing what really interests me]
Index: 39 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [People are generally pretty friendly towards me]
Index: 40 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel I can successfully complete difficult tasks]
Index: 41 Question: Thinking about your experiences in your undergraduate studies so far, please indicate how true each statement is for you on a scale of 1 (Not at all true) to 5 (Extremely true). [I feel optimistic about my career prospects after I complete my education]
Index: 42 Question: How would you describe your current mental and physical health? [Mental health]
Index: 43 Question: How would you describe your current mental and physical health? [Physical health]
Index: 44 Question: How often DURING THE LAST MONTH did you: [Feel that you were unable to control the important things in your life]
Index: 45 Question: How often DURING THE LAST MONTH did you: [Feel confident about your ability to handle problems]
Index: 46 Question: How often DURING THE LAST MONTH did you: [Feel that things were going your way]
Index: 47 Question: How often DURING THE LAST MONTH did you: [Feel that difficulties were piling up so high that you couldn't control them]
Index: 48 Question: What do you expect from this course?
Index: 49 Question: Have you officially declared a major?
Index: 50 Question: What is your (intended) major?
Index: 51 Question: How interested are you in a CS/CE major?
Index: 52 Question: How interested are you in a CS/CE minor?
Index: 53 Question: Have you met with an undergraduate advisor in the past 6 months?
Index: 54 Question: What do you intend to do after you receive your undergraduate degree?
Index: 55 Question: What type of employment would you like to hold after completing your education?
Index: 56 Question: In which state/country were you born?
Index: 57 Question: Are you an international student?
Index: 58 Question: What is your first language?
Index: 59 Question: What is your current gender identity?
Index: 60 Question: Do you consider yourself to be a part of the lesbian, gay, bisexual, transgender, plus (LGBT+) community?
Index: 61 Question: What is your race or ethnicity
Index: 62 Question: Are you a first generation undergraduate student?
Index: 63 Question: Which of the following best describes your family's financial situation most of the time when you were growing up
Index: 64 Question: Are you currently in a committed relationship (e.g., marriage, domestic partnership)?
Index: 65 Question: Do you have children?
'''
