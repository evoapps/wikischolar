## ---- setup--------------------------------------------------------------
library(dplyr)
library(broom)
library(lubridate)

library(ggplot2)

library(lme4)

## ---- data, echo = TRUE--------------------------------------------------
library(wikischolarlib)
data(random1000)

## ---- theme--------------------------------------------------------------
base_plot <- ggplot(random1000) +
  theme_minimal() +
  theme(
    axis.ticks = element_blank()
  )

current_year <- year(Sys.Date())
wiki_start <- 2001
max_age <- current_year - wiki_start

scale_x_age <- scale_x_continuous("article age", breaks = seq(0, max_age, by = 2))
scale_y_quality <- scale_y_continuous("article quality", breaks = 0:6)
quality_coords <- coord_cartesian(ylim = c(0, 6))

## ---- quality-by-date----------------------------------------------------
base_plot +
  ggtitle("Article quality by date") +
  geom_line(aes(x = timestamp, y = quality, group = title)) +
  scale_x_date("date") +
  scale_y_quality +
  quality_coords

## ---- quality-by-date-average--------------------------------------------
base_plot +
  ggtitle("Average article quality by date") +
  geom_line(aes(x = timestamp, y = quality, group = 1),
            stat = "summary", fun.y = "mean") +
  scale_x_date("date") +
  scale_y_quality +
  quality_coords

## ---- quality-by-age-----------------------------------------------------
base_plot +
  ggtitle("Article quality by age") +
  geom_line(aes(x = age, y = quality, group = title)) +
  scale_x_age +
  scale_y_quality +
  quality_coords

## ---- quality-by-age-average---------------------------------------------
base_plot +
  ggtitle("Average article quality by age") +
  geom_line(aes(x = age, y = quality, group = 1),
            stat = "summary", fun.y = "mean") +
  scale_x_age +
  scale_y_quality +
  quality_coords

## ---- hist-article-ages--------------------------------------------------
extant <- random1000 %>% group_by(title) %>% filter(age == max(age))
(base_plot %+% extant) +
  ggtitle("Article ages in sample") +
  geom_histogram(aes(x = age), binwidth = 1) +
  scale_x_age

## ---- age-lmer
age_mod <- lmer(quality ~ age + (age|title), data = random1000)
tidy(age_mod, effect = "fixed")
