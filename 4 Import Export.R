# Importing and Exporting Data in R.

# Importing Libraries.
# Note: Install pacman Package if you want to load packages like this. 
pacman::p_load(pacman, rio, jsonlite, writexl)

# Import.
print("Importing")
# CSV File Import.
print("CSV File Import")
csv <- read.csv("C:\\Users\\LENOVO\\Desktop\\R Programs\\Churn_Modelling.csv")

print("Class")
print(class(csv))

print("Summary")
print(summary(csv))

print("Structure")
print(str(csv))

print("Head")
print(head(csv))

print("Tail")
print(tail(csv))

print("First 10 Records of Geography Column")
print(csv$Geography[1:10])

print("Maximum of Balance")
print(max(csv$Balance))

print("Minimum of Balance")
print(min(csv$Balance))

print("Mean of Balance")
print(mean(csv$Balance))

print("Median Age")
print(median(csv$Age))

print("Subset of the Dataset which has records having Age > 80")
print(subset(csv, Age > 80))


# Excel File Import.
print("Excel File Import")
excel <- import("D:\\Downloads\\Amazon Sales Data.xlsx")
print("Class")
print(class(excel))

print("Summary")
print(summary(excel))

print("Structure")
print(str(excel))

print("Head")
print(head(excel))

print("Tail")
print(tail(excel))

print("First 10 Records of Item Column")
print(excel$Item[1:10])

print("Maximum of Total Sale Amount")
print(max(excel$`Total Sale Amount`))

print("Minimum of Price")
print(min(excel$Price))

print("Mean of Quantity")
print(mean(excel$Quantity))

print("Median of Quantity")
print(median(excel$Quantity))

print("Printing Subset of the Dataset which has records having Quantity > 6 ")
print(subset(excel, Quantity > 6))


# Text File Import.
print("Text file Import")
textFile <- import("D:\\Downloads\\TUMORdata.txt")
print("Class")
print(class(textFile))

print("Summary")
print(summary(textFile))

print("Structure")
print(str(textFile))

print("Head")
print(head(textFile))

print("Tail")
print(tail(textFile))

print("Median of Time")
print(median(textFile$time))

print("Maximum of futime")
print(max(textFile$futime))

print("Unique values and their frequencies in Size Column")
print(table(textFile$size))

# JSON File Import.
print("Import JSON File")
jsonFile <- fromJSON("D:\\Downloads\\free-bike-status-1.json")
print("All column names")
print(names(jsonFile))

print("Class")
print(class(jsonFile))

print("Summary")
print(summary(jsonFile))

print("Structure")
print(str(jsonFile))

print("Head")
print(head(jsonFile))

print("Tail")
print(tail(jsonFile))

print("Unique Bike Names")
print(table(jsonFile$name))

# URL File Import.
# I got the data from GitHub API: https://api.github.com/users/RahulKanwal/repos
# In place of "RahulKanwal", if you put your username, you'll get your repositories data.
print("Import URL File")
URLFile <- fromJSON("https://api.github.com/users/RahulKanwal/repos")

print("Print all the column names")
print(names(URLFile))

print("Number of Repositories")
print(length(URLFile$name))

print("Names of all the repositories")
print(URLFile$name)

print("Total sum of size")
cat(sum(URLFile$size), "KB", "\n")

print("Get all the unique languages used")
print(unique(URLFile$language))

# Export.
print("Exporting")

# CSV File Export.
print("Exporting to CSV")
csvOp <- write.csv(URLFile, "githubData.csv")

# Excel File Export.
print("Exporting to Excel")
excelOp <- write_xlsx(jsonFile, "bike_status.xlsx")

# Text File Export.
print("Exporting to Text File")
students_df <- data.frame(
  firstName = c("Mikasa", "Reiner", "Bertholdt", "Annie", "Eren", "Jean", "Marco", "Connie", "Sasha", "Krista"),
  lastName = c("Ackerman", "Braun", "Hoover", "Leonhart", "Jaeger", "Kirstein", "Bott", "Springer", "Blouse", "Lenz"),
  rank = c(1:10),
  gender = factor(c("F", "M", "M", "F", "M", "M", "M", "M", "F", "F")),
  rollNo = c(1, 5, 6, 10, 7, 8, 4, 11, 3, 9)
)
textOp <- write.table(students_df, "AttackOnTitan.txt", sep = ",")

# JSON File Export.
print("Exporting to JSON")
jsonOp <- write_json(csv, "churnModelling.json")

# Tab Seperated File Export. 
print("Exporting to Tab Seperated File")
tabOp <- write.table(textFile, "TUMORdata.txt", sep = "\t")


# print("Text file Import")
# textFile11 <- import("http://courses.washington.edu/b517/Datasets/MRI.txt")
# print(names(textFile11))
# 
# print(median(textFile11$weight))

