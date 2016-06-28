#' Recode the quality column.
#'
#' Create new columns based off quality column in frame.
#'
#' The following columns will be created:
#'
#' \itemize{
#'   \item quality_diff. The difference in quality between the current version
#'         and the previous.
#' }
#'
#' @examples
#' library(wikischolarlib)
#' data("random1000")
#' random1000 <- recode_quality(random1000)
#'
#' @import dplyr
#' @export
recode_quality <- function(frame) {
  frame %>%
    group_by(title) %>%
    mutate(quality_diff = c(NA, diff(quality))) %>%
    ungroup
}


#' Recode the age column.
#'
#' Create new columns based off the age column in the frame.
#'
#' The following columns will be created:
#' \itemize{
#'   \item age_sqr. The age variable squared.
#' }
#'
#' @import dplyr
#' @export
recode_age <- function(frame) {
  age_map <- data_frame(
    age = unique(frame$age),
    age_sqr = age^2
  )
  frame %>% left_join(age_map)
}


#' Recode the edits column.
#'
#' Create new columns based off the edits column in the frame.
#'
#' The following columns will be created:
#' \itemize{
#'   \item edits_sum. The total number of edits to this article so far.
#'   \item edits_sqr. The edits_sum variable squared.
#' }
#'
#' @import dplyr
#' @import magrittr
#' @export
recode_edits <- function(frame) {
  frame %<>%
    group_by(title) %>%
    mutate(edits_sum = cumsum(edits)) %>%
    ungroup

  edits_map <- data_frame(
    edits_sum = unique(frame$edits_sum),
    edits_sum_sqr = edits_sum^2
  )

  frame %>% left_join(edits_map)
}


#' Recode the generations column.
#'
#' Create new columns based off the generations column in the frame.
#'
#' The following columns will be created:
#' \itemize{
#'   \item generations_sum. The total number of generations to this article
#'         so far.
#'   \item generations_sum_sqr. The generations_sum variable squared.
#' }
#'
#' @import dplyr
#' @import magrittr
#' @export
recode_generations <- function(frame) {
  frame %<>%
    group_by(title) %>%
    mutate(generations_sum = cumsum(generations)) %>%
    ungroup

  generations_map <- data_frame(
    generations_sum = unique(frame$generations_sum),
    generations_sum_sqr = generations_sum^2
  )

  frame %>% left_join(generations_map)
}
