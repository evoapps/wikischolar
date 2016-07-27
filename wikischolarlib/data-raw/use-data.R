library(devtools)
library(dplyr)
library(lubridate)
library(readr)
library(magrittr)

source("R/summarizers.R")

overwrite <- TRUE
article_classes <- c("Stub", "Start", "C", "B", "GA", "FA")

read_wikischolar_data <- function(data_dir) {
  wikischolar_csv <- function(table) file.path("data-raw", data_dir, paste0(table, ".csv"))

  articles <- wikischolar_csv("articles") %>% read_wikischolar_table
  edits <- wikischolar_csv("edits") %>% read_wikischolar_table
  generations <- wikischolar_csv("generations") %>% read_wikischolar_table

  qualities <- wikischolar_csv("qualities") %>%
    read_wikischolar_table %>%
    mutate(
      quality = weighted_quality(Stub, Start, C, B, GA, FA),
      prediction = factor(prediction, levels = article_classes)
    ) %>%
    select(title, timestamp, prediction, quality) %>%
    arrange(title, timestamp)

  wikischolar <- articles %>%
    left_join(qualities) %>%
    left_join(edits) %>%
    left_join(generations)

  wikischolar %<>%
    mutate(year = year(timestamp)) %>%
    group_by(title) %>%
    mutate(year0 = min(year)) %>%
    ungroup %>%
    mutate(age = year - year0)

  wikischolar
}

read_wikischolar_table <- function(table_csv) {
  read_csv(table_csv) %>%
    select(-1)  # drop index col
}

random1000 <- read_wikischolar_data("random1000")
use_data(random1000, overwrite = overwrite)

# featured1000 <- read_wikischolar_data("featured1000")
# use_data(featured1000, overwrite = overwrite)
