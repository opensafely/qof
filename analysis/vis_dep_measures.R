library(ggplot2)
library(dplyr)
library(zoo)

measures <- read.csv('output/dep/dep_jaidip.csv.gz')
measures$interval_start <- as.yearmon(measures$interval_start)
measures_total <- summarise(group_by(measures, interval_start), numerator = sum(numerator))

plot <- ggplot(measures_total, aes(x = interval_start, y = numerator, group = 1)) +
    geom_line() +
    geom_point() +
    labs(x = 'Month', y = 'Prevalence', title = 'Monthly Depression Prevalence')

ggsave('output/dep/viz_dep_measures.png')