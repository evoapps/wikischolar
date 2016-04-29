library(devtools)
library(dplyr)
library(lubridate)
library(readr)

articles <- read_csv("data-raw/articles.csv")
revisions <- read_csv("data-raw/revisions.csv")
qualities <- read_csv("data-raw/qualities.csv")

labeled_revisions <- left_join(revisions, qualities)
random1000 <- merge(articles, labeled_revisions)

# Set order for article classes
article_classes <- c("Stub", "Start", "C", "B", "GA", "FA")
random1000$prediction <- factor(random1000$prediction, levels = article_classes)

# Compute article age
random1000 <- random1000 %>%
  group_by(title) %>%
  mutate(year0 = min(year(timestamp))) %>%
  ungroup %>%
  mutate(age = year(timestamp) - year0)

# Calculate continuous article quality
weighted_quality <- function(Stub, Start, C, B, GA, FA) {
  (Stub * 1) + (Start * 2) + (C * 3) + (B * 4) + (GA * 5) + (FA * 6)
}
random1000$quality <- with(random1000, weighted_quality(Stub,Start,C,B,GA,FA))

use_data(random1000, overwrite = TRUE)
