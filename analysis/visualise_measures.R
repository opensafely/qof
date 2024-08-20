library(tidyverse)
library(ggplot2)
library(gridExtra)  # For arranging multiple plots

# Load data
df_measures <- readr::read_csv(
  here::here("output", "hyp", "hyp001_measures.csv")
)

df_measures <- df_measures %>%
    mutate(
        start_date = as.Date(interval_start, format = "%Y-%m-%d"),
        end_date = as.Date(interval_end, format = "%Y-%m-%d")
    )

df_resolved <- df_measures %>%
    filter(measure == "resolved_diagnosis_by_age") %>%
    mutate(age_band = case_when(
        is.na(age_band) ~ "(Missing)",
        TRUE ~ age_band
        ),
        sex = case_when(
            sex == "unknown" ~ "(Missing)",
            TRUE ~ sex
        ),
        ratio = case_when(
        is.na(ratio) ~ 0,
        TRUE ~ ratio
        )
    ) %>%
    arrange(end_date)

df_diagnosis <- df_measures %>%
    filter(measure == "diagnosis_by_age") %>%
    mutate(age_band = case_when(
        is.na(age_band) ~ "(Missing)",
        TRUE ~ age_band
        ),
        sex = case_when(
            sex == "unknown" ~ "(Missing)",
            TRUE ~ sex
        ),
        ratio = case_when(
        is.na(ratio) ~ 0,
        TRUE ~ ratio
        )
    ) %>%
    arrange(end_date)

# df_resolved_tidy <- df_resolved %>%
#     pivot_wider(
#         id_cols = c(start_date, end_date, sex),
#         names_from = age_band,
#         values_from = ratio,
#         values_fill = list(ratio = 0)
#     ) %>%
#     select(
#         start_date,
#         end_date,
#         sex,
#         `0-19`,
#         `20-39`,
#         `40-59`,
#         `60-79`,
#         `80+`
#     ) %>%
#     group_by(sex) %>%
#     arrange(end_date)


# df_diagnosis_tidy <- df_diagnosis %>%
#     pivot_wider(
#         id_cols = c(start_date, end_date, sex),
#         names_from = age_band,
#         values_from = ratio,
#         values_fill = list(ratio = 0)
#     ) %>%
#     select(
#         start_date, 
#         end_date,
#         sex, 
#         `0-19`, 
#         `20-39`, 
#         `40-59`, 
#         `60-79`, 
#         `80+`
#     ) %>%
#     group_by(sex) %>%
#     arrange(end_date)

# Filter out rows where age_band and sex is "Missing"
df_diagnosis_filtered <- df_diagnosis %>%
  filter(age_band != "(Missing)" & sex != "(Missing)")

# Create a list to store the plots
plot_list <- list()

# Unique age bands
age_bands <- c("0-19", "20-39", "40-59", "60-79", "80+")

# Generate plots for each age band
for (age_band in age_bands) {
  # Filter data for the current age band
  df_age_band <- df_diagnosis_filtered %>%
    filter(age_band == !!age_band)
  # Create the plot for the current age band
  p <- ggplot(df_age_band, aes(x = end_date, y = ratio, color = sex, group = sex)) +
    geom_line() +
    labs(title = paste("Diagnosis Ratio for Age Band:", age_band),
         x = "End Date",
         y = "Diagnosis Ratio",
         color = "Gender") +
    theme_minimal()
  
  # Add the plot from loop to the list
  plot_list[[age_band]] <- p
}

"-------------"

# Filter out rows where age_band and sex is "Missing"
df_resolved_filtered <- df_resolved %>%
  filter(age_band != "(Missing)" & sex != "(Missing)")

# Create a list to store the plots
plot_list2 <- list()

# Unique age bands
age_bands <- c("0-19", "20-39", "40-59", "60-79", "80+")

# Generate plots for each age band
for (age_band in age_bands) {
  # Filter data for the current age band
  df_age_band <- df_resolved_filtered %>%
    filter(age_band == !!age_band)
  # Create the plot for the current age band
  p1 <- ggplot(df_age_band, aes(x = end_date, y = ratio, color = sex, group = sex)) +
    geom_line() +
    labs(title = paste("Resolved Diagnosis Ratio for Age Band:", age_band),
         x = "End Date",
         y = "Resolved Ratio",
         color = "Gender") +
    theme_minimal()
  
  # Add the plot from loop to the list
  plot_list2[[age_band]] <- p1
}


