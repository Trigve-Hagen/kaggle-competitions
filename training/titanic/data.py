# Logistic Regression from scratch - https://www.youtube.com/watch?v=Jj7WD71qQWE&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja

import os
import re
import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

def getTitanicData():
    script_dir = Path(__file__).parent
    TRAIN = script_dir / "dataset" / "train.csv"
    TEST = script_dir / "dataset" / "test.csv"
    train = pd.read_csv(TRAIN)
    test = pd.read_csv(TEST)

    # Save for submission and training respectively
    passenger_id = test['PassengerId']
    target = train['Survived']

    # Drop PassengerId on both copies
    for df in [train, test]:
        df.drop('PassengerId', axis=1, inplace=True)

    # Concatenate the train and test data into one big dataframe for uniformity
    all_data = pd.concat([train.drop('Survived',axis=1), test]).reset_index(drop=True)

    # Save indexes for splitting all_data later on
    ntrain = train.shape[0]
    ntest = test.shape[0]

    # start by creating a feature for family size to thin out the amount of columns.
    # It more of a choice to include or exclude the passenger in this feature.
    # It is also advisable drop SibSip and/or Parch to avoid the features being too
    # correlated

    # Create FamSize feature and drop
    all_data['FamSize'] = 1 + all_data['SibSp'] + all_data['Parch']
    all_data.drop(['SibSp','Parch'], axis=1, inplace=True)

    # Lets explore what features contain missing data (NaN or Null)
    # so we can then work on each feature individually
    total_miss = all_data.isnull().sum()
    percent_miss = (total_miss/all_data.isnull().count()*100)

    # Creating dataframe from dictionary
    missing_data = pd.DataFrame({'Total missing':total_miss, '% missing':percent_miss})
    # print(missing_data.sort_values(by='Total missing', ascending=False).head())

    # print(all_data[all_data['Embarked'].isnull()])

    # Find the percentage of each value in Embarked
    value_percentages = all_data['Embarked'].value_counts(normalize=True) * 100
    # print("Percentage of Embarked unique values:")
    # print(value_percentages)

    # Oround 70% of passengers embarked at Southampton (S) or (C)
    _ = all_data._set_value(61,'Embarked',value='S')
    _ = all_data._set_value(829,'Embarked',value='S')

    # Empty DataFrame
    # print(all_data[all_data['Embarked'].isnull()])

    # It seems as if these entries were people who either worked in the Titanic or
    # their ticket was paid for.
    # Philadelphia's westbound voyage was cancelled, with Storey and several other
    # shipmates; Andrew Shannon [Lionel Leonard], August Johnson,
    # William Henry Törnquist, Alfred Carver and William Cahoone Johnson) forced to
    # travel aboard Titanic as passengers.
    # print(all_data[all_data['Fare'].isnull()])

    # Add him to the list of employees whoes fare was paid for
    _ = all_data._set_value(1043,'Fare',value=0)

    # People who worked on the ship
    # print(all_data[all_data['Fare']==0])

    # Find the percentage of each value in Fare
    # value_percentages = all_data['Fare'].value_counts(normalize=True) * 100
    # print("Percentage of Fare unique values:")
    # print(value_percentages)

    splits = 5
    # for i in range(splits):
    #   print(f'Group {i+1}:', pd.qcut(all_data['Fare'], splits).sort_values().unique()[i])

    def discretize_fare(val):
        fare_group = pd.qcut(all_data['Fare'], splits).sort_values().unique()

        for i in range(splits):
            if val in fare_group[i]:
                return i+1
            elif np.isnan(val):
                return val

    all_data['Fare'] = all_data['Fare'].apply(discretize_fare)
    all_data['Fare'] = all_data['Fare'].fillna(5).astype(int)

    # for i in range(splits):
    #   print(f'Group {i+1}:', pd.qcut(all_data['Age'].dropna(), splits).unique()[i])

    def discretize_age(val):
        age_group = pd.qcut(all_data['Age'], splits).sort_values().unique()

        for i in range(splits):
            if val in age_group[i]:
                return i+1
            elif np.isnan(val):
                return 0

    all_data['Age'] = all_data['Age'].apply(discretize_age).astype(int)

    # print(all_data.head())

    # Search for titles and make a Title column
    def get_title(name):
        title_search = re.search(r'([A-Za-z]+)\.', name)
        # If the title exists, extract and return it.
        if title_search:
            return title_search.group(1)
        return ""

    all_data['Title'] = all_data['Name'].apply(get_title)

    # print(all_data['Title'].unique())

    # Master: boys and young men
    # Don/Donna/Lady/Sir/Countess/Jonkheer: royal or high profile title
    # Rev: reverend, priest
    # Mme/Ms: woman of unknown marrital status (usually unmarried)
    # Major/Col/Capt: military title
    # Mlle: married woman

    # With this we can make the following replacements:
    all_data['Title'] = all_data['Title'].replace(['Ms','Mlle'],'Miss')
    all_data['Title'] = all_data['Title'].replace('Mme','Mrs')
    all_data['Title'] = all_data['Title'].replace(['Don','Dona','Lady','Sir',
                                                    'Countess','Jonkheer'],'Royal')
    all_data['Title'] = all_data['Title'].replace(['Rev','Major','Col','Capt','Dr'],'Other')



    # plt.figure(figsize=(10,4))
    # sns.stripplot(x='Title',y='Age',data=all_data[all_data['Age']!=0],
    #               hue='Pclass',dodge=True)
    # plt.legend(loc=1)
    # plt.show()

    # Fill the missing age group values. We have to options here, to either fill
    # with the mean for each (very) specific category, or filling randomly.
    # Lets try filling with the mean
    def impute_age(row):

        # Features from row
        pclass = row['Pclass']
        title = row['Title']
        age = row['Age']

        if age == 0:
            return int(round(all_data.loc[(all_data['Age']!=0)&
                                        (all_data['Pclass']==pclass)&
                                        (all_data['Title']==title)]['Age'].mean(),1))
        else:
            return age

    all_data['Age'] = all_data.apply(impute_age,axis=1)

    # Change Cabin for Deck, and fill the empty values with a placeholder 'N'
    _ = all_data.rename({'Cabin':'Deck'},axis=1,inplace=True)
    all_data['Deck'] = all_data['Deck'].fillna('N')

    # Grab the first letter of each cabin code, which is the deck level where
    # the cabin is located
    def cabin_to_deck(row):
        return row['Deck'][0]

    all_data['Deck'] = all_data.apply(cabin_to_deck,axis=1)

    ticket_list = []
    for ticket_id in list(all_data['Ticket'].unique()):

        # count = all_data[all_data['Ticket']==ticket_id].count()[0]
        count = len(all_data[all_data['Ticket']==ticket_id])
        decks = all_data[all_data['Ticket']==ticket_id]['Deck']
        empty_decks = (decks=='N').sum()

        if (count > 1) and (empty_decks > 0) and (empty_decks < len(decks)):
            ticket_list.append(ticket_id)

    # print(ticket_list)

    # So now that we have these ticket IDs, we can explore the dataset and see if
    # we can fill any Deck values individually, that is with the help of
    # [2] (cabin reference)
    # Show dataframes with the previous specifications
    # for ticket in ticket_list:
    #     print(all_data[all_data['Ticket']==ticket])

    # ticket ID, information

    # 2668, 2 siblings (sharing with mother)
    _ = all_data._set_value(533,'Deck',value=all_data.loc[128]['Deck'])
    _ = all_data._set_value(1308,'Deck',value=all_data.loc[128]['Deck'])

    # PC 17755, maid to Mrs. Cardeza
    _ = all_data._set_value(258,'Deck',all_data.loc[679]['Deck'])

    # PC 17760, manservant to Mrs White
    _ = all_data._set_value(373,'Deck',value='C')

    # 19877, maid to Mrs Cavendish
    _ = all_data._set_value(290,'Deck',value=all_data.loc[741]['Deck'])

    # 113781, maid and nurse to the Allisons
    _ = all_data._set_value(708,'Deck',value=all_data.loc[297]['Deck'])
    _ = all_data._set_value(1032,'Deck',value=all_data.loc[297]['Deck'])

    # 17421, maid to Mrs Thayer
    _ = all_data._set_value(306,'Deck',value='C')

    # PC 17608, governess (teacher) to Master Ryerson
    _ = all_data._set_value(1266,'Deck',value=all_data.loc[1033]['Deck'])

    # 36928, parents (sharing with daughters)
    _ = all_data._set_value(856,'Deck',value=all_data.loc[318]['Deck'])
    _ = all_data._set_value(1108,'Deck',value=all_data.loc[318]['Deck'])

    # PC 17757, maid and manservant to the Astors
    _ = all_data._set_value(380,'Deck',value='C')
    _ = all_data._set_value(557,'Deck',value='C')

    # PC 17761, maid to Mrs Douglas, occupied room with another maid
    _ = all_data._set_value(537,'Deck',value='C')

    # 24160, maid to Mrs. Robert, testimony that she was on deck E
    _ = all_data._set_value(1215,'Deck',value='E')

    # S.O./P.P. 3, very little information, will assume on deck E with Mrs. Mack
    _ = all_data._set_value(841,'Deck',value=all_data.loc[772]['Deck'])

    # fig,ax = plt.subplots(1,2,figsize = (10,4))
    # plt.tight_layout(w_pad=2)
    # ax = ax.ravel()

    # Missing Deck based on Pclass
    # Lets check were out passengers were situated based on Pclass
    # sns.countplot(x='Pclass',data=all_data[all_data['Deck']!='N'],hue='Deck',ax=ax[0])
    # ax[0].legend(loc=1)
    # ax[0].set_title('Pclass count for known Deck')
    # sns.countplot(x='Pclass',data=all_data[all_data['Deck']=='N'],hue='Deck',ax=ax[1])
    # ax[1].set_title('Pclass count for unkown Deck')
    # plt.show()

    # Accoring to our reference [2], 3rd class passengers were on the lower levels
    # of the Titanic, mainly E,F, and G decks. Let's start by making lists of the
    # possible decks each passenger might have belonged to based on their Pclass

    # Note: The reference also states that the T deck was unique, and only one
    # person was housed there.

    decks_by_class = [[],[],[]]
    for i in range(3):
        decks_by_class[i] = list(all_data[all_data['Pclass']==i+1]['Deck'].unique())
        # print(f'Pclass = {i+1} decks:',decks_by_class[i])

    # Pclass = 1 decks: ['C', 'E', 'A', 'N', 'B', 'D', 'T']
    # Pclass = 2 decks: ['N', 'D', 'F', 'E']
    # Pclass = 3 decks: ['N', 'G', 'F', 'E']

    # Removing null ('N') entries and single 'T' cabin
    for i in range(3):
        if 'N' in decks_by_class[i]:
            decks_by_class[i].remove('N')
        if 'T' in decks_by_class[i]:
            decks_by_class[i].remove('T')

    # Lets also assign weights so when we select randomly from each list the
    # selections are properly distributed:

    # Note: Since we removed T from the data (which belonged to Pclass = 1),
    # we need to account for it only for that class, if not the probability will
    # not add to 1!

    weights_by_class = [[],[],[]]

    for i,deck_list in enumerate(decks_by_class):
        for deck in deck_list:
            if i == 0:
                # class_total = all_data[(all_data['Deck']!='N')&(all_data['Pclass']==i+1)].count()[0]-1
                class_total = len(all_data[(all_data['Deck']!='N')&(all_data['Pclass']==i+1)]) - 1
            else:
                # class_total = all_data[(all_data['Deck']!='N')&(all_data['Pclass']==i+1)].count()[0]
                class_total = len(all_data[(all_data['Deck']!='N')&(all_data['Pclass']==i+1)])
            # deck_total = all_data[(all_data['Deck']==deck)&(all_data['Pclass']==i+1)].count()[0]
            deck_total = len(all_data[(all_data['Deck']==deck)&(all_data['Pclass']==i+1)])
            weights_by_class[i].append(deck_total/class_total)
        # print(f'Pclass = {i+1} weights:',np.round(weights_by_class[i],3))

    # Pclass = 1 weights: [0.388 0.131 0.082 0.25  0.149]
    # Pclass = 2 weights: [0.25  0.542 0.208]
    # Pclass = 3 weights: [0.278 0.556 0.167]

    # Store tickets that were already looped with cabin position
    ticket_dict = {}
    def impute_deck(row):

        ticket = row['Ticket']
        deck = row['Deck']
        pclass = row['Pclass']

        if (deck == 'N') and (ticket not in ticket_dict):

            if pclass == 1:
                deck = list(np.random.choice(decks_by_class[0],size=1,
                                            p=weights_by_class[0]))[0]
            elif pclass ==2:
                deck = list(np.random.choice(decks_by_class[1],size=1,
                                            p=weights_by_class[1]))[0]
            elif pclass ==3:
                deck = list(np.random.choice(decks_by_class[2],size=1,
                                            p=weights_by_class[2]))[0]

            ticket_dict[ticket] = deck

        elif (deck == 'N') and (ticket in ticket_dict):
            deck = ticket_dict[ticket]

        return deck

    all_data['Deck'] = all_data.apply(impute_deck,axis=1)

    # Filtering Features

    # Now that most of the features have been used to fill missing values on other
    # features, it is time to get rid of those columns that don't provide any useful
    # information anymore:

    # print(all_data.head(1))
    all_data = all_data.drop(['Name','Ticket','Title'],axis=1)

    # Label Encoding

    # Finally, we need all features to be numerical. For this reason we will assign
    # a numerical integer value to each unique value for the string columns by using
    # pythons .map()

    all_data['Deck'] = all_data['Deck'].map({'F':0,'C':1,'E':2,
                                                'G':3,'D':4,'A':5,
                                                'B':6,'T':7}).astype(int)

    all_data['Embarked'] = all_data['Embarked'].map({'S':0,'C':1,'Q':2}).astype(int)
    all_data['Sex'] = all_data['Sex'].map( {'female':0,'male':1}).astype(int)

    # _Alone_ Feature

    # Many Kernels suggest using a feature to determine whether a passenger is
    # alone or not. After many hours of experimenting, I finally caved in and
    # created this feature, which indeed has provided me with the the best score
    # I have achieved, so lets add it to our data:

    all_data['Alone'] = 0
    all_data.loc[all_data['FamSize']==1,'Alone'] = 1

    return ntrain, ntest, train, test, all_data, target
