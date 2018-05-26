#### Part One

import codecademylib
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency


# Loading the Data
species = pd.read_csv('species_info.csv')


# print species.head()
print (species.head())


# count various values
species_count = species.scientific_name.nunique()

species_type = species.category.unique()

conservation_statuses = species.conservation_status.unique()


# Use groupby to count how many scientific_name falls into each conservation_status criteria
conservation_counts = species.groupby('conservation_status')\
                      .scientific_name.nunique().reset_index()

print conservation_counts


# Replace NaN in our DataFrame with 'No Intervention'
species.fillna('No Intervention', inplace = True)


# Now run the same groupby as before to see how many species require No Intervention.
conservation_counts_fixed = species.groupby('conservation_status')\
                             .scientific_name.nunique().reset_index()

print conservation_counts_fixed


# Create a new DataFrame called protection_counts, which is sorted by scientific_name
species = pd.read_csv('species_info.csv')

species.fillna('No Intervention', inplace = True)

protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')

    
# Now let's create a bar chart!    
plt.figure(figsize=(10, 4))

ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.xlabel = 'Conservation Status'
plt.title('Conservation Status by Species')

plt.show()


####

species = pd.read_csv('species_info.csv')

species.fillna('No Intervention', inplace = True)


# Create a new column in species called is_protected
species['is_protected'] = species.conservation_status != 'No Intervention'


# Now group by both category and is_protected
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()


# Examine category_counts.head()
print category_counts.head()

category_pivot = category_counts.pivot(columns='is_protected',
                      index='category',
                      values='scientific_name')\
                      .reset_index()

  
# Examine category_pivot
print category_pivot


# Rename the categories True and False to something more descriptive
category_pivot.columns = ['category',
                        'not_protected',
                        'protected']


# Let's create a new column in category_pivot called percent_protected
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)


####

# You now have the endangered species data pivoted in the table below. 
# Let's see if we can use it to answer the question "are certain types of species more likely to be endangered?".

# Create a table called contingency and fill it with the correct values.
contingency1 = [[30, 146],
                [75, 413]]

contingency2 = [[30, 146],
                [5, 73]]


# In order to perform our chi-squared test, we'll need to import the correct function from scipy
from scipy.stats import chi2_contingency


# Run chi2_contingency on the contingency table
chi2, pval1, dof, expected = chi2_contingency(contingency1)
print pval1

chi2, pval_reptile_mammal, dof, expected = chi2_contingency(contingency2)
print pval_reptile_mammal


#### Part Two

import codecademylib
import pandas as pd
from matplotlib import pyplot as plt

species = pd.read_csv('species_info.csv')
species.fillna('No Intervention', inplace = True)
species['is_protected'] = species.conservation_status != 'No Intervention'


# Load observations.csv into a variable called observations.
observations = pd.read_csv('observations.csv')


# Inspect the first couple rows of observations
print (observations.head())


# Use apply and a lambda function to create a new column in species 
# called is_sheep which is True if the common_names contains 'Sheep', and False otherwise
species['is_sheep'] = species.common_names.apply(lambda x: True if \
                                                 'Sheep' in x else False)


# Select the rows of species where is_sheep is True and save it to the variable species_is_sheep.
species_is_sheep = species[species.is_sheep == True]


#Print species_is_sheep and inspect the results.
print species_is_sheep


# Many of the results are actually plants. 
# Select the rows of species where is_sheep is True and category is Mammal
sheep_species = species[(species.is_sheep == True) &\
                        (species.category == 'Mammal')]


# Print and inspect sheep_species.
print sheep_species


# Now merge sheep_species with observations to get a DataFrame with observations of sheep.
sheep_observations = pd.merge(sheep_species, observations)


# Print and inspect the first couple rows of sheep_observations using .head().
print(sheep_observations.head())


# How many total sheep sightings (across all three species) were made at each national park?
obs_by_park = sheep_observations.groupby('park_name')\
								.observations.sum().reset_index()


# Print obs_by_park.
print obs_by_park


#####

import codecademylib
import pandas as pd
from matplotlib import pyplot as plt

species = pd.read_csv('species_info.csv')
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

observations = pd.read_csv('observations.csv')

sheep_observations = observations.merge(sheep_species)

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()


# Create a bar chart showing the different number of observations per week at each park.
plt.figure(figsize=(10, 4))

ax = plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')

plt.show()


# last year it was recorded that 15% of sheep at Bryce National Park have foot and mouth disease.
#  calculate the number of sheep that they would need to observe from each park
# to make sure their foot and mouth percentages are significant.

# What is the baseline percentage of this sample size determination?
baseline = 0.15


# Calculate "Minimum Detectable Effect".
minimum_detectable_effect = 0.333
sample_size_per_variant = 870


# How many weeks would the scientists need to spend at Yellowstone National Park to observe enough sheep?
yellowstone_weeks_observing = sample_size_per_variant / 507


# The scientists also want to repeat their measurements at Bryce National Park.
bryce_weeks_observing = sample_size_per_variant / 250


