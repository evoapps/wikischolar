library(testthat)
library(wikischolarlib)

library(dplyr)
library(magrittr)

context("Model summarizers")

# setup fixture data
library(lme4)
data("sleepstudy")

test_that("lmer preds works on sleepstudy data", {
  mod <- lmer(Reaction ~ Days + (Days|Subject), data = sleepstudy)
  preds <- lmer_preds(sleepstudy, "Days", mod)
  expect_equal(preds$Days, 0:9)
})

test_that("lmer preds works on missing x preds", {
  sleepstudy$DaysMissing <- sleepstudy$Days
  sleepstudy[sample(rownames(sleepstudy), size = 5), "DaysMissing"] <- NA

  mod <- lmer(Reaction ~ DaysMissing + (DaysMissing|Subject), data = sleepstudy)
  preds <- lmer_preds(sleepstudy, "DaysMissing", mod)

  expect_equal(preds$DaysMissing, 0:9)
})
