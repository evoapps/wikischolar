## ---- setup
library(dplyr)
library(broom)
library(lubridate)
library(magrittr)

library(ggplot2)
library(gridExtra)

library(lme4)
library(AICcmodavg)

## ---- data
library(wikischolarlib)
data("random1000")

random1000 <- random1000 %>%
  recode_quality %>%
  recode_age %>%
  recode_edits %>%
  recode_generations

## ---- theme
base_plot <- ggplot(random1000) +
  theme_minimal() +
  theme(
    axis.ticks = element_blank()
  )

colors <- RColorBrewer::brewer.pal(3, "Set2")
names(colors) <- c("green", "orange", "blue")

# year
year_map <- unique(random1000[, c("year0", "year")]) %>%
  arrange(year) %>%
  filter(rep_len(c(TRUE, FALSE), length.out = n()))  # label every other year
scale_x_year <- scale_x_continuous("year", breaks = year_map$year0, labels = year_map$year)

# age
current_year <- year(Sys.Date())
wiki_start <- 2001
max_age <- current_year - wiki_start
scale_x_age <- scale_x_continuous("article age", breaks = seq(0, max_age, by = 2))

# quality
scale_y_quality <- scale_y_continuous("article quality", breaks = 0:6)
scale_y_quality_diff <- scale_y_continuous(expression(paste(Delta, " quality")), breaks = 0:6)

quality_coords <- coord_cartesian(ylim = c(1, 6))

## ---- ages
extant <- random1000 %>% group_by(title) %>% filter(age == max(age))
(base_plot %+% extant) +
  ggtitle("Article ages in sample") +
  geom_histogram(aes(x = age), color = colors[["blue"]], fill = NA, binwidth = 1) +
  scale_x_age

## ---- date-mod
date_mod <- lm(quality ~ year0 + year0_sqr, data = random1000)
tidy(date_mod)

date_preds_x <- unique(random1000[,c("year0", "year0_sqr")])
date_preds_y <- predict(date_mod, date_preds_x, se = TRUE)
date_preds <- cbind(date_preds_x, date_preds_y) %>%
  select(year0, quality = fit, se = se.fit)

## ---- age-mod
age_mod <- lmer(quality ~ age + age_sqr + (age + age_sqr|title), data = random1000)
tidy(age_mod, effects = "fixed")

age_preds <- lmer_preds(random1000, c("age", "age_sqr"), age_mod)

## ---- quality
date <- base_plot +
  ggtitle("Article quality by date") +
  geom_line(aes(x = year0, y = quality, group = title),
            color = colors[["green"]], alpha = 0.2) +
  geom_point(aes(x = year0, y = quality, group = 1),
            stat = "summary", fun.y = "mean",
            size = 2, color = "black") +
  geom_line(aes(x = year0, y = quality),
            data = date_preds,
            size = 2, color = colors[["orange"]], alpha = 0.6) +
  scale_x_year +
  scale_y_quality +
  quality_coords

age <- base_plot +
  ggtitle("Article quality by age") +
  geom_line(aes(x = age, y = quality, group = title),
            color = colors[["blue"]], alpha = 0.2) +
  geom_point(aes(x = age, y = quality, group = 1),
            stat = "summary", fun.y = "mean",
            size = 2, color = "black") +
  geom_line(aes(x = age, y = quality),
            data = age_preds,
            size = 2, color = colors[["orange"]], alpha = 0.6) +
  scale_x_age +
  scale_y_quality +
  quality_coords

grid.arrange(date, age, nrow = 1)

## ---- predictors
edits <- base_plot +
  geom_point(aes(x = edits, y = quality_diff),
             color = colors[["blue"]], shape = 1) +
  scale_x_continuous("raw edits") +
  scale_y_quality_diff

generations <- base_plot +
  geom_point(aes(x = generations, y = quality_diff),
             color = colors[["green"]], shape = 1) +
  scale_y_quality_diff

grid.arrange(edits, generations, nrow = 1)

## ---- edit-types
ggplot(random1000, aes(x = edits, y = generations)) +
  geom_point() +
  geom_abline(intercept = 0, slope = 1)

ggplot(random1000, aes(x = edits_sum, y = generations_sum)) +
  geom_point() +
  geom_abline(intercept = 0, slope = 1)

## ---- edits-mod
edits_mod <- lmer(quality ~ edits_sum + (edits_sum|title),
                  data = random1000)
tidy(edits_mod, effects = "fixed")

edits_preds <- lmer_preds(random1000, "edits_sum", edits_mod)

## ---- generations-mod
generations_mod <- lmer(quality ~ generations_sum + (generations_sum|title),
                        data = random1000)
tidy(generations_mod, effects = "fixed")

generations_preds <- lmer_preds(random1000, "generations_sum", generations_mod)

## ---- cumulative-edits
base_plot +
  ggtitle("Article quality by cumulative edits") +
  geom_line(aes(x = edits_sum, y = quality, group = title),
            color = colors[["blue"]], alpha = 0.2) +
  geom_point(aes(x = edits_sum, y = quality, group = 1),
             stat = "summary", fun.y = "mean",
             size = 2, color = "black") +
  geom_line(aes(x = edits_sum, y = quality),
            data = edits_preds,
            size = 2, color = colors[["orange"]], alpha = 0.6) +
  scale_y_quality +
  quality_coords

## ---- cumulative-generations
base_plot +
  ggtitle("Article quality by cumulative edits") +
  geom_line(aes(x = generations_sum, y = quality, group = title),
            color = colors[["blue"]], alpha = 0.2) +
  geom_point(aes(x = generations_sum, y = quality, group = 1),
             stat = "summary", fun.y = "mean",
             size = 2, color = "black") +
  geom_line(aes(x = generations_sum, y = quality),
            data = generations_preds,
            size = 2, color = colors[["orange"]], alpha = 0.6) +
  scale_y_quality +
  quality_coords