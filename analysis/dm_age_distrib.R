library('tidyverse')

df_dm_reg <- read_csv(
  here::here("output", "dataset_dm_marr.csv.gz"),
  col_types = cols(age = col_double())
)

plot_dm_age <- ggplot(data = df_dm_reg, aes(df_dm_reg$age)) + geom_histogram()


ggsave(
  plot= plot_dm_age,
  filename="report_histo_dm_marr.png", path=here::here("output"),
)
