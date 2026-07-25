import pandas as pd


def calculate_demographic_data(print_data=True):
    # 1. Lecture du fichier CSV
    df = pd.read_csv('adult.data.csv')

    # 2. Nombre de personnes par race
    race_count = df['race'].value_counts()

    # 3. Âge moyen des hommes (arrondi au dixième)
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 4. Pourcentage de personnes titulaires d'une licence (Bachelors)
    percentage_bachelors = round(
        (df['education'] == 'Bachelors').mean() * 100, 1
    )

    # 5. Advanced education (Bachelors, Masters, Doctorate)
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    # Pourcentage des personnes avec études supérieures gagnant >50K
    higher_education_rich = round(
        (df[higher_education]['salary'] == '>50K').mean() * 100, 1
    )

    # Pourcentage des personnes sans études supérieures gagnant >50K
    lower_education_rich = round(
        (df[lower_education]['salary'] == '>50K').mean() * 100, 1
    )

    # 6. Nombre minimum d'heures de travail par semaine
    min_work_hours = df['hours-per-week'].min()

    # 7. Pourcentage des personnes travaillant le nombre min d'heures et gagnant >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round(
        (num_min_workers['salary'] == '>50K').mean() * 100, 1
    )

    # 8. Pays avec le plus fort pourcentage de personnes gagnant >50K
    country_totals = df['native-country'].value_counts()
    country_rich_totals = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_rich_percentage = (country_rich_totals / country_totals) * 100

    highest_earning_country = country_rich_percentage.idxmax()
    highest_earning_country_percentage = round(country_rich_percentage.max(), 1)

    # 9. Métier le plus populaire pour les personnes gagnant >50K en Inde
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_rich['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print(
            "Country with highest percentage of rich:", highest_earning_country
        )
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation,
    }