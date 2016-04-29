library(devtools)
library(dplyr)
library(lubridate)
library(readr)

qualities <- read_csv("data-raw/qualities.csv")

# Set order for article classes
article_classes <- c("Stub", "Start", "C", "B", "GA", "FA")
qualities$prediction <- factor(qualities$prediction, levels = article_classes)

# Compute article age
qualities <- qualities %>%
  group_by(article) %>%
  mutate(year0 = min(year(timestamp))) %>%
  ungroup %>%
  mutate(age = year(timestamp) - year0)

use_data(qualities, overwrite = TRUE)
