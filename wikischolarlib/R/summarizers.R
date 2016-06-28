
weighted_quality <- function(Stub, Start, C, B, GA, FA) {
  (Stub * 1) + (Start * 2) + (C * 3) + (B * 4) + (GA * 5) + (FA * 6)
}


#' Format the predicted values from an lmer model.
#'
#' @param frame The data.frame used to fit the model.
#' @param x_pred_vars A character vector of columns in frame used as
#'        predictors in the model.
#' @param lmer_mod An lmer model object to obtain predictions from.
#'
#' @import dplyr
#' @import AICcmodavg
#'
#' @export
lmer_preds <- function(frame, x_pred_vars, lmer_mod) {
  x_preds <- select_(frame, .dots = x_pred_vars) %>%
    na.omit %>%
    unique
  y_preds <- predictSE(lmer_mod, x_preds, se = TRUE)
  cbind(x_preds, y_preds) %>%
    select_(x_pred_vars, quality = "fit", se = "se.fit")
}
