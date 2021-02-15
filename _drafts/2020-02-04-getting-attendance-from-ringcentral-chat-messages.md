---
layout: post
title: "Getting attendance from Ringcentral chat messages"
date: 2020-02-04
background: '/img/posts/01.jpg'
---
# Introduction
Consider these situations. we need the attendance. 
1. We had an online lecture, and we want to get attendance of all attendees in the meeting.
2. We hosted an online meeting on Zoom, and we wish to understand the level of engagement of all attendees in a meeeting.

Here we describe a fully automated method to accomplish both these goals.
The idea is to scrape the chat messages that Zoom or Ringcentral saves on disk and make a list of attendees and give 
them a participation score. The participation score we will use is simply the ratio of the number of messages they sent 
to the host with the max number of messages sent to the host by a single attendee. We can use percentile instead but 
this score is usually enough to identify attendees with low engagement levels.

I will use Ringcentral for this demonstration but this method can easily be implemented for Zoom with modifications 
necessary for the different naming conventions.

# The process
The actual analysis is only one step but ETL of data requires some effort. So we will include ETL part also.
The analysis can be broken into 3 broad categories.
1. Get the correct meeting folder and load the chat data
2. Process the chat data
3. Merge with existing database of user emails 

If we just want to see how the chat messages are parsed, we can skip to [2](##Process the data).

## Load the data


## Process the data


# The entire code
You can also find the following code and sample chat folder and email database on GitHub

```python
def participationscoreinclass(gradebookname=None, ringcentral_dirname=None, verbose=True):

    for dirs in os.listdir(ringcentral_dirname):
        dirdate = re.findall(r'\d+-\d+-\d+', dirs)

        # if the meeting directories are found in the folder
        if len(dirdate) > 0:
            dirdate = dt.datetime.strptime(dirdate[0], '%Y-%m-%d').date()

            # get all directories within a 7 day period
            if dirdate > dt.date.today() - dt.timedelta(days=7):
                # extract coursename from the directory name
                coursename = re.findall(r'\d\d\.\d\d\.\d\d (.*?) ', dirs)
                if len(coursename) > 0:
                    coursename = coursename[0]
                    # if the last character is not a number then append a period
                    # e.g. MH240M becomes MH240.M but MH140 stays MH140
                    coursename = re.sub(r'(\D)$', r'.\1', coursename)
                    if len(re.findall(coursename, gradebookname)) > 0:
                        gradefile = gradebookname
                    else:
                        continue
                else:
                    continue
                # print(dirdate, coursename, gradefile)
                dfgradebook = pd.read_csv(gradefile)
                dfgradebook["First name"] = dfgradebook["First name"].str.lower()
                dfgradebook["Last name"] = dfgradebook["Last name"].str.lower()
                nameslist = (dfgradebook["First name"] + dfgradebook["Last name"])
                nameslist = list(map(lambda x: re.sub(r' ', '', x).lower().strip(), nameslist))
                dfgradebook['names'] = nameslist
                chatfile = ringcentral_dirname + dirs + '/meeting_saved_chat.txt'

                with open(chatfile, 'r') as f:
                    chatdata = f.read()
                chat_msg_participant_occurence = list(map(lambda x: re.sub(r' To.*| ', '', x).lower().strip(),
                                                          re.findall(r'From (.*?) :', chatdata)))
                participation_count = []
                for p in dfgradebook['names']:
                    count = 0
                    for x in chat_msg_participant_occurence:
                        # print(p, x)
                        if len(re.findall(x, p)) > 0:
                            # print("Found")
                            count = count + 1
                        elif len(re.findall(p, x)) > 0:
                            # print("Found")
                            count = count + 1
                    participation_count.append(count)
                dfgradebook['participation_count'] = participation_count
                max_msgs = dfgradebook['participation_count'].max()
                dfgradebook['participation_pct'] = np.round(dfgradebook['participation_count']/max_msgs*100, 0)
                dfparticipationscore = dfgradebook[["Last name", "First name", 'Email address', 'participation_count',
                                                    'participation_pct']]
                if verbose:
                    helpersmoodle.printdataframe(dfparticipationscore)
                return dfparticipationscore
    print("="*100)
    print("No directory for saved chat messages found. Make sure you copy the directory.")
    print("="*100)

    return pd.DataFrame()