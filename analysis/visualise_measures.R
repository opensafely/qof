library(tidyverse)
library(patchwork)
library(here)

# Load data
df_measures <- read_csv(
  here("output", "hyp", "hyp001_measures.csv")) %>%
  replace_na(list(age_band = "(Missing)")) %>%
  mutate(
    start_date = as.Date(interval_start, format = "%Y-%m-%d"),
    end_date = as.Date(interval_end, format = "%Y-%m-%d"),
    age_band = factor(
      age_band,
      levels = c("0-19", "20-39", "40-59", "60-79", "80+", "(Missing)"),
      labels = c("0-19", "20-39", "40-59", "60-79", "80+", "(Missing)")
      )
  )

plot_hypres <- df_measures %>%
  filter(measure == "resolved_diagnosis_by_age") %>%
  ggplot(aes(
    x = end_date,
    y = ratio,
    colour = age_band,
  )) +
  geom_point() +
  geom_line(alpha = .5) +
  labs(
    title = NULL,
    x = NULL,
    y = "Patients with hypertension resolved code",
    colour = "Age band"
  ) +
  scale_y_continuous(
    labels = scales::label_percent(),
    limits = c(0, 1)
  ) +
  facet_wrap(~ factor(
    sex,
    levels = c("female", "male", "intersex", "unknown"),
    labels = c("Female", "Male", "Intersex", "Unknown")
  ))

plot_hyp <- df_measures %>%
  filter(measure == "diagnosis_by_age") %>%
  ggplot(aes(
    x = end_date,
    y = ratio,
    colour = age_band,
  )) +
  geom_point() +
  geom_line(alpha = .5) +
  labs(
    title = NULL,
    x = NULL,
    y = "Patients with hypertension code",
    colour = "Age band"
  ) +
  scale_y_continuous(
    labels = scales::label_percent(),
    limits = c(0, 1)
  ) +
  facet_wrap(~ factor(
    sex,
    levels = c("female", "male", "intersex", "unknown"),
    labels = c("Female", "Male", "Intersex", "Unknown")
  ))

plot_hyp <- (plot_hyp / plot_hypres) +
  plot_layout(guides = "collect")

ggsave("output/hyp/hyp_plot.png", width = 8, height = 8)
