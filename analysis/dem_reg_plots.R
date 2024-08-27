# Set up
library(tidyverse)
library(lubridate)
df <- read.csv("output/dem/dem_reg_measures.csv")

# summary(df) - confirms that there are 37 missing ratios and 24 missing imds

# Dementia prevalence plot, stratified by IMD
df %>%
  filter(!is.na(imd)) %>%
  ggplot(aes (x = ymd(interval_start), y = ratio, color = as.factor(imd))) +
  geom_line()+
  labs (
    title = "Dementia prevalence over time, per IMD group", 
    x = NULL, 
    y = "Prevalence of dementia",
    color = "Index of multiple depravation"
    ) +
  theme_light()

ggsave("output/dem/dem_rates_imd.png")

# Dementia prevalence, unstratified

df %>%
filter(is.na(imd)) %>%
ggplot(aes (x = ymd(interval_start), y = ratio)) +
geom_line() +
labs (
    title = "Dementia prevalence over time, unstratfied", 
    x = NULL, 
    y = "Prevalence of dementia"
    ) +
theme_light()

ggsave("output/dem/dem_rates.png")