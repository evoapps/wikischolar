library(devtools)
library(readr)

qualities <- read_csv("data-raw/qualities.csv")

use_data(qualities, overwrite = TRUE)
