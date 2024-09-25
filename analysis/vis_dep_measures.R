library(ggplot2)
library(dplyr)
library(zoo)

# Loading measures dataset
measures <- read.csv('output/dep/dep_jaidip.csv.gz')

# Reformatting data for plotting
measures$interval_start <- as.yearmon(measures$interval_start)
measures_total <- summarise(group_by(measures, interval_start), numerator = sum(numerator))

# Plotting data using line graph
plot <- ggplot(measures_total, aes(x = interval_start, y = numerator, group = 1)) +
    geom_line() +
    geom_point() +
    labs(x = 'Month', y = 'Prevalence', title = 'Monthly Depression Prevalence')
ggsave(plot, 'output/dep/viz_dep_measures.png')

# Stratified by sex
measures_sex = summarise(group_by(measures, interval_start, sex), numerator = sum(numerator))
plot2 <- ggplot(measures_total, aes(x = interval_start, y = numerator, color = sex)) +
    geom_line() +
    geom_point() +
    labs(x = 'Month', y = 'Prevalence', title = 'Monthly Depression Prevalence by Sex')
ggsave(plot2, 'output/dep/viz_dep_measures_sex.png')