library(devtools)
library(dplyr)
library(lubridate)
library(readr)
library(magrittr)

source("R/summarizers.R")


# Articles
# ========
articles <- read_csv("data-raw/articles.csv")
use_data(articles, overwrite = TRUE)
articles <- articles %>%
  select(title)


# Qualities
# =========
revisions <- read_csv("data-raw/revisions.csv")
qualities <- read_csv("data-raw/qualities.csv") %>%
  left_join(revisions)
use_data(qualities, overwrite = TRUE)

qualities <- qualities %>%
  mutate(quality = weighted_quality(Stub, Start, C, B, GA, FA)) %>%
  select(title, timestamp, prediction, quality) %>%
  arrange(title, timestamp)


# Edits
# =====
edits <- read_csv("data-raw/edits.csv")
use_data(edits, overwrite = TRUE)
edits <- edits %>% select(title, timestamp, edits = revid)


# Views
# =====
views <- read_csv("data-raw/views.csv")
use_data(views, overwrite = TRUE)


# Merge all data
# ==============
random1000 <- articles %>%
  left_join(qualities) %>%
  left_join(edits) %>%
  left_join(views)

# Set order for article classes
article_classes <- c("Stub", "Start", "C", "B", "GA", "FA")
random1000$prediction <- factor(random1000$prediction, levels = article_classes)

# Compute article age
random1000$year <- year(random1000$timestamp)
random1000 <- random1000 %>%
  group_by(title) %>%
  mutate(year0 = min(year)) %>%
  ungroup %>%
  mutate(age = year - year0)


# Drop weird observations
random1000 <- random1000 %>%
  filter(year0 >= 0)


use_data(random1000, overwrite = TRUE)
