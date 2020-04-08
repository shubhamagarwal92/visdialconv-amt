library(dplyr)
library(reshape2)
library(ggplot2)
library(psych)
require(RJSONIO)
library(jsonlite)
library(irr)


# https://www.youtube.com/watch?v=fT2No3Io72g
# my_data <- read.delim(file.choose())
# levels(my_data$group)
# my_data$group <- ordered(my_data$group,
#                          levels = c("ctrl", "trt1", "trt2"))
# combined_grps = data.frame(cbind())


calculate_anova <- function(csv_file) {
  df_all <- read.csv(csv_file, header=T, row.names=NULL)
  # NOTE: TODO we have index as the first element
  df_all = df_all[2:length(df_all)]
  stacked_groups = stack(df_all)
  res.aov <- aov(values ~ ind, data = stacked_groups)
  # Summary of the analysis
  summary(res.aov)
  # TukeyHSD(res.aov)
}




csv_file = "ndcg_sparse_all.txt"
calculate_anova(csv_file)

csv_file = "ndcg_finetune_all.txt"
calculate_anova(csv_file)