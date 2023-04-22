library(GGally)
library(ggplot2)
library(datasets)
library(magrittr)
library(cluster)

# ZADANIE 1
lst <- 1:10
lst %<>% log2 %<>% sin %<>% sum %<>% sqrt
print(lst)

data(iris)
head(iris)
agg <- iris %>% aggregate(. ~ Species, ., mean)
print(agg)

# ZADANIE 2

ggplot(iris, aes(x = Sepal.Width)) +
  geom_histogram(aes(fill = Species, color = Species), bins=20) +
  geom_vline(data = agg, aes(xintercept = Sepal.Width, color = Species), linetype='dashed') +
  labs(x = 'X', y = 'Y', title = 'Title')

ggpairs(data = iris, aes(color = Species))

# ZADANIE 3

x <- iris[, 1:4]
y <- iris[, 5]

sum <- NULL

for (i in 1:10)
{
  result <- kmeans(x, i)
  sum <- append(sum, result$tot.withinss)
}

ggplot(data.frame(iteration = seq_along(sum), value = sum), aes(x = iteration, y = sum)) +
  geom_line()

result2 <- kmeans(x, 3)
ggplot(iris, aes(x = Sepal.Width, y = Petal.Width, color = result2$cluster)) + geom_point()

ggplot(iris, aes(x = Sepal.Width, y = Petal.Width, color = Species)) + geom_point()
