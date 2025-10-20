##lesson11

cities = ("Aleppo","Lattakia","Homs","Hama") 
pepole_of_cities=(1000000,500000,250000,450000)
most_important=("Citidal","Sea","Clock of Homs","Nawaeir")
football=("الوحدة","الكرامة","الشرطة","الوثبة")


if (len(cities)==len(pepole_of_cities)) and (len(most_important)==len(football)) and (len(cities)==len(football)):
    for i in range(len(cities)):
        print(f"The city {cities[i]} has a population of {pepole_of_cities[i]}, its most important landmark is {most_important[i]}, and its football team is {football[i]}.")
else:
    print("Error: The tuples do not have the same length.")

    