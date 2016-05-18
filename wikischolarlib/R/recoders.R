#' Recode year/age variables for modeling.
#'
#' Requires columns: year, age.
#'
#' @export
recode_quadratic <- function(frame) {
  frame %>%
    mutate(
      year0 = year - min(year),
      year0_sqr = year0^2,
      age_sqr = age^2
    )
}
